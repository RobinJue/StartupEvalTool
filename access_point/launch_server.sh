#!/bin/bash

# Get the directory of this script
BASE_DIR=$(dirname "$0")
SERVER_SCRIPT="$BASE_DIR/server.py"

# Start the server and open the browser
python3 "$SERVER_SCRIPT" &
SERVER_PID=$!

echo "Server started. Opening browser..."
open "http://127.0.0.1:5000/"

# Function to cleanly stop the server
cleanup() {
    echo "Stopping the server..."
    kill $SERVER_PID
    wait $SERVER_PID
    echo "Server stopped."
}

# Trap both Ctrl+C and shell close events
trap cleanup EXIT

# Keep the script running to monitor
wait $SERVER_PID