import json
import redis
import datetime
from jobspy import scrape_jobs

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def make_json_serializable(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj

jobs = scrape_jobs(
    site_name=["linkedin", "indeed"],
    search_term="software engineer",
    location="San Francisco, CA",
    results_wanted=10,
    hours_old=72,
    country_indeed='USA',
)

for _, row in jobs.iterrows():
    job_dict = row.to_dict()
    job_json = json.dumps(job_dict, default=make_json_serializable)
    redis_client.rpush("job_queue", job_json)

print("Jobs added to Redis queue.")
