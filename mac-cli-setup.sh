#!/bin/bash

# This script checks if Geneious Prime is installed and creates a symbolic link to the CLI tool for macOS

if [[ -d /Applications/Geneious\ Prime.app/Contents/Resources/app/resources/geneious ]]; then
    sudo ln -sf /Applications/Geneious\ Prime.app/Contents/Resources/app/resources/geneious /usr/local/bin
else
    echo "Geneious Prime not found"
fi
