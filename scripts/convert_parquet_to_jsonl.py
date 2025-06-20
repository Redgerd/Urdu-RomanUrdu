import pandas as pd
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

df = pd.read_parquet("hf://datasets/CohereLabs/aya_dataset/data/train-00000-of-00001.parquet")

logging.info(f"✅ Loaded total {len(df):,} records")

df = df[df["language"].str.lower() == "urdu"]
logging.info(f"✅ Filtered Urdu rows: {len(df):,}")

output_path = "./input/instruction.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as fout:
    for i, row in enumerate(df.itertuples(index=False)):
        fout.write(json.dumps({
            "inputs": row.inputs.strip(),
            "targets": row.targets.strip()
        }, ensure_ascii=False) + "\n")

        if (i + 1) % 5000 == 0:
            logging.info(f"📝 Written {i+1} rows")

logging.info(f"✅ Done! Final count: {len(df):,} rows → saved to {output_path}")