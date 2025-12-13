#!/bin/bash

ReeseOS Full Autostart

Launches Trinity, Store, Reader with PM2 using .env

BASE_DIR=~/KeystoneCreatorSuite
TRINITY_DIR=$BASE_DIR/trinity
STORE_DIR=$BASE_DIR/store
READER_DIR=$BASE_DIR/reader
LOG_DIR=$BASE_DIR/logs

Make sure logs exist

mkdir -p $LOG_DIR

Load environment variables safely

export $(grep -v '^#' $BASE_DIR/trinity/.env | xargs)

Function to start a PM2 app if not running

start_pm2_app() {
local dir=$1
local name=$2
local script=$3

if pm2 list | grep -q "$name"; then
    echo "🔹 $name already running. Resurrecting..."
    pm2 resurrect
else
    echo "🔹 Starting $name..."
    pm2 start "$dir/$script" \
        --name $name \
        --watch \
        --output $LOG_DIR/${name}_out.log \
        --error $LOG_DIR/${name}_err.log
fi

}

Start services

start_pm2_app $TRINITY_DIR "trinity" "index.js"
start_pm2_app $STORE_DIR "store" "index.js"
start_pm2_app $READER_DIR "reader" "index.js"

Save PM2 process list for persistence

pm2 save

echo "✅ ReeseOS Autostart: Trinity, Store, Reader launched and running!"
