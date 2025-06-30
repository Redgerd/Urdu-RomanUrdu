import os
import json
import re

# === CONFIG ===
OUTPUT_JSONL_FILE = "outputs/batch_68621215e2048190873422e3d42b3261_output.jsonl"
ALPACA_OUTPUT_FILE = "alpaca_data/roman_urdu_QA_full_alpaca.jsonl"
os.makedirs(os.path.dirname(ALPACA_OUTPUT_FILE), exist_ok=True)


# === STEP 1: Robust Content Extractor ===
def get_response_content(entry, idx):
    try:
        return entry["response"]["body"]["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as e:
        print(f"❌ Skipping line {idx} — can't extract content: {e}")
        return None


# === STEP 2: Extract Question & Answer ===
def extract_qna(text):
    """
    Extracts question and answer from structured text.
    Returns (question, answer) or (None, None) if failed.
    """
    text = text.strip()

    q_match = re.search(r"\*\*Question_Text:\*\*\s*(.*?)(?=\*\*Answer_Text:\*\*|\Z)", text, re.DOTALL)
    a_match = re.search(r"\*\*Answer_Text:\*\*\s*(.*)", text, re.DOTALL)

    question = q_match.group(1).strip() if q_match else None
    answer = a_match.group(1).strip() if a_match else None

    return question, answer


# === STEP 3: Convert Entries to Alpaca Format ===
def convert_to_alpaca(input_path, output_path):
    skipped = 0
    written = 0

    with open(input_path, "r", encoding="utf-8") as fin:
        raw_data = [json.loads(line) for line in fin]

    with open(output_path, "w", encoding="utf-8") as fout:
        for idx, entry in enumerate(raw_data):
            content = get_response_content(entry, idx)
            if not content:
                skipped += 1
                continue

            question, answer = extract_qna(content)
            if not question or not answer:
                print(f"⚠️ Skipping line {idx}: Couldn't extract Question/Answer.")
                skipped += 1
                continue

            alpaca_item = {
                "instruction": question,
                "input": "",
                "output": answer,
                "text": f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{question}

### Input:


### Response:
{answer}"""
            }

            fout.write(json.dumps(alpaca_item, ensure_ascii=False) + "\n")
            written += 1

    print(f"\n✅ Finished. Wrote {written} Alpaca records to {output_path}")
    print(f"⚠️ Skipped {skipped} entries due to structure or content issues.")


# === ENTRYPOINT ===
if __name__ == "__main__":
    convert_to_alpaca(OUTPUT_JSONL_FILE, ALPACA_OUTPUT_FILE)
