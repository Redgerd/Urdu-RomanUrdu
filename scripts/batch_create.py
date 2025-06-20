import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BATCH_DIR = "../batch_files"

def wrap_for_batch(file_path):
    output_path = file_path.replace(".jsonl", "_prepared.jsonl")

    with open(file_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for idx, line in enumerate(fin):
            try:
                data = json.loads(line)
                urdu_input = data.get("inputs", "").strip()
                urdu_target = data.get("targets", "").strip()

                prompt = (
                    "Translate the following Urdu sentences into Roman Urdu:\n\n"
                    f"Input: {urdu_input}\n"
                    f"Target: {urdu_target}"
                )

                request = {
                    "custom_id": f"{os.path.basename(file_path)}_line_{idx}",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": "gpt-3.5-turbo-0125",
                        "messages": [
                            {"role": "system", "content": "You are a translator that converts Urdu to Roman Urdu."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 300,
                        "temperature": 0.2
                    }
                }

                fout.write(json.dumps(request, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"❌ Error parsing line {idx}: {e}")

    return output_path

def create_batches():
    job_ids = []

    for i, filename in enumerate(os.listdir(BATCH_DIR)):
        if not filename.endswith(".jsonl") or "prepared" in filename:
            continue