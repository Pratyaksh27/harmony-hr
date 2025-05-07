#!/bin/bash

echo "🎯 Starting frontend..."
cd frontend || exit

# Start Vite dev server
npm install
npm run dev
