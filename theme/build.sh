#!/bin/bash

# Navigate to the theme directory
cd "$(dirname "$0")"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Build Tailwind CSS
echo "Building Tailwind CSS..."
npm run build

echo "Tailwind CSS build completed successfully!" 