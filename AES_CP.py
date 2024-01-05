


P= [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]

def generate_decision_variables(num_inputs,r):
    input_var='\n'.join(f'var 0..1: input{i};' for i in range(1, (r+1)*num_inputs + 1))
    #output_var='\n'.join(f'var 0..1: input{i};' for i in range(1, r*num_outputs + 1))
    r_var='\n'.join(f'var 0..10: r{i};' for i in range(1, 4*r+1))


    return input_var + '\n' +r_var

def generate_objective_function(num_inputs,r):
    objective_terms = [f'input{i}' for i in range(1, (r+1)*num_inputs + 1)]
    return f"var int: objective = {' + '.join(objective_terms)};"

def generate_nonzero_start(num_inputs):
    
    variables = ' + '.join(f'input{i}' for i in range(1, num_inputs + 1))
    return  f"constraint {variables} > 0;";

def generate_sum_constraint(num_inputs,r):
    variables='\n'
    
 
    for i in range(0,r):
            variables += f'constraint input{i*16 + P[0]+1} + input{i*16 + P[1]+1} + input{i*16 + P[2]+1} + input{i*16 + P[3]+1} '
            variables += f'+ input{(i+1)*16 + 1} + input{(i+1)*16 +  2} + input{(i+1)*16 +  3} + input{(i+1)*16 +  4} = r{(4*i)+1};\n'

            variables += f'constraint input{i*16 + P[4]+1} + input{i*16 + P[5]+1} + input{i*16 + P[6]+1} + input{i*16 + P[7]+1} '
            variables += f'+ input{(i+1)*16 + 5} + input{(i+1)*16 +  6} + input{(i+1)*16 +  7} + input{(i+1)*16 +  8} = r{(4*i)+2};\n'

            variables += f'constraint input{i*16 + P[8]+1} + input{i*16 + P[9]+1} + input{i*16 + P[10]+1} + input{i*16 + P[11]+1} '
            variables += f'+ input{(i+1)*16 + 9} + input{(i+1)*16 +  10} + input{(i+1)*16 + 11} + input{(i+1)*16 +  12} = r{(4*i)+3};\n'

            variables += f'constraint input{i*16 + P[12]+1} + input{i*16 + P[13]+1} + input{i*16 + P[14]+1} + input{i*16 +P[15] +1} '
            variables += f'+ input{(i+1)*16 +  13} + input{(i+1)*16 +  14} + input{(i+1)*16 +  15} + input{(i+1)*16 +  16} = r{(4*i)+4};\n'
    return variables

def generate_assert_constraint(r):
    variables=''
    for i in range(0,4*r):
        variables += f"constraint r{i+1} in {{0, 5, 6, 7, 8}};\n";
    return variables

def generate_output_statements(num_inputs,r):
    input_statements = ''.join(f'output ["Input{i}: \\(input{i})\\n"];\n' for i in range(1, (r+1)*num_inputs + 1))

    return input_statements + f'\noutput ["Objective: \\(objective)\\n"]';
def generate_minizinc_model(num_inputs,r):
    decision_variables = generate_decision_variables(num_inputs,r)
    objective_function = generate_objective_function(num_inputs,r)
    nonzero_start=generate_nonzero_start(num_inputs)
    sum_constraint = generate_sum_constraint(num_inputs,r)
    assert_constraint = generate_assert_constraint(r)
    output_statements = generate_output_statements(num_inputs,r)

    model_str = """
% Define decision variables
{}
{}
{}
{}
{}
% Other constraints as needed

% Solve to minimize the objective function
solve minimize objective;

% Output the results
{}
""".format(decision_variables, objective_function, nonzero_start,sum_constraint, assert_constraint, output_statements)

    return model_str

# Example usage with 4 inputs and 4 outputs
r=4
num_inputs = 16


# Generate the MiniZinc model
model_str = generate_minizinc_model(num_inputs,r)

# Write the MiniZinc model to a file
with open("flexible_model.mzn", "w") as file:
    file.write(model_str)

# Inform the user
print(f"MiniZinc model written to flexible_model.mzn")
