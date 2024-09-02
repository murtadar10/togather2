from flask import Flask, render_template, request
import sympy as sp
import traceback

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    compositions = []
    error_message = None
    functions_list = {}

    if request.method == 'POST':
        functions = request.form.get('functions', '').strip().split('\n')
        functions = [f.strip() for f in functions if f.strip()]

        if not functions:
            error_message = "No functions provided."
        else:
            x = sp.symbols('x')
            func_dict = {}
            try:
                # Define the functions and store them in the dictionary
                for i, func in enumerate(functions):
                    func_name = f"f{i+1}(x)"
                    func_expr = sp.simplify(func)
                    func_dict[func_name] = func_expr
                    functions_list[func_name] = func_expr
            except Exception as e:
                error_message = f"Error processing functions: {e}\n{traceback.format_exc()}"
                return render_template('index.html', compositions=compositions, error_message=error_message, functions_list=functions_list)

            # Compute compositions with detailed steps
            try:
                for name1, f1 in func_dict.items():
                    for name2, f2 in func_dict.items():
                        composition = sp.simplify(f1.subs(x, f2))
                        composition_str = str(composition)

                        # Find the function that matches the result
                        matching_func = next((name for name, func in func_dict.items() if sp.simplify(func) == sp.simplify(composition)), None)

                        # Format the composition result
                        formatted_result = f"{name1} ∘ {name2} = {composition_str}"
                        if matching_func:
                            formatted_result += f" = {matching_func}"
                        else:
                            formatted_result += " (No matching function found)"

                        # Collect details for the result
                        details = {
                           
                            'composition': f"{name1}({name2})",
                            'simplified': formatted_result
                        }
                        compositions.append(details)
            except Exception as e:
                error_message = f"Error computing compositions: {e}\n{traceback.format_exc()}"
                return render_template('index.html', compositions=compositions, error_message=error_message, functions_list=functions_list)

    return render_template('index.html', compositions=compositions, error_message=error_message, functions_list=functions_list)

if __name__ == '__main__':
    app.run(debug=True)
