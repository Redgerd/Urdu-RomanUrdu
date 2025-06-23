import os
import json

BATCH_DIR = "./batch_files"
PREPARED_DIR = "./batch_prepared"
os.makedirs(PREPARED_DIR, exist_ok=True)

def wrap_for_batch(file_path):
    output_filename = os.path.basename(file_path).replace(".jsonl", "_prepared.jsonl")
    output_path = os.path.join(PREPARED_DIR, output_filename)

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
   Map each Urdu character or combination to its nearest Roman‐Urdu equivalent:
     آ → aa      ا → a      ب → b      پ → p      ت → t  
     ٹ → ṭ      ث/س/ص → s   ج → j      چ → ch     ح → h  
     خ → kh     د → d      ڈ → ḍ      ذ/ز/ض/ظ → z   ر → r  
     ڑ → ṛ      ط/ت → t    ع → ’      غ → gh     ف → f  
     ق → q      ک → k      گ → g      ل → l      م → m  
     ن → n      و → w/o    ہ → h      ی → y/i     ے → e  
     کھ → kh     گھ → gh     بھ → bh     پھ → ph  

2. Structural Preservation
   – Keep the original word order, punctuation, spacing, and line breaks intact.  
   – Do not translate or interpret meaning—only convert script.  
   – Retain all commas, periods, dashes, and other symbols exactly.

3. Quality Assurance
   – Every Urdu word or phrase must have a Roman‐Urdu rendering.  
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
                    "custom_id": f"{os.path.basename(file_path)}_line_{idx}",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": "llama-3.1-8b-instant",
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
                print(f"❌ Error processing line {idx} in {file_path}: {e}")

    print(f"✅ Created batch file: {output_path}")
    return output_path

def process_all_files():
    for filename in os.listdir(BATCH_DIR):
        if not filename.endswith(".jsonl"):
            continue
        if filename.endswith("_prepared.jsonl"):
            continue

        source_path = os.path.join(BATCH_DIR, filename)
        wrap_for_batch(source_path)

if __name__ == "__main__":
    process_all_files()