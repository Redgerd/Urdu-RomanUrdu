import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BATCH_DIR = "../batch_files"

def create_batches():
    job_ids = []

    for i, filename in enumerate(os.listdir(BATCH_DIR)):
        path = os.path.join(BATCH_DIR, filename)
        print(f"📤 Uploading {filename}")
        upload = client.files.create(file=open(path, "rb"), purpose="batch")
        print(f"  ↪ File ID: {upload.id}")

        batch = client.batches.create(
            input_file_id=upload.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": f"urdu_roman_batch_{i}"}
        )
        print(f"✅ Batch Created: {batch.id}")
        job_ids.append(batch.id)

    return job_ids

if __name__ == "__main__":
    jobs = create_batches()
    print("🆗 All job IDs:")
    for job in jobs:
        print(job)
