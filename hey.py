from datetime import date
from pygooglenews import GoogleNews

gn = GoogleNews()
a = 1

from dbnomics import fetch_series

df1 = fetch_series("AMECO/ZUTN/EA19.1.0.0.0.ZUTN")

from pandas_datareader.fred import FredReader
from pandas_datareader.oecd import OECDReader

data = FredReader("CPGREN01CAM657N", start=date(1980, 1, 1))

OECDReader()
