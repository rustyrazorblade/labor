import os
print os.getcwd()

from model import Model, path
from csv import reader


# area
"""
File Name:  ap.area

Field #/Data Element		Length		Value(Example)

1. area_code			4		A100

2. area_name			80		Text
"""

area = dict()

import re

parser = re.compile("(.{4})(.*)")
with open(path.format("/ap/ap.area")) as fp:
    fp.next()
    fp.next()
    for x in fp:
        x = x.strip()
        matches = parser.match(x)
        area[matches.group(1)] = matches.group(2).strip()

print area

"""
File Name:  ap.footnote

Field #/Data Element		Length		Value(Example)

1. footnote_code		1		C

2. footnote_text		100		Text


File Name:  ap.item

Field #/Data Element		Length		Value(Example)

1. item_code			7		712211

2. item_name			100		Text


File Name:  ap.period

Field #/Data Element		Length		Value(Example)

1. period			3		M01

2. period_abbr			5		JAN

3. period_name			20		Tex
"""

# items
