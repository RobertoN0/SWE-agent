#!/bin/bash
# Build custom Docker images for security experiments

set -e

echo "Building custom SWE-agent security experiment images..."
echo

# Build GPT image
echo "=== Building GPT image (with vision, no OCR) ==="
docker build -t swe-gpt-security:latest -f Dockerfile.gpt .
echo "✓ Built: swe-gpt-security:latest"
echo

# Build Ollama image
echo "=== Building Ollama image (with OCR for text-only model) ==="
docker build -t swe-ollama-security:latest -f Dockerfile.ollama .
echo "✓ Built: swe-ollama-security:latest"
echo

echo "=== Build complete! ==="
echo
echo "Images created:"
docker images | grep "swe-.*-security"
