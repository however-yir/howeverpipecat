#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-however-yir}"
REPO="${2:-howeverpipecat}"
FULL="$OWNER/$REPO"

DESCRIPTION="howeverpipecat: real-time voice and multimodal agent engineering distribution"
HOMEPAGE="https://github.com/$FULL"

gh repo edit "$FULL" \
  --description "$DESCRIPTION" \
  --homepage "$HOMEPAGE" >/dev/null

gh api -X PUT "repos/$FULL/topics" \
  -H "Accept: application/vnd.github+json" \
  -f names[]="voice-agent" \
  -f names[]="multimodal" \
  -f names[]="webrtc" \
  -f names[]="python" \
  -f names[]="ollama" \
  -f names[]="realtime-ai" >/dev/null

echo "Updated repository metadata for $FULL"
