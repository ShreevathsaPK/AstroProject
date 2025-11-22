# Use official Python image
FROM python:3.6.15-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose port Flask will run on
EXPOSE 5009

# Make run.sh executable (if it exists)
RUN chmod +x run.sh || true

# Run the Flask app
CMD ["python", "script_to_gen_horoscope_and_stor/query_script_with_flask.py"]