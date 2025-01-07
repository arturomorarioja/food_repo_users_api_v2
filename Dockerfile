FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=food_repo_users
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5510
ENV FLASK_ENV=development

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["flask", "run"]