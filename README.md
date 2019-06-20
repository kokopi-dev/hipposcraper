![github version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=1.1.1&x2=0)
# Hipposcraper - Python Scripts for Automating Holberton Projects

### [STATUS] This repo is no longer maintained by [Derrick Gee](https://github.com/kai-dg) and [Brennan D Baraban](https://github.com/bdbaraban) starting 6/22/2019, please ask around or on the Holberton Slack to find someone who is maintaining a fork of this repo if you are looking for an updated version of this scraper.

<p align="center">
  <img src="http://www.holbertonschool.com/holberton-logo.png">
</p>

The Hipposcraper automates file template creation for Holberton projects. The 
program takes a link to a Holberton School project, scrapes the webpage, and 
creates the corresponding directory and files. The Hipposcraper currently supports 
the following: 

| System Engineering    | Low-Level Programming | Higher-Level Programming      |
| --------------------- | --------------------- | ----------------------------- |
| Bash script templates | `.c` templates        | `.py` and `.c` templates      |
|                       | Header file           | Header file                   |
|                       | `_putchar` file       |                               |
|                       | `main.c` test files   | `main.c`/`main.py` test files |
| `README.md`           | `README.md`           | `README.md`                   |

---

## Getting Started :wrench:

### IMPORTANT: Make sure your version is up to date (at the top of the readme), running hippoproject or hipporead will display the version.

Follow these instructions to set up the Hipposcraper on your machine.

### Prerequisites

The Hipposcraper relies on the Python packages Mechanize and BeautifulSoup4. 
Installation of these packages requires pip. If you are on a Debian-based Linux 
distribution:

```
sudo apt-get install pip
```

Once pip has been installed, install Mechanize and BeautifulSoup4 as follows:

```
pip install mechanize
pip install beautifulsoup4
```

Note that you may need to run the `--user` option when installing these packages.

### Setup :key:

**Setting User Information**

After cloning a local copy of the repository, enter your Holberton intranet 
username and password as well as your GitHub name, username, and profile link 
in the [auth_data.json](./auth_data.json) file.
  - **Using `setup.sh`: Run `./setup.sh` to automatically setup the required information**

**Setting Aliases**

The Hipposcraper defines two separate Python scripts - one 
([hippoproject.py](./hippoproject.py)) that creates projects, 
and a second ([hipporead.py](./hipporead.py)) that creates 
`README.md` files. To run both simultaneously, you'll need to define an alias 
to the script [hipposcrape.sh](./hipposcrape.sh).

First, open the script and enter the full pathname to the Hipposcraper 
directory where directed. Then, if you work in a Bash shell, define the 
following in your `.bashrc`:

```
alias hipposcrape='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hipposcrape.sh'
```

Alternatievely, you can define separate aliases for each individual script. To 
define a project scraper alias:

```
alias hippoproject='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hipposcraper.py'
```

And to define a `README.md` scraper alias:

```
alias hipporead='./ENTER_FULL_PATHNAME_TO_SCRAPER_DIRECTORY_HERE/hipporead.py'
```

*NOTE: This program only works with Python 2; ensure that your aliases 
specify 'python2' (Mechanize is not supported by Python 3).*

---

## Usage :computer:

After you have setup the proper aliases, you can run the Hipposcraper with the 
following command:

```
~$ hipposcrape project_link
```

Where `project_link` is the URL link to the Holberton School project to scrape.

Alternatively, to run only the project scraper:

```
~$ hippoproject project_link
```

Or only the `README.md` scraper:

```
~$ hipporead project_link
```

### `check.sh` - Generated for checking formats on all required files

```
~$ ./check.sh
```

## Repository Contents :file_folder:

* [hipposcraper.sh](./hipposcraper.sh)
  * A Bash script for running the entire Hipposcraper at once.

* [hippoproject.py](./hippoproject.py)
  * Python script that scrapes Holberton intranet webpage to create project 
directories.

* [hipporead.py](./hipporead.py)
  * Python script that scrapes Holberton intranet webpage to create project 
`README.md`.

* [auth_data.json](./auth_data.json)
  * Stores user Holberton intranet and GitHub profile information.

* [scrapers](./scrapers)
  * Folder of file-creation scrapers.
    * [base_parse.py](./scrapers/base_parse.py): Python script for parsing project pages.
    * [sys_scraper.py](./scrapers/sys_scraper.py): Python methods for creating 
Bash task files for system engineering projects.
    * [low_scraper.py](./scrapers/low_scraper.py): Python methods for creating 
`_putchar.c`, task files, and header file for low-level programming projects.
    * [high_scraper.py](./scrapers/high_scraper.py): Python methods for creating 
Python task files for higher-level programming projects.
    * [test_file_scraper.py](./scrapers/test_file_scraper.py): Python methods for creating 
test files for all project types.
* [setup.sh](./setup.sh): Sets up all variables and aliases with this script.
* [autover.sh](./autover.sh): Development tool for changing all version strings.
    
---

## Example of the C scraper

![demo0](https://i.imgur.com/oB08uzF.png)

## Example of the README scraper

![demo1](https://i.imgur.com/6qaC92l.jpg)

## Example of `check.sh`

![demo2](https://i.imgur.com/oQqTLWXh.jpg)

---

## Author
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)

---

## Contributors
* **Brennan D Baraban** - [bdbaraban](https://github.com/bdbaraban)
