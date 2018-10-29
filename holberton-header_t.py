import sys

arg_len = len(sys.argv) - 1

pos = 1

while (arg_len >= pos):
	header = open(sys.argv[pos], "w+")

	header.write("#ifndef\n")
	header.write("#define\n")
	header.write("\n")
	header.write("#include <stdio.h>\n")
	header.write("#include <stdlib.h>\n")
	header.write("\n")
	header.write("#endif /* */")

	pos += 1
