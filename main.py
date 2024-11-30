import json
import sys
import os

# Ensure the current directory is included in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the evaluation function
from helper_functions.evulate_cnf_from_json import evaluate_cnf

def load_json(file_name):
    """
    Load a JSON file from the helper_functions folder.
    """
    with open(f'helper_functions/{file_name}', 'r') as file:
        return json.load(file)

def print_results(label, results):
    """
    Print the results in a formatted way.
    """
    print(f"\n{label} Results:")
    print(f"Total Graphs: {results['statistics']['total_graphs']}")
    print(f"Correct Graphs: {results['statistics']['correct_graphs']}")
    print(f"Wrong Graphs: {results['statistics']['wrong_graphs']}")

def main():
    # Load JSON files
    cnf_results_chatgpt = load_json("cnf_predictions_chatgpt.json")
    model1_results = load_json("test_cnf_new_model1.json")
    model2_results = load_json("test_cnf_new_model2.json")
    model3_results = load_json("test_cnf_new_model3.json")

    # Evaluate ChatGPT results
    print("Evaluating ChatGPT results...")
    results_chatgpt = evaluate_cnf(cnf_results_chatgpt)
    print_results("ChatGPT", results_chatgpt)

    # Evaluate models
    print("Evaluating Model 1...")
    results_model1 = evaluate_cnf(model1_results)
    print_results("Model 1", results_model1)

    print("Evaluating Model 2...")
    results_model2 = evaluate_cnf(model2_results)
    print_results("Model 2", results_model2)

    print("Evaluating Model 3...")
    results_model3 = evaluate_cnf(model3_results)
    print_results("Model 3", results_model3)

    print("\nPrinted all results from ChatGPT and my model 3 predictions !")

if __name__ == "__main__":
    main()
