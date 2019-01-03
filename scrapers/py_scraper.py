#!/usr/bin/python2


""" Scrapes python project files """
def scrape_py(find_file_name, py_proto_tag):
    # Storing py prototypes into arr
    py_proto_arr = []
    for item in py_proto_tag:
        py_proto = item.next_sibling.text
        find_py = py_proto.find(":")
        # Stores only python prototypes
        if find_py != -1:
            py_proto_arr.append(py_proto)
        else:
            pass

    file_idx = 0
    for li in find_file_name:
        text_file = li.next_sibling.text
        find_comma = text_file.find(",")
        find_pyfile = text_file.find(".py")
        # Handling multiple files
        if find_comma != -1:
            make_comma1 = open(text_file[:find_comma], "w+")
            make_comma2 = open(text_file[find_comma:].strip(", "), "w+")
            make_comma1.close()
            make_comma2.close()
        else:
            make_file = open(text_file, "w+")
            make_file.write("#!/usr/bin/python3\n")
            # Creating prototypes in parallel with files
            if find_pyfile != -1:
                try:
                    make_file.write(py_proto_arr[file_idx])
                    file_idx += 1
                except IndexError:
                    pass
            else:
                pass
            make_file.close()
