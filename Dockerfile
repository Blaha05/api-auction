FROM python:3.12

# Встановлення залежностей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо увесь код
COPY . .

# Вказуємо, що змінні з .env будуть використані
ENV PYTHONUNBUFFERED=1

WORKDIR /app/src

# Запуск FastAPI (змінюй команду залежно від твого фреймворку)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
