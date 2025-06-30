import pandas as pd
import json
import random

alpaca_parquet_path = "hf://datasets/tatsu-lab/alpaca/data/train-00000-of-00001-a09b74b3ef9c3b56.parquet"
alpaca_df = pd.read_parquet(alpaca_parquet_path, engine="pyarrow")
alpaca_subset = alpaca_df.sample(n=511, random_state=42)[["instruction", "input", "output"]]

roman_urdu_path = "alpaca_data/roman_urdu_QA_full_alpaca.jsonl"
roman_urdu_entries = []

with open(roman_urdu_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            roman_urdu_entries.append(obj)
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding line: {e}")

final_dataset = []

# Add Alpaca entries
for _, row in alpaca_subset.iterrows():
    entry = {
        "instruction": row["instruction"],
        "input": row["input"],
        "output": row["output"],
    }
    final_dataset.append(entry)

# Add Roman Urdu entries
for entry in roman_urdu_entries:
    if all(k in entry for k in ("instruction", "input", "output")):
        final_dataset.append(entry)
    else:
        print("⚠️ Skipping malformed Roman Urdu entry:", entry)

random.shuffle(final_dataset)

output_path = "alpaca_data/combined_roman_urdu_english.jsonl"

with open(output_path, "w", encoding="utf-8") as fout:
    for record in final_dataset:
        fout.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ Done! Mixed and wrote {len(final_dataset)} entries to {output_path}")