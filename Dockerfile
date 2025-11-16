# Use official Python image
FROM python:3.6.15-slim


# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from build context (Astro_Projects/)
COPY . .


# Expose port Flask will run on
EXPOSE 5009

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Make run.sh executable
RUN chmod +x run.sh

# Optional: install dependencies later
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["./run.sh"]