"""python3 -m music_migration  →  list CLI entry points."""

from __future__ import annotations

COMMANDS = [
    ("music_migration.traktor.update_nml_paths", "Remap Traktor collection.nml"),
    ("music_migration.traktor.fix_nml_playlists", "Repair playlist PRIMARYKEYs"),
    ("music_migration.traktor.add_stems_audio_playlist", "Playlist of live stems_audio tracks"),
    ("music_migration.rekordbox.traktor_to_rekordbox", "Merge Traktor → Rekordbox XML"),
    ("music_migration.rekordbox.heal_rekordbox_paths", "Heal dead RB XML locations"),
    ("music_migration.rekordbox.relocate_rekordbox_collection", "Relink Collection master.db"),
    ("music_migration.rekordbox.restore_rekordbox_master_db", "Restore master.db from backup"),
    ("music_migration.apple_music.hoist_apple_music", "Hoist Media.localized/Music/"),
    ("music_migration.apple_music.fix_apple_music_library_paths", "Music.app path symlink"),
    ("music_migration.stems.organize_stems", "Organize stems_audio Artist/Album"),
    ("music_migration.stems.cleanup_staging", "Rescue + delete staging trees"),
]


def main() -> None:
    print("music_migration — run from repo root:\n")
    for mod, desc in COMMANDS:
        print(f"  python3 -m {mod} --help")
        print(f"      {desc}\n")


if __name__ == "__main__":
    main()
