import os
import json

BATCH_DIR = "./batch_files"
PREPARED_DIR = "./batch_prepared"
os.makedirs(PREPARED_DIR, exist_ok=True)

def sanitize_custom_id(text):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in text)

def wrap_for_batch(file_path):
    basename = os.path.basename(file_path)
    safe_basename = sanitize_custom_id(basename)
    output_path = os.path.join(PREPARED_DIR, basename.replace(".jsonl", "_prepared.jsonl"))

    with open(file_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin):
            line = line.strip()

            # Skip empty lines
            if not line:
                print(f"⚠️  Skipping empty line {idx} in {basename}")
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError as err:
                print(f"❌ JSON decode error on line {idx} in {basename}: {err}")
                print("↳ Content:", repr(line))
                continue

            urdu_input = str(data.get("inputs", "")).strip()
            if not urdu_input:
                print(f"⚠️  Skipping line {idx} in {basename}: 'inputs' is missing or empty")
                continue

            # Escape dangerous chars
            urdu_input = urdu_input.replace("\r", "").replace("\n", " ").replace('"', '\\"')

            prompt_template = """Transliterate the following Urdu text into Roman Urdu with precise phonetic accuracy and strict structural fidelity.
Guidelines:
1. Name and Word Recognition Priority
*FIRST*: Identify and preserve well-known names and common English-origin words in their standard English spelling:
* *Proper names*: Elon Musk, Donald Trump, Facebook, Google, Microsoft, etc.
* *Common tech/modern terms*: robot(s), computer, internet, mobile, etc.
* *International terms*: university, hospital, hotel, etc.
* *Brand names*: Toyota, Samsung, Apple, etc.
*Recognition patterns*: If an Urdu word phonetically matches a well-known English name/term, use the standard English spelling instead of literal transliteration.
2. Phonetic Mapping (for non-English words)
Map each Urdu character or combination to its nearest Roman-Urdu equivalent:

آ → aa    ا → a     ب → b     پ → p     ت → t    
ٹ → ṭ     ث/س/ص → s  ج → j     چ → ch    ح → h    
خ → kh    د → d     ڈ → ḍ     ذ/ز/ض/ظ → z  ر → r    
ڑ → ṛ     ط/ت → t    ع → '     غ → gh    ف → f    
ق → q     ک → k     گ → g     ل → l     م → m    
ن → n     و → w/o   ہ → h     ی → y/i   ے → e    
کھ → kh   گھ → gh   بھ → bh   پھ → ph   

3. Structural Preservation
* Keep the original word order, punctuation, spacing, and line breaks intact
* Retain all commas, periods, dashes, and other symbols
* Do not merge, split, or omit any original components
4. Decision Process
For each word, ask:
1. Is this a well-known proper name? → Use standard English spelling
2. Is this a common English-origin word? → Use standard English spelling
3. Is this a technical/modern term with standard English equivalent? → Use English spelling
4. Otherwise → Apply phonetic transliteration rules
5. Quality Assurance
* Every Urdu word or phrase must have a Roman-Urdu rendering
* Prioritize recognizability for common names and terms
* Ensure readability and natural flow for Urdu speakers
* Maintain phonetic accuracy for native Urdu words
Forbidden:
* Adding translations, explanations, or context
* Changing word order or punctuation
* Introducing terms not present in the source text
* Over-transliterating obvious English names/terms
Examples:
* ایلون مسک → Elon Musk (not "ailwn msk")
* روبوٹس → robots (not "robwṭs")
* کمپیوٹر → computer (not "kmpyuṭr")
* فیس بک → Facebook (not "fys bk")
*Respond only with the transliterated text. Do not include any additional commentary or explanation.*
**Input:**
{urdu}

**Output:"""

            prompt = prompt_template.replace("{urdu}", urdu_input)

            request = {
                "custom_id": f"{safe_basename}_line_{idx}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4.1-2025-04-14",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a translator that converts Urdu to Roman Urdu."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 300,
                    "temperature": 0.2
                }
            }

            try:
                json_line = json.dumps(request, ensure_ascii=False)
                fout.write(json_line + "\n")
            except Exception as json_err:
                print(f"❌ JSON dump error on line {idx} of {basename}: {json_err}")
                print("↳ Request that failed:", repr(request))

    print(f"✅ Prepared: {output_path}")

def process_all_files():
    for fname in os.listdir(BATCH_DIR):
        if fname.endswith(".jsonl") and not fname.endswith("_prepared.jsonl"):
            wrap_for_batch(os.path.join(BATCH_DIR, fname))

if __name__ == "__main__":
    process_all_files()