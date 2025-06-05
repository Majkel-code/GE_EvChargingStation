#!/bin/bash

set -e

# ----------------------------------------
# Default installation paths
# ----------------------------------------
TARGET_HOME="/home/ge_run"
TARGET_DISPLAY="/home/ge_run/display"

# ----------------------------------------
# Ensure running as root
# ----------------------------------------
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script as root (e.g., with sudo)"
  exit 1
fi

# ----------------------------------------
# Create target directories if not present
# ----------------------------------------
echo "📁 Creating target directories $TARGET_HOME and $TARGET_DISPLAY..."
mkdir -p "$TARGET_HOME"
mkdir -p "$TARGET_DISPLAY"

# ----------------------------------------
# Install .deb packages
# ----------------------------------------
echo "📦 Installing .deb packages from ./res..."
for deb in ./res/*.deb; do
  echo "  ➜ Installing $(basename "$deb")"
  dpkg -i "$deb" || apt-get install -f -y
  echo "     ✔️ Installed"

  # if [[ "$deb" == *gui* ]]; then
  #   echo "📁 Installing display app into $TARGET_DISPLAY"
  #   cp "$deb" "$TARGET_DISPLAY/"
  # else
  #   echo "📁 Installing app into $TARGET_HOME"
  #   cp "$deb" "$TARGET_HOME/"
  # fi
done

DEFAULT_USER="gecharger"
echo "👤 Setting ownership of $TARGET_HOME and $TARGET_DISPLAY to $DEFAULT_USER:$DEFAULT_USER"
chown -R "$DEFAULT_USER:$DEFAULT_USER" "$TARGET_HOME"
chown -R "$DEFAULT_USER:$DEFAULT_USER" "$TARGET_DISPLAY"

# ----------------------------------------
# Done
# ----------------------------------------
echo "✅ Installation complete. Applications installed."

# ----------------------------------------
# Create and run systemd services
# ----------------------------------------
echo "⚙️ Setting up services..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bash "$SCRIPT_DIR/scripts/services.sh"
