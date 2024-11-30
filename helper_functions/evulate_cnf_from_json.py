import json
import random
from sympy import symbols, Or, And, Not as SymNot, sympify

# Logic gate functions
def OR(*inputs):
    return any(inputs)

def AND(*inputs):
    return all(inputs)

def NOT(input):
    return not input

# Evaluate graph representation with assignments
def evaluate_graph(graph, labels, assignments):
    evaluated = {}

    def evaluate_node(node, visiting=set()):
        if node in visiting:
            raise ValueError(f"Cycle detected in graph at node {node}")
        if node in evaluated:
            return evaluated[node]

        if node not in labels:
            raise KeyError(f"Label for node '{node}' is missing")
        
        visiting.add(node)
        label = labels[node]

        # Check if variable is in assignments
        if label == "VAR":
            if node in assignments:
                result = assignments[node]
            else:
                raise KeyError(f"Assignment for variable '{node}' is missing")
        elif label == "NOT":
            input_node = graph.get(node, [None])[0]
            if input_node is None:
                raise IndexError(f"Input node for 'NOT' operation at '{node}' is missing")
            result = NOT(evaluate_node(input_node, visiting))
        elif label == "OR":
            inputs = graph.get(node, [])
            if not inputs:
                raise IndexError(f"Inputs for 'OR' operation at '{node}' are missing")
            result = OR(*[evaluate_node(inp, visiting) for inp in inputs])
        elif label == "AND":
            inputs = graph.get(node, [])
            if not inputs:
                raise IndexError(f"Inputs for 'AND' operation at '{node}' are missing")
            result = AND(*[evaluate_node(inp, visiting) for inp in inputs])
        else:
            raise ValueError(f"Unknown label '{label}' for node '{node}'")

        evaluated[node] = result
        visiting.remove(node)
        return result

    try:
        return evaluate_node("AND_final")
    except Exception as e:
        # print(f"Evaluation error: {e}")
        return False

# Verify consistency of CNF expression and graph
def verify_consistency(cnf_expression_str, graph, labels, num_iterations=10):
    try:
        cnf_expression = sympify(cnf_expression_str.replace("~", "SymNot"))
    except Exception as e:
        print(f"Parsing error: {e}")
        return 0, 10  # Assume all evaluations fail if parsing fails

    variable_symbols = set(str(var) for var in cnf_expression.free_symbols)
    variables = [f"VAR_{var}" for var in variable_symbols]

    correct_count = 0

    for _ in range(num_iterations):
        assignments = {var: random.choice([True, False]) for var in variables}
        cnf_assignments = {symbols(var.split('_')[1]): assignments[var] for var in assignments}
        graph_assignments = {var: assignments[var] for var in assignments}

        cnf_result = cnf_expression.subs(cnf_assignments)
        try:
            graph_result = evaluate_graph(graph, labels, graph_assignments)
        except Exception as e:
            print(f"Error during evaluation: {e}")
            continue

        if cnf_result == graph_result:
            correct_count += 1

    return correct_count, num_iterations - correct_count

# Load CNF graph representations
with open("test_cnf_new_model3.json", "r") as file:
    cnf_graph_results = json.load(file)

# Initialize results
correct_results = []
wrong_results = []

# Evaluate each graph
for index, entry in cnf_graph_results.items():
    cnf_expression_str = entry["CNF_expression"]
    graph = entry["Graph Representation"]
    labels = entry["Node Labels"]

    # Perform 100 evaluations
    correct_count, incorrect_count = verify_consistency(cnf_expression_str, graph, labels)
    print(index)
    if correct_count == 10:
        correct_results.append({
            "cnf_expression": cnf_expression_str,
            "graph_representation": graph,
            "node_labels": labels
        })
    else:
        wrong_results.append({
            "cnf_expression": cnf_expression_str,
            "graph_representation": graph,
            "node_labels": labels,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count
        })

# Save results to JSON
output = {
    "correct_results": correct_results,
    "wrong_results": wrong_results,
    "statistics": {
        "total_graphs": len(cnf_graph_results),
        "correct_graphs": len(correct_results),
        "wrong_graphs": len(wrong_results)
    }
}

with open("Test_new_cnf_results.json", "w") as file:
    json.dump(output, file, indent=4)

print(f"Results saved to Test_new_cnf_results.json")
print(f"Correct graphs: {len(correct_results)}, Incorrect graphs: {len(wrong_results)}")
