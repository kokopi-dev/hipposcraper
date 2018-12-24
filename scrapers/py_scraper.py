#!/usr/bin/python2


""" Scrapes python project files """
def scrape_py(find_file_name):
    for li in find_file_name:
        text_file = li.next_sibling.text
        find_comma = text_file.find(",")
        # Handling multiple files
        if find_comma != -1:
            make_comma1 = open(text_file[:find_comma], "w+")
            make_comma2 = open(text_file[find_comma:].strip(", "), "w+")
            make_comma1.close()
            make_comma2.close()
        else:
            make_file = open(text_file, "w+")
            make_file.write("#!/usr/bin/python3")
            make_file.close()
