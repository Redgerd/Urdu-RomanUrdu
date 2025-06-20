import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paste your job IDs here
job_ids = [
    # e.g., "batch_abc123..."
]

def monitor_jobs():
    done = set()
    while True:
        for job_id in job_ids:
            if job_id in done:
                continue

            batch = client.batches.retrieve(job_id)
            status = batch.status
            print(f"🔄 Job {job_id}: {status}")

            if status == "completed":
                done.add(job_id)
            elif status == "failed":
                print(f"❌ Job {job_id} failed: {batch.errors}")
                done.add(job_id)
            elif status == "in_progress":
                print(f"  ➤ {batch.request_counts.completed}/{batch.request_counts.total} done")

        if len(done) == len(job_ids):
            print("✅ All jobs finished.")
            break

        print("⏳ Sleeping for 15 minutes...")
        time.sleep(900)

if __name__ == "__main__":
    monitor_jobs()
