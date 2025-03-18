import json
import time
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, context_recall, answer_relevancy
from query import generate_answer  # Import function from query.py

# Load the golden dataset of test questions
with open("test_data/golden_set.json", "r", encoding="utf-8") as file:
    golden_set = json.load(file)

# Store queries and expected answers
queries = []
ground_truths = []
generated_answers = []

print("📊 Starting RAG evaluation...\n")

# Loop through each question
for item in golden_set:
    query = item["query"]
    expected_answer = item["ground_truth"]

    print(f"🔍 Evaluating: {query}")

    # Add a delay to prevent hitting API rate limits
    time.sleep(25)

    # Get answer from the RAG system
    generated_answer = generate_answer(query)

    # Append data for evaluation
    queries.append(query)
    ground_truths.append(expected_answer)
    generated_answers.append(generated_answer)

    print(f"✅ Completed: {query}\n")

# Evaluate with RAGAS (pass lists directly)
results = evaluate(
    queries=queries,
    ground_truths=ground_truths,
    predictions=generated_answers,
    metrics=[faithfulness, context_precision, context_recall, answer_relevancy]
)

# Save results to a JSON file
output_file = "evaluation_results.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(results.to_dict(), file, indent=4)

print("\n📊 **Evaluation Complete!** Results saved in `evaluation_results.json`.")
print(results)
