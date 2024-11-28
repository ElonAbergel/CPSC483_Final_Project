import json
from sympy import symbols, Or, And, Not
import random
import openai
import ast


# Ask ChatGPT for the graph representation given a CNF expression
def chatgpt_api_to_graph(cnf_expression):
    openai.api_key = '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'
    prompt = f"""
    Given the following CNF expression: {cnf_expression}
    Please provide a response in this exact format:

    Graph Representation (Adjacency List):
    {{
        'VAR_x1': [],
        'VAR_x2': [],
        'VAR_x3': [],
        'OR_clause_0': ['VAR_x1'],
        'OR_clause_1': ['VAR_x1', 'VAR_x2', 'VAR_x3'],
        'AND_final': ['OR_clause_0', 'OR_clause_1']
    }}

    Node Labels:
    {{
        'VAR_x1': 'VAR',
        'VAR_x2': 'VAR',
        'OR_clause_0': 'OR',
        'AND_final': 'AND'
    }}

    Make sure to include both 'Graph Representation (Adjacency List):' and 'Node Labels:' sections in your response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred in API call: {e}")
        return None



# Parse the output from ChatGPT to extract the graph and labels
def parse_chatgpt_output(output):
    try:
        # Ensure both sections are in the output
        if "Graph Representation (Adjacency List):" not in output or "Node Labels:" not in output:
            raise ValueError("Expected sections 'Graph Representation' or 'Node Labels' not found in output.")
        
        # Split output into the graph and labels sections
        graph_str, labels_str = output.split("Node Labels:")
        
        # Further split to isolate the graph representation part
        graph = ast.literal_eval(graph_str.split("Graph Representation (Adjacency List):")[-1].strip())
        labels = ast.literal_eval(labels_str.strip())
        
        return graph, labels

    except ValueError as ve:
        print(f"Error parsing ChatGPT output: {ve}")
    except SyntaxError as se:
        print(f"Syntax error in ChatGPT output: {se}")
    except Exception as e:
        print(f"Unexpected error parsing ChatGPT output: {e}")
    
    # If parsing fails, return None for both graph and labels
    return None, None



# Load CNF expressions from random_cnf_expressions.json
with open("random_cnf_expressions.json", "r") as file:
    cnf_expressions = json.load(file)

# Dictionary to store results
results = {}

# counter
counter = 0 
# Process each CNF expression and get graph representation
for i, cnf_expression in cnf_expressions.items():
    output = chatgpt_api_to_graph(cnf_expression)
    print(counter)
    counter += 1
    if output:
        graph, labels = parse_chatgpt_output(output)
        if graph and labels:
            results[i] = {
                "CNF_expression": cnf_expression,
                "Graph Representation": graph,
                "Node Labels": labels
            }
        else:
            print(f"Failed to parse output for CNF {i}")
    else:
        print(f"No output received for CNF {i}")

# Save results to a JSON file
with open("cnf_graph_results.json", "w") as file:
    json.dump(results, file, indent=4)

print("Results saved to cnf_graph_results.json")