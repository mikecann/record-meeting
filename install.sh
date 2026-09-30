#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.local/bin"

if [[ $# -gt 1 ]]; then
  echo "Usage: install.sh [target_bin_dir]" >&2
  exit 2
fi

case "${1:-}" in
  -h|--help)
    echo "Usage: install.sh [target_bin_dir]"
    echo "Symlink record-meeting into target_bin_dir (default: ~/.local/bin)."
    echo "Run bash setup_mac.sh to install dependencies and build the app."
    exit 0
    ;;
  -*)
    echo "install.sh: unknown option: $1 (try --help)" >&2
    exit 2
    ;;
  ?*) TARGET_DIR="$1" ;;
esac

mkdir -p "$TARGET_DIR"
chmod +x "$SCRIPT_DIR/record-meeting"
ln -sf "$SCRIPT_DIR/record-meeting" "$TARGET_DIR/record-meeting"
echo "Installed $TARGET_DIR/record-meeting -> $SCRIPT_DIR/record-meeting"
echo "Run bash \"$SCRIPT_DIR/setup_mac.sh\" to set up the native app."
echo "Re-run this installer if you move the clone."

case ":$PATH:" in
  *":$TARGET_DIR:"*) ;;
  *)
    echo "Add this to ~/.zshrc or ~/.bashrc if needed:"
    echo "  export PATH=\"$TARGET_DIR:\$PATH\""
    ;;
esac
