# Roman Urdu + Alpaca QA Mix

A custom instruction-tuned dataset combining Roman Urdu QA pairs and English examples from the Alpaca dataset. This project supports low-resource fine-tuning for multilingual or domain-specific large language models.

## Project Structure

```

├── alpaca\_data/                  # Final and intermediate dataset files
├── batch\_files/                  # Raw GPT/OpenAI outputs
├── batch\_prepared/               # Preprocessed batches
├── input/                        # Initial input prompts
├── outputs/                      # Output logs or generated results
├── scripts/                      # All transformation and processing scripts
│   ├── alpaca\_converted\_data.py
│   ├── batch\_create\_openAI.py
│   ├── convert\_parquet\_to\_jsonl.py
│   ├── create\_instruction\_json.ipynb
│   ├── roman\_urdu\_alpaca\_mixed.py
│   └── splitter.py
├── .env                          # Environment config
├── .gitignore                    # Files to ignore in git
├── output\_to\_excel.ipynb         # Notebook to convert data to Excel
├── ReadMe.md
└── requirements.txt              # Python dependencies

````

## Key Scripts

* `roman_urdu_alpaca_mixed.py`
  Combines Roman Urdu and Alpaca data into one `.jsonl` file.

* `alpaca_converted_data.py`
  Converts structured GPT outputs to Alpaca-compatible format.

* `convert_parquet_to_jsonl.py`
  Extracts samples from Hugging Face Alpaca Parquet file.

* `splitter.py`
  Splits data into batches or formats for processing.

## Dataset Format

The final dataset is saved in:

```
alpaca_data/roman_urdu_QA_full_alpaca.jsonl
```

Each line is a JSON object like:

```json
{
  "instruction": "Translate this sentence to Roman Urdu",
  "input": "میرا نام احمد ہے۔",
  "output": "Mera naam Ahmed hai."
}
```

Fields:

* `instruction`: The instruction or question.
* `input`: Optional input context (may be empty).
* `output`: The answer or desired response.

## Purpose

This dataset aims to support:

* Fine-tuning multilingual language models
* Improving understanding of Roman Urdu by LLMs
* Instruction-based QA training

## Notes

* Roman Urdu data was derived from Urdu prompts using GPT-4.
* English samples were drawn from the Stanford Alpaca dataset.
* Data has been reviewed and formatted to follow Alpaca-style instruction tuning format.

