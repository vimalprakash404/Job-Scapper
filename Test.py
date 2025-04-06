import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["linkedin"],
    search_term="React",
    google_search_term="React",
    location="Kerala, India",
    results_wanted=1000,
    hours_old=24,  
    country_indeed='India',
    linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel