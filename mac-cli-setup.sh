#!/bin/bash

# This script checks if Geneious Prime is installed and creates a symbolic link to the CLI tool for macOS

if [[ $(uname) != "Darwin" ]]; then
    echo "This script is only for macOS"
    exit 1
fi

if [[ -d /Applications/Geneious\ Prime.app ]] ; then
    echo "Creating symbolic link for Geneious CLI tool..."
    sudo ln -sf /Applications/Geneious\ Prime.app/Contents/Resources/app/resources/geneious /usr/local/bin
else
    echo "Geneious Prime not found"
fi
