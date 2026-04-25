import os
import subprocess

user_input = input("Enter something: ")
eval(user_input)  # SECURITY ISSUE (Bandit)

def complex_example(x, y):
    if x > 10:
        if y > 5:
            if x + y > 20:
                print("Large")
            else:
                print("Medium")
        else:
            if x - y > 3:
                print("Small")
            else:
                print("Tiny")
    else:
        if x == 0:
            return 0
        elif x < 0:
            return -1
        else:
            return 1

def unused_function():
    temp = 5
    return temp

class Example:
    def __init__(self):
        if self.value > 10:  # access before definition
            print("Oops")

    def method(self):
        pass