#!/usr/bin/python3
""" Test
"""
from models.engine.file_storage import FileStorage
from models.state import State
from inspect import isfunction


all_fct = FileStorage.__dict__.get("all")
if all_fct is None:
    print("Missing public instance method `all`")
    exit(1)

if not isfunction(all_fct):
    print("`all` is not a function")
    exit(1)

fs = FileStorage()
try:
    fs.all()
except:
    print("`all` is not a public instance method allowing no parameter")
    exit(1)

try:
    fs.all(State)
except:
    print("`all` is not a public instance method allowing a class parameter")
    exit(1)

print("OK", end="")
