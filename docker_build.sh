#!/bin/bash

set -e

# -------------------------------
# Defaults
# -------------------------------
VERSION=""
BUILD_APPS=()
OUTPUT_DIR="./BUILDER"

# -------------------------------
# Functions
# -------------------------------

get_latest_git_tag() {
    if git describe --tags >/dev/null 2>&1; then
        git describe --tags --abbrev=0
    else
        echo "0.0.0"
    fi
}


print_usage() {
    echo "Usage: ./build.sh [--version x.y.z] [charger|vehicle|display]"
    echo "If no app is specified, all will be built."
}

# -------------------------------
# Parse Arguments
# -------------------------------

while [[ $# -gt 0 ]]; do
    case "$1" in
        --version)
            VERSION="$2"
            shift 2
            ;;
        charger|vehicle|display)
            BUILD_APPS+=("$1")
            shift
            ;;
        *)
            print_usage
            exit 1
            ;;
    esac
done

# -------------------------------
# Determine Version
# -------------------------------
if [[ -z "$VERSION" ]]; then
    VERSION=$(get_latest_git_tag)
    echo "ℹ️ Using Git tag version: $VERSION"
else
    echo "ℹ️ Using manual version override: $VERSION"
fi

RELEASE_NAME="ge_evchargingstation_${VERSION}"
RELEASE_DIR="$OUTPUT_DIR/$RELEASE_NAME"
DEB_DIR="$OUTPUT_DIR/res"
SCRIPT_DIR="$RELEASE_DIR/scripts"
TAR_PATH="$OUTPUT_DIR/${RELEASE_NAME}.tar.gz"

# If no apps specified, build all
if [[ ${#BUILD_APPS[@]} -eq 0 ]]; then
    BUILD_APPS=("charger" "vehicle" "display")
fi

# Clean old output
rm -rf "$OUTPUT_DIR"
mkdir -p "$DEB_DIR"
mkdir -p "$RELEASE_DIR"
mkdir -p "$SCRIPT_DIR"

# -------------------------------
# Build Selected Apps
# -------------------------------

for APP in "${BUILD_APPS[@]}"; do
    echo "🚧 Building $APP..."
    docker buildx build --platform linux/arm64 \
        --target build-$APP \
        --build-arg VERSION="$VERSION" \
        -t app-builder:$APP-$VERSION \
        --load .

    echo "📦 Extracting .deb for $APP..."
    case $APP in
        charger)
            docker run --rm -v "$(pwd)/$DEB_DIR:/output" --entrypoint "" app-builder:$APP-$VERSION \
                cp "/app/charger-app_${VERSION}_arm64.deb" /output/
            ;;
        vehicle)
            docker run --rm -v "$(pwd)/$DEB_DIR:/output" --entrypoint "" app-builder:$APP-$VERSION \
                cp "/app/vehicle-app_${VERSION}_arm64.deb" /output/
            ;;
        display)
            docker run --rm -v "$(pwd)/$DEB_DIR:/output" --entrypoint "" app-builder:$APP-$VERSION \
                sh -c 'cp /app/out/make/deb/arm64/*.deb /output/ge-evchargingstation-gui_'"${VERSION}"'_arm64.deb'
            ;;
    esac

    echo "🧹 Removing image for $APP..."
    docker image rm app-builder:$APP-$VERSION > /dev/null 2>&1 || true
done

# -------------------------------
# Assemble tar.gz Package
# -------------------------------

cp -r "$DEB_DIR" "$RELEASE_DIR/res"
cp ./.builders_cfg/scripts/install_temp.sh "$RELEASE_DIR/install.sh"
cp ./.builders_cfg/scripts/create_services.sh "$RELEASE_DIR/scripts/services.sh"
chmod +x "$RELEASE_DIR/install.sh"
chmod +x "$RELEASE_DIR/scripts/services.sh"

echo "📦 Creating archive: ${TAR_PATH}"
tar -czf "$TAR_PATH" -C "$OUTPUT_DIR" "$RELEASE_NAME"

echo "✅ Done. .deb files and release archive are in: $OUTPUT_DIR"

echo "🛠 Generating install.sh for Raspberry Pi..."
