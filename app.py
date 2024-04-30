from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DATABASE = 'zihao.db'


def connect_db():
    return sqlite3.connect(DATABASE)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        messages = cursor.fetchall()
        conn.close()
        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=80)
