# Progress Log — music_migration

Chronological notes for the DJ library migration. Canonical paths and architecture live in [`MASTER_CONTEXT.md`](MASTER_CONTEXT.md).

This file + `git log` is the project journal (Confluence without the ceremony).

---

## 2026-08-30 — stems_audio review playlist

Added top-level Traktor playlist **stems_audio**: 4,968 live collection entries under `~/Music/stems_audio` (1,212 STEM + 3,756 TRACK, including vocals/instrumental). Command: `python3 -m music_migration.traktor.add_stems_audio_playlist --execute`. Backup `collection.nml.stems_audio.bak`. Open Playlists → **stems_audio** (first in the list). DJCU2 that crate when David wants it in Rekordbox.

---

## 2026-08-30 — Traktor remap after ix crate dump

ix `crate/` emptied Unknown Album, mashups, and `_outliers/Inbox`. Then:

- Quit Traktor Pro 4.
- `update_nml_paths --nml` live `Traktor 4.5.1/collection.nml` **executed**. 4,952 stems + 22,612 Music.app files relinked. 1,302 unmatched (factory/orphans, same class as 2026-08-20). Backup `collection.nml.bak`.
- `fix_nml_playlists --execute`: 100 playlist keys repaired (Unknown Album / mashup dests), **0 unresolved**. Backup `collection.nml.playlists.bak`.
- Reopened Traktor. Do not DJCU2 until David confirms playlists.

---

## 2026-08-21 — Post-move dry-run; GitHub Desktop attached

Clone is at `~/github/ixamal/music_migration`. GitHub Desktop shows the same five local files. All `python3 -m music_migration.* --dry-run` runs from the new path; counts match 2026-08-20. No `--execute`. Do not run hoist, organize, or traktor_to_rekordbox against local XML.

---

## 2026-08-20 (late) — Clone moved to ~/github/ixamal

Working copy moved `~/Music/MIGRATED_ORPHANS` → `~/github/ixamal/music_migration` (same `origin`, not a second clone). Org folder: `~/github/alkalurop/` (empty). Open this path in Cursor and **Add local repository** in GitHub Desktop. Parent folders are not git repos.

---

## 2026-08-20 (late) — Canned; BlackHole is a new repo

`music_migration` is parked. Performance-rig work (BlackHole + S88 MkII / S8 / DDJ-FLX10) moves to **https://github.com/ixamal/blackhole** (`~/github/ixamal/blackhole` when created). Reopen this repo when a remap or MRBT retag is needed.

---

## 2026-08-20 (late) — Package dry-runs (no `--execute`)

All `python3 -m music_migration.*` entry points imported and ran dry-run. `--dry-run` is now accepted everywhere (default is still no writes). Manifests land in `config/`.

| Command | Result |
|---------|--------|
| `traktor.update_nml_paths` | Would relink 22,132; 2,812 unmatched. No NML write. |
| `traktor.fix_nml_playlists` | 2,396 keys live; 0 repairs; 144 unresolved (loops/recordings). |
| `rekordbox.heal_rekordbox_paths` | 22,930 OK; 0 heal; 74 still missing (SoundCloud leftovers). |
| `rekordbox.relocate_rekordbox_collection` | 1,543 live; 0 writes; 224 streaming + 19 dead. RB was running (read-only). |
| `rekordbox.traktor_to_rekordbox` | Terrarum master missing. Against local XML: 22,259 Location updates (case like Latour/LaTour); **do not execute** unless we want that rewrite. |
| `rekordbox.restore_rekordbox_master_db` | Terrarum `rekordbox_db_old` not mounted — expected. |
| `apple_music.hoist_apple_music` | First dry-run followed `Music` → `.` and planned 23,334 self-dupes. Guard added: symlink → no-op. |
| `apple_music.fix_apple_music_library_paths` | Compat symlink already in place. |
| `stems.organize_stems` | After self-path fix: 3,835 already OK; 46 leftover moves (tag/folder case). Do not `--execute`. |
| `stems.cleanup_staging` | Staging trees gone; 1 Google Drive shortcut junk listed. |

Do not `--execute` hoist or organize — library is already laid out.

---

## 2026-08-20 (late) — Package layout before BlackHole

Scripts grouped under `music_migration/` with `__init__.py`:

- `traktor/` `rekordbox/` `apple_music/` `stems/`
- Run: `python3 -m music_migration` or `python3 -m music_migration.traktor.update_nml_paths --dry-run`
- Old one-shots → `archive/` (was `archive_py_json/`)
- JSON catalogs/manifests → `config/` (`music_migration/paths.py`)

---

## 2026-08-20 — Apple Music hoist EXECUTED; Traktor + Rekordbox remapped

- Sampler pads: David will rebuild by hand over time. Parked.
- `hoist_apple_music.py --execute` with Music/Traktor/Rekordbox quit:
  - **18,194** moved, **0** errors, **121** kept as `(2)` collisions
  - Nested `Media.localized/Music/` removed (only leftover `.DS_Store` dirs, then pruned)
  - Tree now `{Artist}/{Album}/` — **22,759** of **22,769** audio at depth 3
- Terrarum not mounted → remapped **live** NML (not master). `update_nml_paths.py --nml` + hoist-prefix strip.
- Traktor COLLECTION: **22,259** live / **2,685** miss (old unmatched + factory sounds). Playlist keys: **2,382** live, **905** repaired across two passes, **144** unresolved (recordings/loops/known orphans).
- Rekordbox XML heal: **17,351** nested Music/ paths fixed; **22,930** live / **74** miss / **0** still nested.
- **You:** open Music.app and let it relink; reload rekordbox xml in RB7; reopen Traktor.
- Next: BlackHole + controllers.

### Library.musicdb is encrypted — symlink compat (same night)

Music.app asked Locate per-track (`Less Than Burning Hawt`). `Library.musicdb` is hfma/encrypted; cannot rewrite paths. Locate also started recreating `Media.localized/Music/` (3 files pulled back).

`fix_apple_music_library_paths.py --execute`:
- Backed up musicdb → `~/Music/PioneerDJ/apple_music_library_backups/20260820_221307/`
- Moved the 3 Locate strays back to `{Artist}/{Album}/`
- Replaced nested `Music/` with symlink **`Media.localized/Music` → `.`**
- Old library path now resolves: `Media.localized/Music/Pivots/These Beets/Less Than Burning Hawt.m4a`

Reopen Music.app — playlists should find files without Locate. If Music has **Keep Media folder organized** on, turn it off so it doesn’t fight the symlink.

David confirmed: Music playback/playlists worked; he also cleaned playlists by hand.

**Rekordbox Collection relocate (same night):** XML was already healthy (22,930 live). Per-track Relocate was **Collection** (`master.db`), not XML. With RB quit, `relocate_rekordbox_collection.py --execute` updated **1,157** `FolderPath`s by basename (stems_audio). Left: **224** streaming URLs + **19** dead Downloads/Documents. Backup: `~/Music/PioneerDJ/rekordbox_library_backup_before_old_db/collection_relocate_20260820_223948/`. Reopen Rekordbox.

**Parked — MRBT genre retag (later, with Ollama):** redo genre across Music + Rekordbox + Traktor. Source of truth = file tags; crates/set names (Pivots, Humidor, In My Soul, …) as the vocabulary. First pass is local LLM *inference* + a genre list, not fine-tuning on audio. Fine-tune later only if the label set needs it.

**Next session:** BlackHole + controllers.

---

## 2026-08-10 — Disable Cursor git co-author attribution

- Turned off Commit + PR attribution for local Agent:
  - IDE storage: `attributeCommitsToAgent=false`, `attributePRsToAgent=false`
  - CLI: `~/.cursor/cli-config.json` → `attribution.attributeCommitsToAgent/PRsToAgent: false`
- Project rule: `.cursor/rules/no-cursor-attribution.mdc` + note in `.cursorrules`
- Goal: future commits/PRs authored by David alone (no `Co-authored-by: Cursor` / `Made-with: Cursor`)
- UI cross-check: Cursor Settings → Git & PRs → Attribution (both off). Restart Cursor if toggles look stale.

---

## 2026-08-08 (evening wrap) — Traktor + Rekordbox day; user happy; call it

### Verdict

Huge day. Traktor library + stems tree are in good shape. Rekordbox XML bridge works (acapellas, From Traktor, Apple Music remaps). Sampler **audio** restored; sampler **pad banks** partially recovered via old `master.db` — still imperfect; **manual pad rebuild acceptable**. Apple Music Media left alone. **Stop here for the night.**

---

## Session timeline (what we did)

### A. Traktor NML (earlier → afternoon)

1. Hardened `update_nml_paths.py`
   - O(1) basename dict (avoids `[bracket]` glob blowups)
   - URL-decode + case-insensitive match
   - Removed per-file print spam; `--dry-run` + `--sample`
   - Initial remaps: **33,621** / unmatched **2,812**
2. Traktor analysis on ~22k tracks — **COMPLETE** (user confirmed)
3. Empty playlists diagnosed: COLLECTION remapped but playlist `PRIMARYKEY` still pointed at `~/Documents/Stems/...`
   - Stem keys use `TYPE=STEM` (not only `TRACK`) — **1,530** STEM keys
4. `fix_nml_playlists.py` → repaired **~1,476** keys (Stems 127/130, Xmas 236/239, April Fools 26/26, etc.)
5. `organize_stems.py --execute` → **3,872** files into `stems_audio/{Artist}/{Album}/`
6. Post-reorg: NML remap + playlist repair again
7. Staging cleanup `cleanup_staging.py`
   - Rescued **7** Unicode-only files → `_rescued_from_staging/`
   - Deleted `MIGRATED_ORPHANS/{Desktop,Documents,Downloads,Library}` (~**129GB → ~38MB**)
8. User verified crates/tree — **Traktor phase accepted**
9. GitHub bootstrap: https://github.com/ixamal/music_migration

### B. Rekordbox (evening)

1. **Parked** Apple Music / `Media.localized` reorg (path risk; do later)
2. `traktor_to_rekordbox.py` — **merge**, don’t replace
   - Base: Terrarum `rekordbox.xml` (preserve Sampler TRACK rows + old RB crates)
   - Fold in live Traktor paths (stems_audio + Apple Music remaps), cues/grids, playlists under **From Traktor**
   - Output: `~/Music/PioneerDJ/rekordbox.xml` — **23,004** tracks
   - Preserved **1,574** RB rows; updated **789**; added **21,430**; **33** Traktor playlists
3. Rekordbox 7 has **no** File → Import Collection
   - Use: Preferences → View → Layout → enable **rekordbox xml**
   - Advanced → Database → Imported Library → point at our XML
4. `heal_rekordbox_paths.py` — acapellas still pointed at `~/Documents/Stems…/acapella/`
   - Healed **602** paths by basename → stems_audio Artist/Album
   - Acapella (Spoken) **3→19/21**; Song **14→85/88**; Feb 2026 **17→131/144**
5. Sampler WAVs restored from Terrarum → `~/Music/PioneerDJ/Sampler/` (Capture **71**, OSC presets)
6. Pad banks stayed empty until old DB found
   - **Lesson:** `~/Music/rekordbox` = sample audio only
   - Pad map lives in `~/Library/Pioneer/rekordbox/master.db`
7. User copied old prefs to Terrarum:
   - `/Volumes/Terrarum/MIGRATION_MASTER/rekordbox_old_prefs/Library_Pioneer_rekordbox/` (**master.db 24MB**)
   - `.../Library_Application_Support_Pioneer_rekordbox/` (SamplerSettings, pads, MIDI)
8. Restored old `master.db` + companions into live `~/Library/Pioneer/rekordbox/`
   - Backup of prior live DB: `~/Music/PioneerDJ/rekordbox_library_backup_before_old_db/20260808_224131/`
   - SamplerSettings1.xml into `rekordbox6` (mostly OSC presets NOISE/SINE/SIREN/HORN)
9. User confirmed XML library usable (Acapella Spoken loading, analysis/cues visible). Sampler banks still not fully satisfying → **wrap for today; happy enough.**

---

## Lessons (keep)

- Always repair playlist `PRIMARYKEY`s (`TRACK` **and** `STEM`) after path remaps
- Quit Traktor / Rekordbox before writing their DBs/NML
- Dry-run before moves; keep basenames stable for filename-keyed remaps
- Rekordbox 7 XML = Preferences Imported Library, not File → Import Collection
- Merge RB XML (keep Sampler + old crates); then heal leftover Documents paths
- Sampler **files** ≠ sampler **slots**; slots need `Library/Pioneer/rekordbox/master.db`
- Never commit audio, NML, master.db, or giant JSON to git

---

## Key on-disk artifacts (not in git)

| Artifact | Path |
|----------|------|
| Healed merged XML | `~/Music/PioneerDJ/rekordbox.xml` |
| Master baseline XML | `~/Music/PioneerDJ/rekordbox.master_baseline.xml` |
| Sampler Capture | `~/Music/PioneerDJ/Sampler/Capture/` (71 wav) |
| Old prefs backup (Terrarum) | `/Volumes/Terrarum/MIGRATION_MASTER/rekordbox_old_prefs/` |
| Live DB backup before swap | `~/Music/PioneerDJ/rekordbox_library_backup_before_old_db/` |
| Stems tree | `~/Music/stems_audio/{Artist}/{Album}/` |
| Rescued stragglers | `~/Music/stems_audio/_rescued_from_staging/` |

---

## Next (another day)

1. Sampler pads: finish manually from Capture, or further dig old DB vs RB7 slot model
2. Fold `_rescued_from_staging` into Artist/Album; optional Traktor wrap
3. Apple Music Media cleanup (own project)
4. BlackHole + S88 MkII / S8 / DDJ-FLX10
5. Optional: commit more docs after sampler settled

---

## Safety rules

- Never move audio without `--dry-run` first
- Never commit audio, `collection.nml`, `master.db`, or giant catalog JSON
- Re-remap NML + playlist keys after any path-changing pass
- Backup live `~/Library/Pioneer/rekordbox/` before any DB swap
