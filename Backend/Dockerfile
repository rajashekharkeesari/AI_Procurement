FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY Backend/ ./Backend/
COPY .env .

# Create empty DB files if they don't exist (volumes will override)
RUN touch procurement.db workflow_checkpoints.db

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "-m", "Backend.app"]
