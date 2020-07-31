from scraper import clean_data
import joblib
import pandas as pd 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="Input Username String")
args = vars(ap.parse_args())

model = joblib.load('instaspam.sav')
data = clean_data(args['query'])
data_df = pd.DataFrame(data)
print(model.predict(X = data_df))

