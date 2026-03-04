import os
import time
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database configuration from Environment Variables
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_NAME = os.environ.get('DB_NAME', 'todo_db')

def get_db_connection():
    # Retry logic: Wait for MySQL to be ready
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error:
            print("MySQL not ready yet, retrying...")
            time.sleep(5)
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))")
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    # Listen on 0.0.0.0 to be accessible outside the container
    app.run(host='0.0.0.0', port=8080)