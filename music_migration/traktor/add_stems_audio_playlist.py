"""Build a Traktor playlist of every live COLLECTION entry under stems_audio.

Dry-run is the default. Quit Traktor before --execute.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from music_migration.traktor.fix_nml_playlists import loc_to_key, loc_to_path

TRAKTOR_DIR = Path.home() / "Documents/Native Instruments/Traktor 4.5.1"
DEFAULT_NML = TRAKTOR_DIR / "collection.nml"
STEMS_ROOT = Path.home() / "Music" / "stems_audio"
PLAYLIST_NAME = "stems_audio"


def stems_entries(collection: ET.Element) -> list[tuple[str, str]]:
    """Return (pk_type, key) for live stems_audio locations, sorted by path."""
    found: list[tuple[str, str, Path]] = []
    for entry in collection.findall("ENTRY"):
        location = entry.find("LOCATION")
        if location is None:
            continue
        directory = location.get("DIR") or ""
        file_attr = location.get("FILE") or ""
        volume = location.get("VOLUME") or "Macintosh HD"
        if "stems_audio" not in directory:
            continue
        path = loc_to_path(directory, file_attr)
        try:
            path.relative_to(STEMS_ROOT)
        except ValueError:
            continue
        if not path.is_file():
            continue
        pk_type = "STEM" if ".stem." in path.name.lower() else "TRACK"
        found.append((pk_type, loc_to_key(volume, directory, file_attr), path))
    found.sort(key=lambda row: str(row[2]).lower())
    return [(pk_type, key) for pk_type, key, _ in found]


def ensure_playlist(root_folder: ET.Element, name: str) -> ET.Element:
    subnodes = root_folder.find("SUBNODES")
    if subnodes is None:
        raise SystemExit("PLAYLISTS $ROOT is missing SUBNODES")
    for node in subnodes.findall("NODE"):
        if node.get("TYPE") == "PLAYLIST" and node.get("NAME") == name:
            playlist = node.find("PLAYLIST")
            if playlist is not None:
                playlist.clear()
                return playlist
    node = ET.Element(
        "NODE",
        TYPE="PLAYLIST",
        NAME=name,
    )
    playlist = ET.SubElement(
        node,
        "PLAYLIST",
        ENTRIES="0",
        TYPE="LIST",
        UUID=uuid.uuid4().hex,
    )
    # Keep review crate visible at the top of $ROOT, before year folders.
    subnodes.insert(0, node)
    subnodes.set("COUNT", str(len(list(subnodes))))
    return playlist


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--nml", type=Path, default=DEFAULT_NML)
    parser.add_argument("--name", default=PLAYLIST_NAME)
    args = parser.parse_args()
    dry_run = not args.execute
    nml_path = args.nml.expanduser().resolve()
    if not nml_path.exists():
        print(f"Error: NML not found: {nml_path}", file=sys.stderr)
        return 1

    started = time.time()
    tree = ET.parse(nml_path)
    root = tree.getroot()
    collection = root.find("COLLECTION")
    playlists = root.find("PLAYLISTS")
    if collection is None or playlists is None:
        print("Error: COLLECTION or PLAYLISTS missing.", file=sys.stderr)
        return 1
    root_folder = playlists.find("NODE")
    if root_folder is None or root_folder.get("NAME") != "$ROOT":
        print("Error: $ROOT playlist folder missing.", file=sys.stderr)
        return 1

    rows = stems_entries(collection)
    stems = sum(1 for pk_type, _ in rows if pk_type == "STEM")
    tracks = len(rows) - stems
    print(
        f"{'DRY-RUN' if dry_run else 'EXECUTE'}: {len(rows):,} live stems_audio "
        f"({stems:,} STEM / {tracks:,} TRACK) → playlist '{args.name}'"
    )
    if dry_run:
        for pk_type, key in rows[:8]:
            print(f"  {pk_type:5} {key.split('/:')[-1]}")
        print("No NML written. Re-run with --execute after quitting Traktor.")
        print(f"Execution time: {time.time() - started:.2f}s")
        return 0

    playlist = ensure_playlist(root_folder, args.name)
    for pk_type, key in rows:
        entry = ET.SubElement(playlist, "ENTRY")
        ET.SubElement(entry, "PRIMARYKEY", TYPE=pk_type, KEY=key)
    playlist.set("ENTRIES", str(len(rows)))

    backup = nml_path.with_suffix(nml_path.suffix + ".stems_audio.bak")
    if backup.exists():
        backup.unlink()
    shutil.copy2(nml_path, backup)
    tree.write(nml_path, encoding="UTF-8", xml_declaration=True)
    print(f"Backed up to: {backup}")
    print(f"Wrote:       {nml_path}")
    print("Reopen Traktor. Playlist is at the top of Playlists: stems_audio.")
    print(f"Execution time: {time.time() - started:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
