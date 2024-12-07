# Gunakan base image Python
FROM python:3.9-slim

# Set lingkungan kerja
WORKDIR /app

# Salin file requirements.txt
COPY requirements.txt .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke container
COPY . .

# Expose port default Flask
EXPOSE 8080

# Command untuk menjalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
