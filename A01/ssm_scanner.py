# David Park
# dappark
# 109582425

import sys
import re

# Return error on undefined jump location
def jumpError():
    sys.exit("Invalid/missing jump")


# Return error on missing argument to jump or stack operation
def argError():
    sys.exit("Invalid/missing argument")


# Return error on invalid integer
def numError():
    sys.exit("Invalid numeric value")


# Return error on attempted operation on empty stack
def emptyStackError():
    sys.exit("Invalid operation on empty stack")


# Return error on attempted operation on empty store
def emptyStoreError():
    sys.exit("Invalid operation on empty store")


# Return error on invalid label name
def labelError():
    sys.exit("Invalid label name")


# Return error on invalid use of reserved keyword
def reservedError():
    sys.exit("Invalid use of reserved keyword")


reserved = (
    "ildc",
    "iadd",
    "isub",
    "imul",
    "idiv",
    "imod",
    "pop",
    "dup",
    "swap",
    "jz",
    "jnz",
    "jmp",
    "load",
    "store",
)

# Read in file from command line
f = open(sys.argv[1], "r")
# Split input by line
program = f.read().splitlines()
f.close()

# Seperate labels from instructions
program = [line.replace(":", ": ") for line in program]
# Strip whitespace
program = [line.strip() for line in program]

# Remove comments starting with "#" and ending at newline
i = 0
while i < len(program):
    if "#" in program[i]:
        program[i] = program[i][: program[i].index("#")]
    i += 1
# Separate each line into own string
program = [word for line in program for word in line.split()]

program = tuple(program)
length = len(program)
i = 0
stack = []
store = {}

while i < length:
    if program[i] == "ildc":
        if i == length - 1:
            argError()
        if program[i + 1][0] == "-":
            if program[i + 1][1:].isnumeric():
                stack.append(int(program[i + 1]))
                i += 2
                continue
            else:
                numError()
        elif program[i + 1].isnumeric():
            stack.append(int(program[i + 1]))
            i += 2
            continue
        else:
            numError()
    elif program[i] == "iadd":
        try:
            stack.append(stack.pop() + stack.pop())
        except:
            emptyStackError()
    elif program[i] == "isub":
        try:
            a = stack.pop()
            b = stack.pop()
        except:
            emptyStackError()
        stack.append(b - a)
    elif program[i] == "imul":
        try:
            stack.append(stack.pop() * stack.pop())
        except:
            emptyStackError()
    elif program[i] == "idiv":
        try:
            a = stack.pop()
            b = stack.pop()
        except:
            emptyStackError()
        stack.append(b / a)
    elif program[i] == "imod":
        try:
            a = stack.pop()
            b = stack.pop()
        except:
            emptyStackError()
        stack.append(b % a)
    elif program[i] == "pop":
        try:
            stack.pop()
        except:
            emptyStackError()
    elif program[i] == "dup":
        try:
            stack.append(stack[-1])
        except:
            emptyStackError()
    elif program[i] == "swap":
        try:
            a = stack.pop()
            b = stack.pop()
        except:
            emptyStackError()
        stack.append(a)
        stack.append(b)
    elif program[i] == "jz":
        if i == length - 1:
            argError()
        try:
            if stack.pop() == 0:
                if (program[i + 1] + ":") in program:
                    i = program.index(program[i + 1] + ":")
                    i += 2
                    continue
                else:
                    jumpError()
        except:
            emptyStackError()
    elif program[i] == "jnz":
        if i == length - 1:
            argError()
        try:
            if stack.pop() != 0:
                if (program[i + 1] + ":") in program:
                    i = program.index(program[i + 1] + ":")
                    i += 2
                    continue
                else:
                    jumpError()
        except:
            emptyStackError()
    elif program[i] == "jmp":
        if i == length - 1:
            argError()
        if (program[i + 1] + ":") in program:
            i = program.index(program[i + 1] + ":")
            i += 2
            continue
        else:
            jumpError()
    elif program[i] == "load":
        try:
            addr = stack.pop()
        except:
            emptyStackError()
        try:
            stack.append(store[addr])
        except:
            emptyStoreError()
    elif program[i] == "store":
        try:
            value = stack.pop()
            addr = stack.pop()
            store[addr] = value
        except:
            emptyStackError()
    elif program[i].endswith(":"):
        if program[i][: program[i].index(":")] in reserved:
            reservedError()
        elif re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*:", program[i]):
            i += 1
            continue
        else:
            labelError()
    else:
        argError()
    i += 1

try:
    print(stack.pop())
except:
    print("")
