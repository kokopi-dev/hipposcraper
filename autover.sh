#!/usr/bin/env bash
# This tool is for developing purposes
# Auto-updates version in 3 files

current=$(grep -oP "(?<=type=6&v=).*?(?=&x2=0)" README.md)
echo "Current version: $current"
echo "Enter the version number you want to update to:"
read -r version

echo "Updated README.md from $current to $version ..."
sed -i "s/$current/$version/g" README.md
echo "Updated hippoproject.py from $current to $version ..."
sed -i "s/$current/$version/g" hippoproject.py
echo "Updated hipporead.py from $current to $version ..."
sed -i "s/$current/$version/g" hipporead.py

echo "Completed."
