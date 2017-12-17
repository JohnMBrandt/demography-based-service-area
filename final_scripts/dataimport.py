import pandas as pd
from sodapy import Socrata
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = Socrata("data.cityofnewyork.us", None)
results = client.get("fhrw-4uyv")
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("results.csv")

