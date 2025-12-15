# Base image
FROM python:3.10-slim

# Prevent python from buffering stdout (Important for logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (Caching layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (Render sets $PORT env var automatically, but we default to 8000)
ENV PORT=8000
EXPOSE $PORT

# Command to run the app
# We use shell form to expand the $PORT variable
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT