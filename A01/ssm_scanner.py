# David Park
# dappark
# 109582425

import sys


def jumpError():
    sys.exit("Invalid/missing jump")


def argError():
    sys.exit("Invalid/missing argument")


def numError():
    sys.exit("Invalid numeric value")


def emptyStackError():
    sys.exit("Invalid operation on empty stack")


f = open(sys.argv[1], "r")
program = f.read().split()
f.close()

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
            else:
                numError()
        elif program[i + 1].isnumeric():
            stack.append(int(program[i + 1]))
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
        if stack.pop() == 0:
            if (program[i + 1] + ":") in program:
                i = program.index(program[i + 1] + ":")
            else:
                jumpError()
    elif program[i] == "jnz":
        if i == length - 1:
            argError()
        if stack.pop() != 0:
            if (program[i + 1] + ":") in program:
                i = program.index(program[i + 1] + ":")
            else:
                jumpError()
    elif program[i] == "jmp":
        if i == length - 1:
            argError()
        if (program[i + 1] + ":") in program:
            i = program.index(program[i + 1] + ":")
        else:
            jumpError()
    elif program[i] == "load":
        try:
            stack.append(store[stack.pop()])
        except:
            emptyStackError()
    elif program[i] == "store":
        try:
            value = stack.pop()
            addr = stack.pop()
        except:
            emptyStackError()
        store[addr] = value
    i += 1

try:
    print(stack.pop())
except:
    emptyStackError()
