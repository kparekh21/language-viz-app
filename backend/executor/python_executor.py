import subprocess
import uuid
import os
import base64

def run_python_script(code):
    filename = f"temp_scripts/script_{uuid.uuid4().hex}.py"
    output_path = f"outputs/output_{uuid.uuid4().hex}.png"

    # Inject code to save matplotlib output
    full_code = f"""{code}

# Save as image if static
try:
    import matplotlib.pyplot as plt
    plt.savefig("{output_path}")
except:
    pass

# Save Plotly output if interactive
try:
    import plotly.io as pio
    fig.write_html("{output_path.replace('.png', '.html')}")
except:
    pass
"""

    with open(filename, 'w') as f:
        f.write(full_code)

    result = subprocess.run(["python3", filename], capture_output=True, text=True)

    html_path = output_path.replace('.png', '.html')
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
        'content': result.stderr or 'Unknown error'
    }