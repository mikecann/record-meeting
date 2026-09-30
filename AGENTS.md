# Agent guidance for record-meeting

This is a standalone macOS 15+ meeting recorder. The native SwiftUI app uses
ScreenCaptureKit and AVFoundation. Its bundled Python processor uses ffmpeg,
faster-whisper and pyannote.audio for audio export, transcription and speaker
detection. Notion publishing is optional.

## Working on this repo

- Keep source files in this clone. `install.sh` only symlinks the launcher into
  `~/.local/bin` (or a supplied directory). Re-run it after moving the clone.
- Use test-first development for non-trivial changes. If there is no clean
  test seam, extract one before adding the test.
- When behaviour, UI copy, layout, persistence or startup changes, update
  affected tests and rerun them after implementing the change.
- Test before committing. Check exit codes, then verify the actual app when
  the change affects recording or playback.
- Do not commit app bundles, build output, Python environments, model downloads,
  recordings or tokens.
- Avoid eyebrows and kickers in UI designs. Keep user-facing copy plain and
  conversational, without em dashes or en dashes.
- Start PR descriptions with `## Why`, explaining what prompted the change.

## Development and verification

```bash
swift test
python3 -m unittest discover -s tests -p 'test_*.py' -v
bash restart.sh
```

`setup_mac.sh` creates the Python environment under
`~/Library/Application Support/Record Meeting/venv` and calls `build-app.sh`.
The app is staged at `~/Applications/Record Meeting.app`. `restart.sh` stops
the old instance, builds a debug bundle, signs it and opens it. Use that bundle
for manual checks so macOS associates privacy permissions with the app.

- Keep shell scripts compatible with macOS Bash 3.2, including empty arrays
  under `set -u` in the signing script.
- Keep the existing bundle ID and Keychain service so rebuilds retain
  settings, tokens and privacy permissions. Tokens belong in Preferences and
  macOS Keychain; this app does not load `.env` files.
- Unit tests must run without model downloads, API secrets, microphone access
  or screen recording permission. Notion tests use a mock transport.
- Recording changes need a real microphone and system audio test with
  headphones, followed by playback and synchronized transcript review. Test
  Notion publishing separately with an integration and a shared parent page.
- Preserve the temporary capture on processing failure for recovery. Remove
  it only after the MP3 and transcript JSON have been written safely.

## Main files

- `Sources/RecordMeetingApp/`: native app, recording, review, settings and Notion.
- `record_meeting_processor.py`: bundled transcription and speaker detection.
- `tests/RecordMeetingAppTests/`: Swift tests.
- `tests/test_*.py`: dependency-free Python tests and installer checks.
- `Resources/Info.plist`: bundle identity and permission descriptions.
- `record-meeting`: launcher with start, restart, stop and setup commands.
- `install.sh`: launcher installation only; run `setup_mac.sh` for dependencies
  and the signed native app.
