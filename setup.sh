#!/usr/bin/env bash
# Initial variable setup for hipposcraper
# Run this to configure file paths and setup user information
project_alias="alias='python2 $(pwd)/hippoproject.py'"
read_alias="alias='python2 $(pwd)/hipporead.py'"
scrape_alias="alias='python2 $(pwd)/hipposcrape.sh'"
echo "Press Ctrl-C if you need to redo"
echo "What is your Holberton Email?"
read setup_user
echo "What is your Holberton Email's Password?"
read setup_pass
echo "What is your full name?"
read setup_name
echo "What is your github user name?"
read setup_github_name
echo "What is your github profile's link?"
read setup_github_link
echo "Type anything to continue, press Ctrl-C to redo something"
read confirmation

if grep -q YOUR_HOLBERTON_INTRANET_USERNAME auth_data.json
then
    sed -i "s/YOUR_HOLBERTON_INTRANET_USERNAME/$setup_user/g" auth_data.json
fi

if grep -q YOUR_HOLBERTON_INTRANET_PASSWORD auth_data.json
then
    sed -i "s/YOUR_HOLBERTON_INTRANET_PASSWORD/$setup_pass/g" auth_data.json
fi

if grep -q YOUR_NAME auth_data.json
then
    sed -i "s/YOUR_NAME/$setup_name/g" auth_data.json
fi

if grep -q YOUR_GITHUB_USERNAME auth_data.json
then
    sed -i "s/YOUR_GITHUB_USERNAME/$setup_github_name/g" auth_data.json
fi

if grep -q YOUR_GITHUB_PROFILE_LINK auth_data.json
then
    sed -i "s/YOUR_GITHUB_PROFILE_LINK/$setup_github_link/g" auth_data.json
fi

if grep -q Hipposcraper-alias ~/.bashrc
then
    :
else
    echo "# Hipposcraper-alias"
fi

if grep -q -i hippoproject.py ~/.bashrc
then
    :
else
    echo "$project_alias" >> ~/.bashrc
fi

if grep -q -i hipporead.py ~/.bashrc
then
    :
else
    echo "$read_alias" >> ~/.bashrc
fi

if grep -q -i hipposcrape.sh ~/.bashrc
then
    :
else
    echo "$scrape_alias" >> ~/.bashrc
fi
