#!/usr/bin/python2
def scrape_tests(find_pre):
    """Create test files for Holberton School projects."""
    for pre in find_pre:
        find_main = pre.text.find("main.c")
        find_test = pre.text.find("cat")
        find_c = pre.text.find(".c")
        find_py = pre.text.find(".py")

        # find_main checks if there are main files on project page
        if find_main != -1:
            if find_test != -1 and (find_c != -1 or find_py != -1):
                name = pre.text.split("cat ", 1)[1]
                if find_c != -1:
                    name = name.split(".c", 1)[0] + ".c"
                else:
                    name = name.split(".py", 1)[0] + ".py"
                text = pre.text.split(name, 1)[1]
                text = text.split("\n", 1)[1]
                text = text.split("@ubuntu", 1)[0]
                text = text.split("\n")
                test_file = open(name, "w+")
                for i in range(len(text) - 1):
                    test_file.write(text[i] + "\n")
                test_file.close()
        else:
            pass
