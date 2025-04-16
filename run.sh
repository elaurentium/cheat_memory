#!/bin/bash

BINARY="cheat" # COMPILED BINARY


if [ ! -f "$BINARY" ]; then
    make run
fi

echo "give root privileges..."
sudo chown root:root "$BINARY"

if [ $? -ne 0 ]; then
    echo "failed to give root privileges"
    exit 1
fi

echo "binary info:"
ls -l "$BINARY"