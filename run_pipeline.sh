#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🚀 Starting Roman Urdu Batch Pipeline..."

# # Optional Step 1: Convert Parquet to JSONL
# echo "📦 Step 1: Converting Parquet → JSONL"
# if python3 scripts/convert_parquet_to_jsonl.py; then
#     echo "✅ Step 1 complete"
# else
#     echo "❌ Step 1 failed: Could not convert Parquet to JSONL"
#     exit 1
# fi

# # Optional Step 2: Split JSONL into batches of 500
# echo "✂️ Step 2: Splitting JSONL into batches of 500"
# if python3 scripts/splitter.py; then
#     echo "✅ Step 2 complete"
# else
#     echo "❌ Step 2 failed: Could not split JSONL"
#     exit 1
# fi

# Step 3: Send batches to Groq LLaMA Batch API
echo "📤 Step 3: Sending batches to LLaMA API (real or simulated)"
if python3 scripts/batch_create_openAI.py; then
    echo "✅ Step 3 complete"
else
    echo "❌ Step 3 failed: Sending or simulating batches failed"
    exit 1
fi

echo "🏁 Pipeline completed successfully!"
