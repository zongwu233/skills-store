#!/bin/bash
# Post-installation hook for Skills Store Plugin
# This script runs after the plugin is installed

echo "🔧 Setting up Skills Store plugin..."

# Create plugin-skills directory if it doesn't exist
mkdir -p "plugin-skills"

echo "✅ Skills Store plugin setup complete!"
echo ""
echo "Quick start:"
echo "  /skills list          - List installed skills"
echo "  /skills search \"pdf\"   - Search for skills"
echo "  /skills install pdf   - Install a skill"
echo ""
echo "For more information, run: /skills"
