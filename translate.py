f = open("Code.gs", "rt")
code = f.read().split("\n")
f.close()


def GetIndent(string):
    indent = 0
    for char in string:
        if char == " ":
            indent += 1
        else:
            return int(indent / 4)


tab = "    "

fstring = ""
string = ""
indentreturns = []

indent = 0
lastindent = 0
else_ = False

for l in range(0, len(code)):
    line = code[l]
    indent = GetIndent(line)
    line = line.strip()
    if line.startswith("//"): continue
    if line == "":
        for i in range(l + 1, len(code)):
            if code[i].strip() != "":
                indent = GetIndent(code[i])
                break

    if line.startswith("else") or line.startswith("elif"): else_ = True

    if indent < lastindent:
        for i in range(0, lastindent - (indent + int(else_))):
            fstring += indentreturns.pop() + "\n"

    if else_: else_ = False

    if line.startswith("def"):
        if not line.endswith(":"):
            print("expected : at end of function definition (line " + str(code.index(line)) + ")")
            exit(1)

        fstring += line.split(" ")[1].split("(")[0] + " = function(" + line.split("(")[1][:-1]
        indentreturns.append("end function")

    elif line.startswith("for"):
        if line.endswith(":"):
            fstring += line[:-1]
            indentreturns.append("end for")
        else:
            fstring += line.split(":")[0] + "\n" + line.split(":")[1].strip() + "\n" + "end for"

    elif line.startswith("if"):
        if line.endswith(":"):
            fstring += line[:-1] + " then"
            indentreturns.append("end if")
        else:
            fstring += line.split(":")[0] + " then\n" + line.split(":")[1].strip()
            indentreturns.append("end if")

    elif line.startswith("elif"):
        if line.endswith(":"):
            fstring += "else if " + " ".join(line.split(" ")[1:])
        else:
            fstring += "else if " + " ".join(line.split(" ")[1:].split(":")[0]).strip() + "\n" + line.split(":")[1]

    elif line.startswith("else"):
        if line.endswith(":"):
            fstring += line[:-1]
            indent += 1
        else:
            fstring += line.split(":")[0] + "\n" + line.split(":")[1].strip()
            indent += 1

    else:
        fstring += line

    fstring += "\n"
    lastindent = indent


indent = 0
fstring = fstring.split("\n")

for l in range(0, len(fstring)):
    line = fstring[l]
    string += tab * indent

    if line.startswith("elif") or line.startswith("else"): string = string[:-4]

    elif line.startswith("end"):
        string = string[:-4]
        indent -= 1

    elif line.startswith("for") or line.startswith("if") or "function" in line: indent += 1

    string += line + "\n"

command = ""
for line in string.split("\n"):
    command += "echo " + line.strip() + "&"
command = command[:-1] + "| clip"

print(string)
