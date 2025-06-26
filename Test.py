import json
import redis
import datetime
from jobspy import scrape_jobs
import os
import asyncio
from Logger import Logger  # Ensure Logger.info and Logger.error are async functions
from dotenv import load_dotenv
os.environ["PYTHONHTTPSVERIFY"] = "0"

# Redis 
load_dotenv()  # Load .env variables
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
    username="default",
    password=os.environ.get("REDIS_PASSWORD", "password"),
)

# JSON serializer
def make_json_serializable(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj


# Input combinations
job_titles = ["journalism", "Backend Developer", "Frontend Developer"]
locations = ["Kerala"]

# Unique collections
unique_titles = []
unique_locations = []

logger = Logger()

async def main():
    for title in job_titles:
        for location in locations:
            
            await logger.info(f"🔍 Scraping jobs for '{title}' in '{location}'")

            try:
                jobs = scrape_jobs(
                    site_name=["linkedin" , "indeed"],
                    search_term=title,
                    google_search_term=f"{title} jobs near {location} since yesterday",
                    location=location,
                    results_wanted=50,
                    hours_old=240,
                    country_indeed="India",
                    # linkedin_fetch_description=True,
                )
                
                
                await logger.info(f"✅ Found {len(jobs)} jobs for '{title}' in '{location}'")

                for _, row in jobs.iterrows():
                    job_dict = row.to_dict()

                    found_title = job_dict.get("title")
                    
                    if found_title and found_title not in job_titles:
                        job_titles.append(found_title)
                        unique_titles.append(found_title)

                    await logger.info(f"🔍 Found job title: {found_title} on location : {location}  in company : {job_dict.get('company')}")
                    found_location = job_dict.get("location")
                    if found_location and found_location not in locations:
                        locations.append(found_location)
                        unique_locations.append(found_location)

                    job_dict["scraped_title"] = title
                    job_dict["scraped_location"] = location

                    job_json = json.dumps(job_dict, default=make_json_serializable)

                    try:
                        redis_client.rpush("job_queue", job_json)
                    except Exception as redis_err:
                        await logger.error(f"❌ Redis error for job '{job_dict.get('title')}': {redis_err}")

            except Exception as e:
                await logger.error(f"❌ Error scraping '{title}' in '{location}': {e}")
            
            await logger.info(f"⏳ Waiting 30 minutes before next combination...")
            await asyncio.sleep(1)  # 30 minutes

    await logger.info("✅ All jobs pushed to Redis queue.")
    await logger.info(f"📍 Unique Locations Found: {unique_locations}")
    await logger.info(f"💼 Unique Titles Found: {unique_titles}")


if __name__ == "__main__":
    asyncio.run(main())
