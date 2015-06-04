import os
import sys

from model import Model, path, get_cluster, get_session
from csv import reader
import re

import pandas
import ironeagle

# area
"""
File Name:  ap.area
Field #/Data Element		Length		Value(Example)
1. area_code			4		A100
2. area_name			80		Text
"""

session = get_session()
session.execute("CREATE TABLE IF NOT EXISTS average_price_data (area_code text primary key, area_name text)")

area = pandas.read_fwf(path.format("ap/ap.area"), widths=[4,100], names=["area_code", "area_name"], skiprows=2)

for i, row in area.iterrows():
    print row

# footnote = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100])
# items = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100])

# items = parse_kv("ap/ap.item", 7)
# periods = parse_kv("ap/ap.period")


"""

File Name:  ap.period

Field #/Data Element		Length		Value(Example)

1. period			3		M01

2. period_abbr			5		JAN

3. period_name			20		Tex
"""

# items
