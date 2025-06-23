import os
import json

# Point this at the folder containing batch_0.jsonl, batch_1.jsonl, etc.
BATCH_DIR = "./batch_files"

# Where to write the prepared JSONL files
PREPARED_DIR = "./batch_prepared"
os.makedirs(PREPARED_DIR, exist_ok=True)

def wrap_for_batch(file_path):
    basename = os.path.basename(file_path)
    output_path = os.path.join(
        PREPARED_DIR,
        basename.replace(".jsonl", "_prepared.jsonl")
    )

    with open(file_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin):
            try:
                data = json.loads(line)
                urdu_input = data.get("inputs", "").strip()

                prompt = f"""Instruction:
Transliterate the following Urdu text into Roman Urdu with precise phonetic accuracy and strict structural fidelity.

Guidelines:

1. Phonetic Mapping
   Map each Urdu character or combination to its nearest Roman-Urdu equivalent:
     آ → aa      ا → a      ب → b      پ → p      ت → t  
     ٹ → ṭ      ث/س/ص → s   ج → j      چ → ch     ح → h  
     خ → kh     د → d      ڈ → ḍ      ذ/ز/ض/ظ → z   ر → r  
     ڑ → ṛ      ط/ت → t    ع → ’      غ → gh     ف → f  
     ق → q      ک → k      گ → g      ل → l      م → m  
     ن → n      و → w/o    ہ → h      ی → y/i     ے → e  
     کھ → kh     گھ → gh     بھ → bh     پھ → ph  

2. Structural Preservation
   – Keep the original word order, punctuation, spacing, and line breaks intact.
   – Do not translate or interpret—only convert the script.
   – Retain all commas, periods, dashes, and other symbols.

3. Quality Assurance
   – Every Urdu word or phrase must have a Roman-Urdu rendering.
   – Do not introduce English words beyond the mapped phonetic equivalents.
   – Ensure readability and natural flow for Urdu speakers.
   – Do not merge, split, or omit any original components.

Forbidden:
   – Adding translations, explanations, or context.
   – Changing word order or punctuation.
   – Introducing terms not present in the source text.

Respond only with the transliterated text. Do not include any additional commentary or explanation.

Input:
{urdu_input}

Output:
"""

                request = {
                    "custom_id": f"{basename}_line_{idx}",
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
                print(f"❌ Error on line {idx} of {basename}: {e}")

    print(f"✅ Prepared: {output_path}")

def process_all_files():
    for fname in os.listdir(BATCH_DIR):
        if not fname.endswith(".jsonl") or fname.endswith("_prepared.jsonl"):
            continue
        wrap_for_batch(os.path.join(BATCH_DIR, fname))

if __name__ == "__main__":
    process_all_files()
