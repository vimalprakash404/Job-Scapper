from fastapi import FastAPI
import redis
import json
import threading
import time

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def process_job(job_data: dict):
    """
    Define what to do with each job pulled from Redis.
    For now, just print.
    """
    print(f"Processed Job: {job_data['title']} at {job_data['company']}")


def consume_jobs():
    while True:
        job_json = redis_client.blpop("job_queue", timeout=5)
        if job_json:
            _, job_str = job_json
            job_data = json.loads(job_str)
            process_job(job_data)
        time.sleep(1)  # Throttle to prevent CPU hogging


@app.on_event("startup")
def start_consumer_thread():
    thread = threading.Thread(target=consume_jobs, daemon=True)
    thread.start()
    print("Started job consumer thread.")
