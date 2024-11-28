import json
from sympy import symbols, Or, And, Not
import random

# Generate a random CNF expression using sympy, ensuring no empty clauses
def generate_random_cnf(num_vars, num_clauses, max_literals_per_clause):
    variables = [symbols(f'x{i}') for i in range(1, num_vars + 1)]
    cnf = []
    
    for _ in range(num_clauses):
        clause = []
        num_literals = random.randint(1, max_literals_per_clause)
        
        for _ in range(num_literals):
            var = random.choice(variables)
            literal = var if random.choice([True, False]) else Not(var)
            clause.append(literal)
        
        if clause:
            cnf.append(Or(*clause))
    
    return And(*cnf)

# Store CNF expressions in a dictionary with indices as keys
cnf_expressions = {}

for i in range(10000):
    num_vars = random.randint(1, 10)
    num_clauses = random.randint(1, 10)
    max_literals_per_clause = random.randint(1, 10)
    
    cnf_expression = generate_random_cnf(num_vars, num_clauses, max_literals_per_clause)
    cnf_expressions[i] = str(cnf_expression)  # Use index `i` as the key for each entry

# Save all CNF expressions to a JSON file
with open("random_check_model.json", "w") as file:
    json.dump(cnf_expressions, file, indent=4)

# print("30,000 CNF expressions saved to random_cnf_expressions.json")
