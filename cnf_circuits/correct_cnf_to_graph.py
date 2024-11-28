import json
from sympy import symbols, sympify, Not as SymNot, Or

def cnf_to_graph(cnf_expression, variables):
    # Initialize graph and labels dictionaries
    graph = {}
    labels = {}
    node_counter = 0

    # Map each variable to a unique VAR node
    var_nodes = {str(var): f"VAR_{var}" for var in variables}
    for var, node in var_nodes.items():
        graph[node] = []
        labels[node] = "VAR"

    # Create OR clauses for each clause in the CNF expression
    clause_nodes = []
    for i, clause in enumerate(cnf_expression.args):
        clause_node = f"OR_clause_{i}"
        graph[clause_node] = []
        labels[clause_node] = "OR"
        clause_nodes.append(clause_node)

        # Process each literal in the clause
        for literal in clause.args if clause.func == Or else [clause]:
            if literal.func == SymNot:
                var_name = str(literal.args[0])
                not_node = f"NOT_{var_name}_{node_counter}"
                graph[not_node] = [var_nodes[var_name]]  # Connect NOT node to variable node
                labels[not_node] = "NOT"
                graph[clause_node].append(not_node)      # Connect clause node to NOT node
            else:
                var_name = str(literal)
                graph[clause_node].append(var_nodes[var_name])  # Connect clause to variable node
            node_counter += 1

    # Create the final AND node that connects all OR clauses
    and_node = "AND_final"
    graph[and_node] = clause_nodes
    labels[and_node] = "AND"

    return graph, labels

def process_cnf_expressions(input_filename, output_filename, max_entries=9102):
    # Load CNF expressions from the input JSON file
    with open(input_filename, "r") as file:
        cnf_data = json.load(file)

    # Dictionary to store the results
    processed_data = {}

    # Process each entry up to the specified max_entries
    for idx, (key, cnf_expression_str) in enumerate(cnf_data.items()):
        if idx >= max_entries:
            break

        try:
            # Convert the CNF expression string to a SymPy expression
            cnf_expression = sympify(cnf_expression_str.replace("~", "SymNot"))
            
            # Extract variables from the CNF expression
            variables = list(cnf_expression.free_symbols)
            
            # Generate graph and labels from the CNF expression
            graph, labels = cnf_to_graph(cnf_expression, variables)
            
            # Construct the final entry in the required format
            processed_data[key] = {
                "CNF_expression": cnf_expression_str,
                "Graph Representation": graph,
                "Node Labels": labels
            }
            
            # Print progress every 100 entries
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1} entries out of {max_entries}")

        except Exception as e:
            print(f"Error processing CNF expression with key {key}: {e}")

    # Save processed data to the output JSON file
    with open(output_filename, "w") as file:
        json.dump(processed_data, file, indent=4)
    print(f"Results saved to {output_filename}")

# Specify input and output file names
input_filename = "random_cnf_expressions.json"
output_filename = "cnf_graph_results.json"

# Process only the first 9102 CNF expressions
process_cnf_expressions(input_filename, output_filename, max_entries=9102)
