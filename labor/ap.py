import os
import sys

from model import Model, path, get_cluster, get_session
import re

import pandas
import ironeagle

from cassandra.cqlengine.columns import Text, Integer
from cassandra.cqlengine.management import sync_table

# area
"""
File Name:  ap.area
Field #/Data Element		Length		Value(Example)
1. area_code			4		A100
2. area_name			80		Text
"""
def run():
    session = get_session()
    class AveragePriceData(Model):
        # ['footnote_codes', 'item_name', 'end_year', 'area_name', 'begin_year', 'area_code', 'item_code', 'begin_period', 'end_period']
        series_id = Text(primary_key=True)
        footnote_codes = Text()
        item_name = Text()
        begin_year = Integer()
        end_year = Integer()
        area_name = Text()
        area_code = Text()
        item_code = Text()
        begin_period = Text()
        end_period = Text()

    sync_table(AveragePriceData)

    # read the master data (ap.series)
    series = pandas.read_csv(path.format("ap/ap.series"), sep='\t', skiprows=1,
                             names=["series_id", "area_code", "item_code", "footnote_codes", "begin_year",
                                    "begin_period", "end_year", "end_period"] )

    # not sure why i'm getting extra spaces, cleaning that up
    series["item_code"] = series["item_code"].map(lambda x: str(x).strip())
    series.set_index("series_id", inplace=True)

    # load areas
    area = pandas.read_fwf(path.format("ap/ap.area"), widths=[4,100], names=["area_code", "area_name"], skiprows=2)
    area.set_index("area_code", inplace=True)

    footnotes = pandas.read_fwf(path.format("ap/ap.footnote"), skiprows=1, widths=[1,100], names=["footnote_code", "footnote_text"])
    footnotes.set_index("footnote_code", inplace=True)

    items = pandas.read_fwf(path.format("ap/ap.item"), widths=[7, 100], skiprows=2, names=["item_code", "item_name"])
    items.set_index("item_code", inplace=True)

    result = series.join(area, on="area_code").join(items, on="item_code")
    print result.head(5)

    for k, v in result.iterrows():
        vals = v.to_dict()
        vals["series_id"] = k
        try:
            AveragePriceData.create(**vals)
        except Exception as e:
            print e
            print vals
            break
        print "Created {}".format(k)

if __name__ == "__main__":
    run()
