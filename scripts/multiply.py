#!/usr/bin/env python3
import sys
import datetime

if len(sys.argv) != 3:
    sys.exit("usage: multiply <a> <b>")

a, b = map(float, sys.argv[1:])
print(datetime.datetime.now(datetime.UTC).isoformat())
print(a * b)

