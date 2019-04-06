#!/usr/bin/env bash
# Sets up the hipposcraper:
#+  Configures aliases in .bashrc
#+  Sets inputted user information in auth.json

echo "Thanks for downloading the Hipposcraper! Let's get you set up."
echo -n "  -> Holberton Intranet email: "
read -r email
echo -n "  -> Holberton Intranet password: "
read -r password
echo -n "  -> Full name (for author section of README's): "
read -r name
echo -n "  -> Github username: "
read -r github_username
echo -n "  -> Github profile link: "
read -r github_link

if grep -q YOUR_HOLBERTON_INTRANET_USERNAME auth_data.json
then
    sed -i "s/YOUR_HOLBERTON_INTRANET_USERNAME/$email/g" auth_data.json
fi

if grep -q YOUR_HOLBERTON_INTRANET_PASSWORD auth_data.json
then
    sed -i "s/YOUR_HOLBERTON_INTRANET_PASSWORD/$password/g" auth_data.json
fi

if grep -q YOUR_NAME auth_data.json
then
    sed -i "s/YOUR_NAME/$name/g" auth_data.json
fi

if grep -q YOUR_GITHUB_USERNAME auth_data.json
then
    sed -i "s/YOUR_GITHUB_USERNAME/$github_username/g" auth_data.json
fi

if grep -q YOUR_GITHUB_PROFILE_LINK auth_data.json
then
  sed -i "s,YOUR_GITHUB_PROFILE_LINK,$github_link,g" auth_data.json
fi

echo "Setting aliases:"
if ! grep -q hippoproject ~/.bashrc || \
   ! grep -q hipporead  ~/.bashrc || \
   ! grep -q hipposcrape ~/.bashrc
then
  echo -e "\n# Hipposcraper aliases" >> ~/.bashrc
fi

if ! grep -q hippoproject.py ~/.bashrc
then
    project_alias="alias hippoproject='python2 $(pwd)/hippoproject.py'"
    echo "$project_alias" >> ~/.bashrc
    echo "  -> $project_alias"
else
  echo "  -> hippoproject already defined"
fi

if ! grep -q hipporead.py ~/.bashrc
then
  read_alias="alias hipporead='python2 $(pwd)/hipporead.py'"
  echo "$read_alias" >> ~/.bashrc
  echo "  -> $read_alias"
else
  echo "  -> hipporead already defined"
fi

if ! grep -q hipposcrape.sh ~/.bashrc
then
    scrape_alias="alias hipposcrape='python2 $(pwd)/hipposcrape.sh'"
    echo "$scrape_alias" >> ~/.bashrc
    echo "  -> $scrape_alias"
else
  echo "  -> hipposcrape already defined"
fi

echo "All set!"
