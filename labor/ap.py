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

# read the master data (ap.series)
series = pandas.read_csv(path.format("ap/ap.series"), sep='\t', skiprows=1,
                         names=["series_id", "area_code", "item_code", "footnote_codes", "begin_year",
                                "begin_period", "end_year", "end_period"] )

# not sure why i'm getting extra spaces, cleaning that up
series["item_code"] = series["item_code"].map(lambda x: str(x).strip())
series.set_index("series_id", inplace=True)

print series

# load areas
area = pandas.read_fwf(path.format("ap/ap.area"), widths=[4,100], names=["area_code", "area_name"], skiprows=2)
area.set_index("area_code", inplace=True)

print area

footnotes = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100], names=["footnote_code", "footnote_text"])
footnotes.set_index("footnote_code", inplace=True)

items = pandas.read_fwf(path.format("ap/ap.item"), widths=[7, 100], skiprows=2, names=["item_code", "item_name"])
items.set_index("item_code", inplace=True)


"""

File Name:  ap.period

Field #/Data Element		Length		Value(Example)

1. period			3		M01

2. period_abbr			5		JAN

3. period_name			20		Tex
"""

# items
