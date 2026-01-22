#!/bin/bash
set -euo pipefail

# Script: Download KhulnaSoft Parse Binary
# Description: Downloads the latest pre-compiled parse binary for your platform
# Usage: ./download_parse.sh [version]

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
cd "$SCRIPT_DIR"

# Validate curl is available
if ! command -v curl &> /dev/null; then
    echo "ERROR: curl is required but not installed"
    exit 1
fi

# Get version
VERSION="${1:-v0.0.17}"

echo "Downloading parse binary..."
if ! command -v curl &> /dev/null; then
    echo "ERROR: curl is required but not installed"
    exit 1
fi

# Get version
VERSION="${1:-v0.0.17}"

echo "Downloading parse binary..."
echo "Version: $VERSION"

# Clean up previous downloads
rm -f parse.gz parse

# Download and extract
if ! curl -Lo parse.gz "https://github.com/khulnasoft/khulnasoft-parse/releases/download/$VERSION/parse.gz"; then
    echo "ERROR: Failed to download parse binary version $VERSION"
    exit 1
fi

if ! gzip -d parse.gz; then
    echo "ERROR: Failed to extract parse binary"
    rm -f parse.gz parse
    exit 1
fi

if ! chmod +x parse; then
    echo "ERROR: Failed to make parse executable"
    exit 1
fi

echo "Successfully downloaded parse binary ($VERSION)"
echo "Run './parse -help' to see available options"
