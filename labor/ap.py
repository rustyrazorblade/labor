import os
import sys

from model import Model, path, parse_kv
from csv import reader
import re

import pandas

# area
"""
File Name:  ap.area
Field #/Data Element		Length		Value(Example)
1. area_code			4		A100
2. area_name			80		Text
"""

area = pandas.read_fwf(path.format("ap/ap.area"), widths=[4,100], names=["area_code", "area_name"], skiprows=2)
print area.head(2)

sys.exit()
for x in area.iterrows():
    print x
    break

footnote = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100])
items = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100])

items = parse_kv("ap/ap.item", 7)
# periods = parse_kv("ap/ap.period")


"""

File Name:  ap.period

Field #/Data Element		Length		Value(Example)

1. period			3		M01

2. period_abbr			5		JAN

3. period_name			20		Tex
"""

# items
