import json
import os
from collections import defaultdict

# dataset paths
files = {
    "train": "../datasets/id-Layman-train-clean-org.json",
    "dev": "../datasets/id-Layman-dev-clean-org.json",
    "test": "../datasets/id-Layman-test-clean-org.json"
}

# store lawyers split-wise
split_lawyers = {}

# ---------------------------------------------
# PROCESS EACH SPLIT
# ---------------------------------------------

for split_name, file_path in files.items():

    print(f"\nProcessing {split_name} dataset...")

    # create split output folder
    split_output_dir = f"../outputs/{split_name}"
    os.makedirs(split_output_dir, exist_ok=True)

    # load dataset
    with open(file_path, "r") as f:
        data = json.load(f)

    # ---------------------------------------------
    # TASK 1
    # ---------------------------------------------

    unique_lawyers = set()

    # ---------------------------------------------
    # TASK 2
    # ---------------------------------------------

    category_to_lawyers = defaultdict(set)

    # ---------------------------------------------
    # TASK 3
    # lawyer -> category -> count
    # ---------------------------------------------

    lawyer_category_count = defaultdict(lambda: defaultdict(int))

    # ---------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------

    for item in data:

        category = item.get("query-category")

        responses = item.get("responses", [])

        for response in responses:

            lawyer = response.get("responder")

            if lawyer:

                unique_lawyers.add(lawyer)

                category_to_lawyers[category].add(lawyer)

                lawyer_category_count[lawyer][category] += 1

    # save split lawyers
    split_lawyers[split_name] = unique_lawyers

    # ---------------------------------------------
    # SAVE UNIQUE LAWYERS
    # ---------------------------------------------

    with open(f"{split_output_dir}/unique_lawyers.txt", "w") as f:

        f.write(f"Total Unique Lawyers: {len(unique_lawyers)}\n\n")

        for lawyer in sorted(unique_lawyers):
            f.write(lawyer + "\n")

    # ---------------------------------------------
    # SAVE CATEGORY -> LAWYERS
    # ---------------------------------------------

    with open(f"{split_output_dir}/category_to_lawyers.txt", "w") as f:

        for category, lawyers in sorted(category_to_lawyers.items()):

            f.write(f"{category}:\n")

            for lawyer in sorted(lawyers):
                f.write(f"   - {lawyer}\n")

            f.write("\n")

    # ---------------------------------------------
    # SAVE LAWYER -> CATEGORIES WITH COUNTS
    # ---------------------------------------------

    with open(f"{split_output_dir}/lawyer_to_categories.txt", "w") as f:

        for lawyer, categories in sorted(lawyer_category_count.items()):

            f.write(f"{lawyer}:\n")

            for category, count in sorted(categories.items()):

                f.write(f"   - {category} ({count})\n")

            f.write("\n")

    # ---------------------------------------------
    # SAVE ONLY 10+ CATEGORY COUNTS
    # ---------------------------------------------

    with open(f"{split_output_dir}/lawyers_with_10plus_categories.txt", "w") as f:

        for lawyer, categories in sorted(lawyer_category_count.items()):

            valid_categories = []

            for category, count in categories.items():

                if count >= 10:
                    valid_categories.append((category, count))

            if valid_categories:

                f.write(f"{lawyer}:\n")

                for category, count in sorted(valid_categories):

                    f.write(f"   - {category} ({count})\n")

                f.write("\n")

# ---------------------------------------------
# COMMON LAWYERS WITH TRAIN
# ---------------------------------------------

train_lawyers = split_lawyers["train"]

for split_name in ["dev", "test"]:

    common_lawyers = split_lawyers[split_name].intersection(train_lawyers)

    output_file = f"../outputs/{split_name}/common_with_train.txt"

    with open(output_file, "w") as f:

        f.write(f"Common Lawyers between TRAIN and {split_name.upper()}\n\n")

        f.write(f"Total Common Lawyers: {len(common_lawyers)}\n\n")

        for lawyer in sorted(common_lawyers):
            f.write(lawyer + "\n")

print("\nAll outputs generated successfully.")