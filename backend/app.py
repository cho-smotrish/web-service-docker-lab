import os
import time

import psycopg2
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    for attempt in range(20):
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("POSTGRES_DB", "cocktails"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
                connect_timeout=2
            )
        except psycopg2.OperationalError:
            if attempt == 19:
                raise
            time.sleep(1)


@app.get("/api/cocktails")
def cocktails():
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, base, ingredients, preparation, price "
                "FROM cocktails ORDER BY id"
            )
            rows = cursor.fetchall()
        return jsonify([to_cocktail(row) for row in rows])
    except (psycopg2.Error, RuntimeError) as error:
        return jsonify({"error": f"База данных недоступна: {error}"}), 503
    finally:
        if connection is not None:
            connection.close()


@app.get("/api/search")
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Введите название или алкогольную основу"}), 400
    service_url = os.getenv("WEB_SERVICE_URL", "http://web-service:5001")
    try:
        response = requests.get(
            f"{service_url}/search",
            params={"query": query},
            timeout=8
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as error:
        return jsonify({"error": f"Web-сервис недоступен: {error}"}), 503


def to_cocktail(row):
    return {
        "id": row[0],
        "name": row[1],
        "base": row[2],
        "ingredients": row[3],
        "preparation": row[4],
        "price": row[5]
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
