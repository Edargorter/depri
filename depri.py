#!/usr/bin/env python3
#DEbug PRInter Debug macro by Zachary Bowditch (Edargorter) 2020

import argparse
from shutil import copy2

__prog_name__ = "depri"
__author__ = "Zachary Bowditch (Edargorter)"

def _exit(msg, n):
    print(msg)
    exit(n)

#Language specific print function with single-line comment syntax
langs = {"C/C++": {"print": "printf(\"Debug: {}\\n\");", "comment": "//"},
        "Python": {"print": "print(\"Debug: {}\")", "comment": "#"},
        "JavaScript": {"print": "console.log(\"Debug: {}\\n\");", "comment": "//"},
        "Bash": {"print": "echo {}", "comment": "#"}
        }

file_extensions = {"cpp": "C/C++",
                    "c": "C/C++",
                    "py": "Python",
                    "js": "JavaScript"
                  }

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="DEbug PRInter - The Ultimate Printer for Debugging")
    parser.add_argument("-c", "--clear", help="Clear all debug print lines.", action="store_true", default=0)
    parser.add_argument("-p", "--pattern", metavar="pattern", type=str, help="The pattern string whose line is to be replaced by the print. Default: DEBUG", default="DEBUG")
    parser.add_argument("-s", "--statement", metavar="statement", type=str, help="The (print) statement to replace the line containing the pattern. E.g. printf('debug here\\n');")
    parser.add_argument("-b", "--backup", type=int, help="Turn backup on or off. Default: 1 = ON", choices=[0,1], default=1)
    parser.add_argument("filename", metavar="filename", type=str, help="the source file (with file extension). E.g. prog.cpp")

    error_count = 0
    args = parser.parse_args()

    filename = args.filename

    error_count += 1
    fe = filename.split(".")[-1]  #File extension

    if not fe:
        _exit("No file provided.", error_count)

    error_count += 1
    if fe not in file_extensions:
        _exit("File extension not supported.", error_count)

    error_count += 1

    #Make backup of file
    if args.backup:
        copy2(filename, filename + ".backup")

    try:
        f = open(filename, "r+")
    except Exception as e:
        _exit(e, error_count)

    replace_string = args.pattern
    lang = file_extensions[fe]

    print("File extension: {}".format(fe))
    print("Language detected: {}".format(lang))

    lines = f.readlines()
    f.close()

    #clearing debug prints
    if args.clear:  
        print("Clearing debug statements...")
        limit = len(lines)
        i = 0
        while i < limit:
            if replace_string in lines[i]:
                lines.pop(i)
                limit -= 1
            i += 1

    #inserting debug prints
    else:
        print("Inserting debug statements...")
        if args.statement:
            debug_string = args.statement[0]
            debug_comment = ""
        else:
            debug_string = langs[lang]["print"]
            debug_comment = langs[lang]["comment"]
        count = 0
        for i in range(len(lines)):

            line = lines[i].strip()
            space = len(lines[i]) - len(line) - 1 # -1 for newline character

            if replace_string in line:
                lines[i] = lines[i][:space] + debug_string.format(count) + " " + debug_comment + replace_string + '\n'
                count += 1

    try:
        f = open(filename, 'r+')
        f.truncate(0)
    except Expection as e:
        _exit(e, error_count)

    error_count += 1
    
    #Write back into file 
    for line in lines:
        f.write(line)

    f.close()

    print("Done.")
