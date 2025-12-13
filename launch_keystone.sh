#!/bin/bash
pkill -f "node" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
npm run build
./node_modules/.bin/tailwindcss -i ./src/index.css -o ./build/static/css/output.css --minify --watch &
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
npx serve -s build -l 3000
