from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
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
                return jsonify(message = "Sporočilo shranjeno")
            cursor.execute("SELECT id, content FROM messages ORDER BY id")
            messages = cursor.fetchall()
            return jsonify(messages)
    finally:
        conn.close()
