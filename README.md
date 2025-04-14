# Language-Agnostic Visualization Web Application

This project is a web-based visualization platform that enables users to submit custom scripts written in either **Python** or **R** to generate **static**, **interactive**, or **3D** charts. The application executes user-submitted code on the backend and returns the resulting visualizations for rendering in the frontend.

## Features

- Support for both Python and R scripting languages
- Handles static (e.g., Matplotlib, ggplot2), interactive (Plotly), and 3D visualizations
- Clean, responsive Angular frontend with live chart rendering via iframe
- Backend script execution in a secure and sandboxed manner
- Basic error handling and unsafe code filtering for Python scripts

---

## Tech Stack

### Frontend:
- **Angular 17+**
- Uses `ngModel`, `srcdoc`, and `DomSanitizer` to safely display embedded chart outputs
- Responsive layout and code editor interface

### Backend:
- **Python + Flask**
- Dynamic execution of scripts using `subprocess`
- Supports:
  - `matplotlib`, `plotly` for Python
  - `ggplot2`, `plotly` for R
- Saves visual outputs as `.png` (static) or `.html` (interactive)
- Secure AST-based filtering to block unsafe Python code (`open`, `os`, `eval`, etc.)


---

## Issues Encountered & Solutions

### 1. **CORS Errors Between Angular and Flask**
- Issue: Angular frontend couldn’t reach Flask backend due to CORS restrictions.
- Fix: Enabled CORS in Flask using `flask_cors.CORS(app)` with appropriate headers.

### 2. **R Plotly Charts Not Rendering in Angular**
- Issue: `htmlwidgets::saveWidget()` was outputting HTML with relative asset paths (`_files/` folders), which iframe could not resolve.
- Fix:
  - Installed `pandoc` and `webshot2` in the environment
  - Ensured `selfcontained = TRUE, libdir = NULL` to inline all JS/CSS in one file
  - Cleaned YAML front matter if present

### 3. **Security Risks in Python Execution**
- Issue: Users could submit dangerous Python code using `os`, `open`, `eval`, etc.
- Fix: Added AST-based whitelisting to allow only known-safe imports and block risky calls.


---

## Prerequisites

- Node.js & Angular CLI for frontend
- Python 3 with Flask, Matplotlib, Plotly
- R with `ggplot2`, `plotly`, `htmlwidgets`, `htmltools`
- `pandoc` and `webshot2` installed for R HTML rendering

---

## Run Locally

### Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend:
```bash
cd frontend
npm install
ng serve
```

## Sample Scripts

Below are sample visualization scripts you can paste into the application to test functionality across Python and R.

### Python Examples

#### 1. Static Line Chart (Matplotlib)

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 14, 12, 18, 20]

plt.figure(figsize=(6, 4))
plt.plot(x, y, marker='o', color='blue')
plt.title("Line Chart")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
```

#### 2. Interactive Scatter Plot (Plotly)

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
```

#### 3. 3D Scatter Plot (Plotly)

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter_3d(df, x="sepal_length", y="sepal_width", z="petal_length", color="species")
```
### R Examples

#### 1. Static Scatter Plot (ggplot2)

```r
library(ggplot2)

p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point(color = "tomato", size = 3) +
  ggtitle("Displacement vs. Highway MPG")
```
#### 2. Interactive Plotly Chart

```r
library(plotly)

p <- plot_ly(
  data = iris,
  x = ~Sepal.Length,
  y = ~Petal.Length,
  color = ~Species,
  type = 'scatter',
  mode = 'markers'
)

```
#### 3. 3D Plotly Scatter Plot

```r
library(plotly)

p <- plot_ly(
  data = iris,
  x = ~Sepal.Length,
  y = ~Sepal.Width,
  z = ~Petal.Length,
  color = ~Species,
  type = 'scatter3d',
  mode = 'markers'
)

```



