# 1. Convert HF dataset to JSONL
python scripts/convert_parquet_to_jsonl.py

# 2. Split JSONL into batches of 500 examples
python scripts/splitter.py

# 3. Prepare and submit batch jobs to OpenAI
python scripts/batch_create.py
