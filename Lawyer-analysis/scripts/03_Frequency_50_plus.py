import json
import os
from collections import defaultdict

# dataset paths
files = {
    "train": "../datasets/id-Layman-train-clean-org.json",
    "dev": "../datasets/id-Layman-dev-clean-org.json",
    "test": "../datasets/id-Layman-test-clean-org.json"
}

# create output folder
os.makedirs("../outputs/frequency_analysis", exist_ok=True)

# ---------------------------------------------
# PROCESS EACH SPLIT
# ---------------------------------------------

for split_name, file_path in files.items():

    print(f"\nProcessing {split_name} dataset...")

    # lawyer -> category -> count
    lawyer_category_count = defaultdict(lambda: defaultdict(int))

    # load dataset
    with open(file_path, "r") as f:
        data = json.load(f)

    # ---------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------

    for item in data:

        category = item.get("query-category")

        responses = item.get("responses", [])

        for response in responses:

            lawyer = response.get("responder")

            if lawyer:

                lawyer_category_count[lawyer][category] += 1

    # ---------------------------------------------
    # SAVE OUTPUT
    # ---------------------------------------------

    output_path = f"../outputs/frequency_analysis/{split_name}_50plus.txt"

    with open(output_path, "w") as f:

        filtered_lawyers = []

        # first collect valid lawyers
        for lawyer, categories in sorted(lawyer_category_count.items()):

            valid_categories = []

            for category, count in categories.items():

                if count >= 50:
                    valid_categories.append((category, count))

            if valid_categories:
                filtered_lawyers.append((lawyer, valid_categories))

    # ---------------------------------------------
    # UNIQUE LAWYER COUNT
    # ---------------------------------------------

        total_filtered_lawyers = len(filtered_lawyers)

        print(f"Unique Lawyers with category count >= 50: {total_filtered_lawyers}")

        # write at top of file
        f.write(f"Unique Lawyers with category count >= 50: {total_filtered_lawyers}\n\n")

    # ---------------------------------------------
    # WRITE LAWYERS
    # ---------------------------------------------

        for lawyer, valid_categories in filtered_lawyers:

            f.write(f"{lawyer}:\n")

            for category, count in sorted(valid_categories):

                f.write(f"   - {category} ({count})\n")

            f.write("\n")

    print(f"Saved: {output_path}")

print("\nFrequency analysis completed.")