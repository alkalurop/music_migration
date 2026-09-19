# music_migration

Traktor / Rekordbox / Apple Music library migration tooling for [ixamal](https://github.com/ixamal) / [alkalurops.org](https://www.alkalurops.org).

**Vibe coding.** Cursor and Codex only. Git commits are David — no Cursor or Codex co-author trailers.

This repo tracks **scripts + docs only** — not the audio library. Local SSD paths and collection files stay on the machine / backup volume.

**Living log:** `docs/PROGRESS.md` + `git log` = lightweight Confluence (decisions, counts, gotchas).

## Layout

```
music_migration/          Python package (run as python3 -m …)
  traktor/                NML remap + playlist keys
  rekordbox/              XML merge/heal + Collection master.db
  apple_music/            Media.localized hoist + Music.app symlink
  stems/                  stems_audio organize + staging cleanup
config/                   JSON catalogs + move manifests (gitignored)
archive/                  one-shot helpers from the first migration day
docs/                     MASTER_CONTEXT + PROGRESS
```

## What this project does

1. Consolidate orphan / stem audio onto `~/Music/stems_audio`
2. Relink Traktor `collection.nml` to local SSD paths
3. Reorganize stems into `{Artist}/{Album}/{Track}.ext`
4. Repair playlist `PRIMARYKEY`s after moves (`TYPE=TRACK` + `TYPE=STEM`)
5. Bridge Traktor → Rekordbox XML (merge + path heal)
6. Restore / document Rekordbox sampler DB + Capture audio

**Canned 2026-08-20.** Performance rig (BlackHole + controllers) is **[ixamal/blackhole](https://github.com/ixamal/blackhole)**. Reopen this repo for remaps or MRBT retag.

## Docs

| Doc | Purpose |
|-----|---------|
| [`docs/MASTER_CONTEXT.md`](docs/MASTER_CONTEXT.md) | Architecture, paths, milestones, next tasks |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | Chronological session log |
| `git log` | Immutable checkpoint trail |

## Commands

From the repo root (`~/github/ixamal/music_migration`):

```bash
python3 -m music_migration                          # list commands

# Traktor (quit Traktor before --execute writes)
python3 -m music_migration.traktor.update_nml_paths --dry-run
python3 -m music_migration.traktor.fix_nml_playlists --dry-run

# Rekordbox (quit Rekordbox before Collection/XML writes)
python3 -m music_migration.rekordbox.traktor_to_rekordbox --dry-run
python3 -m music_migration.rekordbox.heal_rekordbox_paths --dry-run
python3 -m music_migration.rekordbox.relocate_rekordbox_collection --dry-run

# Apple Music (quit Music.app first)
python3 -m music_migration.apple_music.hoist_apple_music --dry-run
python3 -m music_migration.apple_music.fix_apple_music_library_paths --dry-run

# stems_audio
python3 -m music_migration.stems.organize_stems --dry-run
```

Destructive scripts default to dry-run; pass `--execute` to write.

Requires: Python 3.9+, `mutagen`, `tinytag`. Collection relocate also needs `pyrekordbox`.

Rekordbox 7: Preferences → View → Layout → enable **rekordbox xml**; Advanced → Database → Imported Library → `~/Music/PioneerDJ/rekordbox.xml`.

## Status (2026-08-20)

**Traktor:** Remapped after Apple Music hoist; playlists repaired.

**Rekordbox:** XML ~23k live after hoist heal; Collection `master.db` relocated **1,157** local files. Sampler pads still manual.

**Apple Music:** `Media.localized/{Artist}/{Album}/` hoist done; `Music/` symlink for library-db compat. Playback confirmed.

**Parked:** Sampler pads (by hand); MRBT genre retag via Ollama later.

**Next:** BlackHole + S88 MkII / S8 / DDJ-FLX10.

## Remote

- GitHub: https://github.com/ixamal/music_migration
- Profile: https://github.com/ixamal
