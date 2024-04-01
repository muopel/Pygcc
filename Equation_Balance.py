#Function that balnaces equations
from sympy import Matrix, symbols, solve #Matrix is a method that can be used

def balance_equation(equation):
    # Split the equation into reactants and products
    reactants, products = equation.split(' -> ')
    reactants = reactants.split(' + ')
    products = products.split(' + ')

    elements = list(set(''.join(reactants + products)))

    # Create matrices
    reactant_matrix = []
    product_matrix = []
    for element in elements:
        reactant_row = []
        product_row = []
        for reactant in reactants:
            reactant_row.append(reactant.count(element))
        for product in products:
            product_row.append(product.count(element))
        reactant_matrix.append(reactant_row)
        product_matrix.append(product_row)

    # Create SymPy symbols for coefficients
    coefficients = symbols(' '.join(['a{}'.format(i+1) for i in range(len(reactants) + len(products))]))

    # Create equations
    equations = []
    for i in range(len(elements)):
        equation = 0
        for j in range(len(reactants)):
            equation += reactant_matrix[i][j] * coefficients[j]
        for j in range(len(products)):
            equation -= product_matrix[i][j] * coefficients[len(reactants) + j]
        equations.append(equation)

    # Solve equations
    solution = solve(equations)

    # Extract coefficients
    coefficients = [solution[coeff] for coeff in coefficients]

    # Generate balanced equation
    balanced_equation = ''
    for i in range(len(reactants)):
        balanced_equation += str(coefficients[i]) + ' ' + reactants[i] + ' + '
    balanced_equation = balanced_equation[:-3] + ' -> '
    for i in range(len(products)):
        balanced_equation += str(coefficients[len(reactants) + i]) + ' ' + products[i] + ' + '

    return balanced_equation[:-3]

