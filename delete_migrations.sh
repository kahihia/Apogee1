#!/bin/bash
find . -maxdepth 2 -name migrations | while read folder; do
    echo "Removing files from '$folder'"
    rm -r $folder/*
done