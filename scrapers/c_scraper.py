#!/usr/bin/python2


def scrape_putchar(find_putchar, find_putchar_name):
    """Scrape for _putchar and either create or do not create."""
    # Find if page has _putchar
    if find_putchar is not None:
        find_putchar_name = find_putchar.next_sibling.text
    # Making _putchar
    if find_putchar_name == "_putchar" and find_putchar_name is not None:
        h_putchar = open("_putchar.c", "w+")
        h_putchar.write("#include <unistd.h>\n")
        h_putchar.write("\n")
        h_putchar.write("/**\n")
        h_putchar.write(" * _putchar - writes the character c to stdout\n")
        h_putchar.write(" * @c: The character to print\n")
        h_putchar.write(" *\n")
        h_putchar.write(" * Return: On success 1.\n")
        h_putchar.write(" * On error, -1 is returned, and errno")
        h_putchar.write(" is set appropriately.\n")
        h_putchar.write(" */\n")
        h_putchar.write("int _putchar(char c)\n")
        h_putchar.write("{\n")
        h_putchar.write("       return (write(1, &c, 1));\n")
        h_putchar.write("}")
        h_putchar.close()
        print("created.")
    else:
        print("not created.")


def scrape_c(find_file_name):
    """Scrape for C files."""
    for li in find_file_name:
        file_name = li.next_sibling.text
        try:
            store_file_name = open(file_name, "w+")
            store_file_name.write("#include <stdio.h>\n")
            store_file_name.write("#include <stdlib.h>\n")
            store_file_name.write("/**\n")
            store_file_name.write(" * main - Entry Point\n")
            store_file_name.write(" *\n")
            store_file_name.write(" * Return:\n")
            store_file_name.write(" */\n")
            store_file_name.write("int main(void)\n")
            store_file_name.write("{\n")
            store_file_name.write("\n")
            store_file_name.write("}")
            store_file_name.close()
        except:
            sys.stdout.write("Error: Could not create ")
            sys.stdout.write("task file %s\n" % file_name)
            sys.stdout.write("                   ... ")
            continue
