#!/bin/bash

# Exit immediately if a command fails
set -e

echo "Starting Roman Urdu Batch Pipeline..."

# Step 1: Convert Parquet to JSONL
echo "Step 1: Converting Parquet → JSONL"
if python3 scripts/convert_parquet_to_jsonl.py; then
    echo "✅ Step 1 complete"
else
    echo "❌ Step 1 failed: Could not convert Parquet to JSONL"
    exit 1
fi

# Step 2: Split JSONL into batches of 500
echo "Step 2: Splitting JSONL into batches of 500"
if python3 scripts/splitter.py; then
    echo "✅ Step 2 complete"
else
    echo "❌ Step 2 failed: Could not split JSONL"
    exit 1
fi

# Step 3: Prepare for OpenAI batch API (simulate or real)
# echo "Step 3: Preparing batches for OpenAI API (simulated or real)"
# if python3 scripts/simulate_batches.py; then
#     echo "✅ Step 3 complete"
# else
#     echo "❌ Step 3 failed: Could not prepare or simulate batches"
#     exit 1
# fi

echo "Pipeline completed successfully!"
