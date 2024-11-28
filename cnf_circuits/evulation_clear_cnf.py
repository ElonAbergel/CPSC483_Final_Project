import re
import random

def parse_cnf_expression(cnf_expression):
    # Split the CNF into clauses
    cnf_expression = cnf_expression.replace("(", "").replace(")", "")
    clauses = [clause.strip().split(" OR ") for clause in cnf_expression.split(" AND ")]
    return clauses

def extract_variables(cnf_expression):
    # Extract all variables (without NOT) from the CNF expression
    variables = set(re.findall(r'\bx\d+\b', cnf_expression))
    return variables

def generate_random_assignment(variables):
    # Generate a random assignment (True/False) for each variable
    return {var: random.choice([True, False]) for var in variables}

def evaluate_clause(clause, assignment):
    # Evaluate a single clause by checking if any literal in the clause is True
    for literal in clause:
        if literal.startswith("NOT "):
            var = literal[4:]  # remove "NOT " to get the variable name
            if not assignment.get(var, False):  # if NOT(var) is True
                return True
        else:
            var = literal
            if assignment.get(var, False):  # if var is True
                return True
    return False  # clause is False if no literal is True

def evaluate_cnf_expression(cnf_expression):
    # Parse the CNF expression into clauses
    clauses = parse_cnf_expression(cnf_expression)
    variables = extract_variables(cnf_expression)
    assignment = generate_random_assignment(variables)

    # Evaluate each clause; if any clause is False, the whole CNF is False
    for clause in clauses:
        if not evaluate_clause(clause, assignment):
            return False, assignment  # return False if any clause is unsatisfied
    return True, assignment  # CNF is True if all clauses are satisfied

def evaluate_circuit(adjacency_list, labels, assignment):
    # A helper function to evaluate a node recursively
    def evaluate_node(node, evaluated):
        # If the node is already evaluated, return its value
        if node in evaluated:
            return evaluated[node]
        
        # Get the label for this node
        label = labels[node]
        
        # Evaluate based on the label type
        if label == "VAR":
            # Return the assignment for this variable
            value = assignment[node]
        
        elif label == "NOT":
            # NOT operation - invert the value of the single input node
            input_node = adjacency_list[node][0]
            value = not evaluate_node(input_node, evaluated)
        
        elif label == "OR":
            # OR operation - True if any input node is True
            value = any(evaluate_node(input_node, evaluated) for input_node in adjacency_list[node])
        
        elif label == "AND":
            # AND operation - True if all input nodes are True
            value = all(evaluate_node(input_node, evaluated) for input_node in adjacency_list[node])
        
        # Store the evaluated result to avoid redundant calculations
        evaluated[node] = value
        return value

    # Dictionary to store evaluated nodes to avoid recomputation
    evaluated = {}
    
    # Start evaluation from the final output node ("AND_final")
    final_result = evaluate_node("AND_final", evaluated)
    return final_result

def verify_circuit_consistency(cnf_expression, adjacency_list, labels, num_iterations=5):
    for _ in range(num_iterations):
        # Evaluate the CNF expression
        cnf_result, assignment = evaluate_cnf_expression(cnf_expression)
        
        # Prepare the assignment for the circuit with variable names prefixed by "VAR_"
        circuit_assignment = {f"VAR_{var}": value for var, value in assignment.items()}
        
        # Evaluate the circuit
        circuit_result = evaluate_circuit(adjacency_list, labels, circuit_assignment)
        
        # Check if the circuit result matches the CNF result
        if cnf_result != circuit_result:
            print("Mismatch found! The circuit does NOT correctly represent the CNF.")
            return False
    
    # If all iterations matched, the circuit is consistent with the CNF
    print("The circuit correctly represents the CNF across all iterations.")
    return True

# Define the CNF and corrected circuit representation
cnf_expression = "(NOT x3 OR NOT x4 OR x4) AND (x2 OR x1 OR x2) AND (x4 OR NOT x4 OR NOT x4)"
adjacency_list = {
    "VAR_x3": ["OR_clause1"],
    "NOT_x4_clause1": ["OR_clause1"],
    "VAR_x4_clause1": ["OR_clause1"],
    
    "VAR_x2_clause2": ["OR_clause2"],
    "VAR_x1": ["OR_clause2"],

    "VAR_x4_clause3": ["OR_clause3"],
    "NOT_x4_clause3_1": ["OR_clause3"],
    "NOT_x4_clause3_2": ["OR_clause3"],

    "OR_clause1": ["AND_final"],
    "OR_clause2": ["AND_final"],
    "OR_clause3": ["AND_final"],
    
    "AND_final": []
}

labels = {
    "VAR_x3": "VAR",
    "NOT_x4_clause1": "NOT",
    "VAR_x4_clause1": "VAR",
    
    "VAR_x2_clause2": "VAR",
    "VAR_x1": "VAR",

    "VAR_x4_clause3": "VAR",
    "NOT_x4_clause3_1": "NOT",
    "NOT_x4_clause3_2": "NOT",

    "OR_clause1": "OR",
    "OR_clause2": "OR",
    "OR_clause3": "OR",
    "AND_final": "AND"
}

# Run the consistency check
verify_circuit_consistency(cnf_expression, adjacency_list, labels)
