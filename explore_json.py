import json
import glob

# find all the JSON files you saved yesterday
files = glob.glob("data/raw/*.json")
print("Files found:", len(files))

# open the first one
with open(files[0], encoding="utf-8") as f:
    data = json.load(f)

# top-level structure of the response
print("Top-level keys:", list(data.keys()))
print("Number of jobs in this file:", len(data["results"]))

# look at ONE job in full detail
print(json.dumps(data["results"][0], indent=2)[:1500])