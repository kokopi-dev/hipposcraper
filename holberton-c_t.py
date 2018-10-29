import sys

arg_len = len(sys.argv) - 1

pos = 1

while (arg_len >= pos):
        ctemp = open(sys.argv[pos], "w+")

        ctemp.write('#include "holberton.h"\n')
        ctemp.write("/**\n")
        ctemp.write(" * main - Entry Point\n")
        ctemp.write(" * Return: 0\n")
        ctemp.write(" */\n")
        ctemp.write("int main(void)\n")
        ctemp.write("{\n")
        ctemp.write("\n")
        ctemp.write("}")

        pos += 1
