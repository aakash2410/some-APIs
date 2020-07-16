# importing the necessary packages
from requests import exceptions
import argparse
import requests
import cv2
import os

# constructing the argument parser and parsing the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

x = open("BingKey1.txt", 'r')

API_KEY = x.read()
RESULT_LIMIT = 200
ONE_REQ_LIMIT = 50

#endpoint url

URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

#All the possible exceptions from request lib, and python in general

EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])


search_term = args['query']
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": search_term, "offset": 0, "count": ONE_REQ_LIMIT}


#making the search 

print("[INFO] Searching the Bing API for '{}'".format(search_term))
response = requests.get(URL, headers=headers, params=params)
response.raise_for_status()       #to debug
results = response.json()  #take response as a json object
estNumResults = min(results["totalEstimatedMatches"], RESULT_LIMIT) #to get least count
print("[INFO] {} total results for '{}'".format(estNumResults, search_term))

total_images = 0            #initialize counter to count images downloaded to print later

#loop over minimum no of results 
for offset in range(0, estNumResults, ONE_REQ_LIMIT):
	# update the search parameters using the current offset, then
	# make the request to fetch the results
	print("[INFO] making request for group {}-{} of {}...".format(
		offset, offset + ONE_REQ_LIMIT, estNumResults))
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}...".format(
		offset, offset + ONE_REQ_LIMIT, estNumResults))

#looping over the results to download them one by one
for v in results["value"]:
		# try to download the image
		try:
			# make a request to download the image
			print("[INFO] fetching: {}".format(v["contentUrl"]))
			r = requests.get(v["contentUrl"], timeout=30)
			# build the path to the output image
			ext = v["contentUrl"][v["contentUrl"].rfind("."):]
			p = os.path.sep.join([args["output"], "{}{}".format(str(total_images).zfill(8), ext)])
			# write the image to disk
			f = open(p, "wb")
			f.write(r.content)
			f.close()
		# catch any errors that would not unable us to download the image
		except Exception as e:
			# check to see if our exception is in our list of exceptions to check for
			if type(e) in EXCEPTIONS:
				print("[INFO] skipping: {}".format(v["contentUrl"]))
				continue 
		if cv2.imread(p) is None:       # if the image is `None` then we could not properly load the image from disk 
			print("[INFO] deleting: {}".format(p))
			os.remove(p)
			continue
		# update the counter
		total_images += 1

print(total_images)