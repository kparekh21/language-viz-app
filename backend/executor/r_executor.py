import subprocess
import uuid
import os
import base64

def run_r_script(code):
    script_id = uuid.uuid4().hex
    filename = f"temp_scripts/script_{script_id}.R"
    image_output = f"outputs/output_{script_id}.png"
    html_output = f"outputs/output_{script_id}.html"

    r_code = f"""{code}

# Save ggplot if exists
tryCatch({{
  if (exists("p") && "ggplot" %in% class(p)) {{
    ggsave("{image_output}", plot = p)
  }}
}}, error = function(e) {{ }})

# Save plotly chart as FULLY self-contained HTML
tryCatch({{
  if (exists("p") && "plotly" %in% class(p)) {{
    htmlwidgets::saveWidget(
      widget = p,
      file = "{html_output}",
      selfcontained = TRUE,
      libdir = NULL, 
      title = "Plotly Chart"
    )
  }}
}}, error = function(e) {{ }})
"""





    with open(filename, 'w') as f:
        f.write(r_code)

    result = subprocess.run(["Rscript", filename], capture_output=True, text=True)

    # Return HTML if plotly was used
    # Read HTML and strip YAML front-matter if detected
    if os.path.exists(html_output):
        with open(html_output, 'r') as f:
            html_content = f.read()

        # If YAML is present at top, strip it
        if html_content.startswith('---'):
            parts = html_content.split('---')
            if len(parts) > 2:
                html_content = parts[2]  # content after header

        return {'type': 'html', 'content': html_content}



    # Return PNG if ggplot2 was used
    if os.path.exists(image_output):
        with open(image_output, 'rb') as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return {
            'type': 'image',
            'content': encoded
        }

    return {
        'type': 'error',
        'content': result.stderr or "No output generated."
    }
