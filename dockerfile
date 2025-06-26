# Use a specific Python version (3.8.20)
FROM python:3.8.20

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Only expose Rasa port
EXPOSE 5005

# Run Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
