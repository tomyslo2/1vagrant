from flask import Flask, jsonify, request
import psycopg2
import redis
import json

app = Flask(__name__)
cache = redis.Redis(host = "127.0.0.1", port = 6379, decode_responses = True)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        cached = cache.get("messages")
        if cached is not None:
            return jsonify(json.loads(cached))
            
    conn = psycopg2.connect(dbname="devops")
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                data = request.get_json(silent = True)
                content = data.get("content")
                cursor.execute(
                    "INSERT INTO messages (content) VALUES (%s)",
                    (content,)
                )
                conn.commit()
                cache.delete("messages")
                return jsonify(message = "Sporočilo shranjeno")
            cursor.execute("SELECT id, content FROM messages ORDER BY id")
            messages = cursor.fetchall()
            cache.set("messages", json.dumps(messages))
            return jsonify(messages)
    finally:
        conn.close()
