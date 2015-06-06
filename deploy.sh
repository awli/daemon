#!/bin/bash

cd ./app
echo "Installing app"
npm install
echo "Starting app..."
npm start &

cd ../griff
echo "Running python..."
python test.py
