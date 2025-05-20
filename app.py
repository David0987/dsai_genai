from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
from config import Config
import os
import sqlite3
import datetime

gemini_api_key = os.getenv("GEMINI_API_KEY")

# conn = sqlite3.connect('user.db')
# conn.execute('create table users (name text, timestamp timestamp)')

# Configure the Gemini API with the key from Config
genai.configure(api_key=gemini_api_key)
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-8b')

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    if request.method == "POST":
        q = request.form.get("q")
        print("where is the q",q)
        t = datetime.datetime.now()
        
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into users(name,timestamp) values(?,?)",(q,t))
        conn.commit()
        c.close()
        conn.close()
    return(render_template("main.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/user_log",methods=["GET","POST"])
def user_log():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from users")
    r = ""
    for row in c:
        print(row)
        r = r+str(row) + "\n"
        print(r)
    c.close()
    print("r: ",r)
    conn.close()

    return(render_template("user_log.html",r=r))

@app.route("/delete_log",methods=["GET","POST"])
def delete_log():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from users")
    # r = ""
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete_log.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    print('q', q)

    r = model.generate_content(q)
    r = r.text

    return(render_template("gemini_reply.html", r=r))

if __name__ == "__main__":
    # app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    app.run(debug=True)