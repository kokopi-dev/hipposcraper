# Python Scripts for Automating Holberton Projects

---

## Required things

* sudo apt-get install pip
* pip install mechanize
* pip install beautifulsoup4

**NOTE: This program only works with python2, make sure your alias is 'python2'.**
* Mechanize is not supported by python3

---

## Description

Automating file template creation for Holberton projects, below is the chart of files that it will automate. The program will first ask you for your header file name, skip it by leaving it blank and pressing enter. Then it will ask if you want to include holberton's putchar file. Finally, it will then create a directory with the correct project name with all the project files in it.

| C Projects | Python Projects | Javascript |
| ------------- | ------------- | ------------- |
| C Templates | Py Templates | Coming Soon |
| Header file | C files | Coming Soon |
| Putchar file | Header files | Coming Soon |
| Main.c files | README.md |
| README.md |

## Instructions

**Install required things above**

**Setting User Information:** Enter in your Holberton intranet username and password as well as your Github name, username, and profile link in the [auth_data.json](./auth_data.json) file.

**Setting Alias:** Type cd in terminal, then open up '.bashrc' with your text editor. then enter in the alias corresponding with the ones that you want to use (alias name totally up to you if you want to change them).

Example of alias below file names in this readme.

---

### [Holberton Proj. All Scrapers](./project-all_scraper.py)
* alias hos='python2 /DIRECTORY/project-all_scraper.py'
* takes 1 argument: the project url
* it will scrape accordingly depending on which project type (c, python, js) it is

### [Holberton README.md Template](./holberton-read_t.py)
* alias hotr='python2 /DIRECTORY/holberton-read_t.py'
* takes 1 argument: the project url

### [Auth Data](./auth_data.json)
* Store your user/pass in here

---
## Example of the C scraper

![demo0](https://i.imgur.com/nIKUgA3.png)

## Example of the README scraper

![demo1](https://i.imgur.com/t6vOCwq.jpg)

## README Modifiying
* Go into the [holberton-read_t.py](./holberton-read_t.py) file to modify the README template to your own if you want
* The comment "README TEMPLATE BELOW" is where you can modify the .write functions
* "SCRAPERS and "EXTRA SCRAPES" are where you can use the variables ending with "_arr" to modify your README
* They are stored in lists, so you will need to loop through them to print them

---

## Author
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)

---

## Contributors
* **Brennan D Baraban** - [bdbaraban](https://github.com/bdbaraban)
