from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

if os.path.exists("messages.db"):
    conn = sqlite3.connect("messages.db", check_same_thread=False)
    c = conn.cursor()
else:
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE messages
        (message_id INTEGER PRIMARY KEY AUTOINCREMENT, message text)''')
    



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    c.execute("SELECT message FROM messages")
    messages = c.fetchall()
    cleaned_msg = []
    for msg in messages:
        cleaned_msg.append(msg[0])
    messages = cleaned_msg
    if request.method == "GET":
        return render_template("index.html", messages=messages)
    
    if request.method == "POST":
        message = request.form.get("message")
        c.execute("INSERT INTO messages (message) VALUES (?)", (message,))
        conn.commit()
        
        c.execute("SELECT message FROM messages")
        messages = c.fetchall()
        cleaned_msg = []
        for msg in messages:
            cleaned_msg.append(msg[0])
        messages = cleaned_msg
        return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")