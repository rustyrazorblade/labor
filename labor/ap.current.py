import os
import sys

from model import Model, path, get_cluster, get_session
import re

import pandas

from cassandra.cqlengine.columns import Text, Integer, Float
from cassandra.cqlengine.management import sync_table

"""
APU0000701111    	1995	M01	       0.238

The series_id (APU0000701111) can be broken out into:

Code                                    Value(Example)

survey abbreviation     =               AP
seasonal(code)          =               U
area_code               =               0000
item_code               =               701111



year                int64
period             object
value             float64
footnote_codes     object
area_code          object
item               object
period_abbr        object
period_name        object
item_name          object
area_name          object

"""

class AveragePriceDataCurrent(Model):
    series_id = Text(primary_key=True)
    year  = Integer(primary_key=True)
    period  = Text(primary_key=True)
    value  = Float()
    footnote_codes  = Text()
    area_code   = Text()
    item = Text()
    period_abbr  = Text()
    period_name  = Text()
    item_name = Text()
    area_name = Text()


def main():
    # session = get_session()
    sync_table(AveragePriceDataCurrent)


    # print series.head(5)
    # pull in the period
    periods = pandas.read_csv(path.format("ap/ap.period"), sep="\t")
    periods.set_index("period", inplace=True)

    # print periods.head(5)

    # get the items
    # print series.head(2)

    items = pandas.read_csv(path.format("ap/ap.item"), sep="\t")
    items["item_code"] = items["item_code"].map(lambda x: x.strip())

    # area
    areas = pandas.read_csv(path.format("ap/ap.area"), sep="\t")

    items.set_index("item_code", inplace=True)
    # series.set_index("series_id", inplace=True)
    areas.set_index("area_code", inplace=True)

    files = ["ap.data.0.Current", "ap.data.1.HouseholdFuels",
             "ap.data.2.Gasoline", "ap.data.3.Food"]

    for f in files:
        file = path.format("ap/") + f

        series = pandas.read_csv(file,
                                 skiprows=1, sep="\t",
                                 names=["series_id", "year", "period",
                                        "value", "footnote_codes"])

        series["area_code"] = series["series_id"].map(lambda x: x[3:7])
        series["item"] = series["series_id"].map(lambda x: x[7:13].strip())

        result = series.join(periods, on="period").join(items, on="item").\
                        join(areas, on="area_code")

        result["series_id"] = result["series_id"].map(lambda x: x.strip())
        result["area_name"]  = result["area_name"].fillna("")
        result["value"]  = result["value"].fillna(0)

        i = 0
        errors = 0
        print "Saving {}".format(file)
        for k, v in result.iterrows():
            i += 1
            vals = v.to_dict()

            try:
                AveragePriceDataCurrent.create(**vals)
            except Exception as e:
                errors += 1
                print e
                print "key: {}".format(k)
                print vals

        print "Total: {}".format(i)
        print "Errors: {}".format(errors)

if __name__ == "__main__":
    main()
