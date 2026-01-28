#!/bin/bash
# Create a new Solana dApp project

PROJECT_NAME=${1:-"my-solana-dapp"}

echo "Creating Solana dApp: $PROJECT_NAME"
npx create-solana-dapp@latest "$PROJECT_NAME" --template next-tailwind-counter

echo ""
echo "Project created! Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm install"
echo "  npm run anchor localnet  # Terminal 1"
echo "  npm run anchor build && npm run anchor deploy  # Terminal 2"
echo "  npm run dev  # Terminal 3"
