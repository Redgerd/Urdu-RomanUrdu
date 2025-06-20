import os
import json

INPUT_FILE = "./input/instruction.jsonl"
OUTPUT_DIR = "./batch_files"
BATCH_SIZE = 500

def split_jsonl_by_size():
    # Sanity check: Does input file exist?
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    # Sanity check: Is input file empty?
    if os.path.getsize(INPUT_FILE) == 0:
        print(f"❌ Input file is empty: {INPUT_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as infile:
        batch_num = 0
        current_batch = []
        total_lines = 0

        for idx, line in enumerate(infile):
            current_batch.append(line)
            total_lines += 1

            if len(current_batch) == BATCH_SIZE:
                batch_path = os.path.join(OUTPUT_DIR, f"batch_{batch_num}.jsonl")
                with open(batch_path, "w", encoding="utf-8") as fout:
                    fout.writelines(current_batch)
                print(f"✅ Wrote batch {batch_num} with {BATCH_SIZE} rows")
                batch_num += 1
                current_batch = []

        # Write the last partial batch if any
        if current_batch:
            batch_path = os.path.join(OUTPUT_DIR, f"batch_{batch_num}.jsonl")
            with open(batch_path, "w", encoding="utf-8") as fout:
                fout.writelines(current_batch)
            print(f"✅ Wrote final batch {batch_num} with {len(current_batch)} rows")

        print(f"Total lines processed: {total_lines}")
        print(f"Total batch files created: {batch_num + 1 if current_batch else batch_num}")

if __name__ == "__main__":
    split_jsonl_by_size()