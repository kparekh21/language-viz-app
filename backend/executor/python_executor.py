import subprocess
import uuid
import os
import base64
import ast

def is_safe_python(code):
    SAFE_IMPORTS = {
        'matplotlib',
        'matplotlib.pyplot',
        'plotly',
        'plotly.express',
        'plotly.graph_objects',
        'plotly.io'
    }

    BLOCKED_CALLS = {'open', 'eval', 'exec', '__import__', 'input', 'compile', 'os', 'subprocess'}

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in SAFE_IMPORTS:
                        return False
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                if module and not any(module.startswith(allowed) for allowed in SAFE_IMPORTS):
                    return False
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id in BLOCKED_CALLS:
                    return False
        return True
    except Exception as e:
        return False


def run_python_script(code):
    if not is_safe_python(code):
        return {
            'type': 'error',
            'content': 'Blocked potentially unsafe Python code.'
        }

    try:
        filename = f"temp_scripts/script_{uuid.uuid4().hex}.py"
        output_path = f"outputs/output_{uuid.uuid4().hex}.png"
        html_path = output_path.replace('.png', '.html')

        # Inject saving logic into the code
        full_code = f"""{code}

# Save as image if static
try:
    import matplotlib.pyplot as plt
    plt.savefig("{output_path}")
except Exception as e:
    print("Matplotlib save failed:", e)

# Save Plotly output if interactive
try:
    import plotly.io as pio
    fig.write_html("{html_path}")
except Exception as e:
    print("Plotly save failed:", e)
"""

        with open(filename, 'w') as f:
            f.write(full_code)

        result = subprocess.run(["python3", filename], capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            return {
                'type': 'error',
                'content': f"Script error:\n{result.stderr.strip() or 'Unknown script error.'}"
            }

        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                html_content = f.read()
            return {'type': 'html', 'content': html_content}

        if os.path.exists(output_path):
            with open(output_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode('utf-8')
            return {'type': 'image', 'content': encoded}

        return {
            'type': 'error',
            'content': 'Script ran, but no output file was generated. Check if your code created a figure named "fig" or used matplotlib correctly.'
        }

    except subprocess.TimeoutExpired:
        return {
            'type': 'error',
            'content': 'Execution timed out. Your script took too long to run.'
        }
    except Exception as e:
        return {
            'type': 'error',
            'content': f'Internal server error: {str(e)}'
        }
