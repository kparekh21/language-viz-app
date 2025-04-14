FROM rocker/r-ver:4.3.1

# Install system packages and Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    pandoc curl unzip \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    libfontconfig1-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install R packages
RUN Rscript -e "install.packages(c('ggplot2', 'plotly', 'htmlwidgets', 'htmltools', 'webshot2'), repos='http://cran.us.r-project.org')"

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Create output dirs
RUN mkdir -p outputs temp_scripts

# Expose backend port
EXPOSE 5050

# Run the Flask app
CMD ["python3", "app.py"]