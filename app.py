from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
from config import Config
import os
import sqlite3
import datetime
import requests

# set up telegram webhook
# curl -F "url=https://dsai-genai-ok5a.onrender.com/telegram" https://api.telegram.org/bot8074722179:AAEPKM37HrgOzAwtPHEdd0fbCxKgALexRdo/setWebhook


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

@app.route("/paynow",methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    # setting up webhook
    if request.method == "POST":
        q = request.form.get("q")
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

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    if request.method == "POST":
        sgd = float(request.form.get('sgd')) if request.form.get('sgd') else 0
        # Formula to convert SGD to DBS stock price
        # dbs_price = sgd * 0.75  # Example conversion rate
        print("sgd: ",sgd)
        dbs_price = 90.22858515 + (-50.60094302*sgd)
        return render_template("prediction.html", dbs_price=dbs_price)
    return render_template("prediction.html", dbs_price=None)

@app.route("/prediction_reply",methods=["GET","POST"])
def prediction_reply():
    q = float(request.form.get("sgd"))
    print(q)
    return(render_template("prediction_reply.html",dbs_price=90.2 + (-50.6*q)))

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

@app.route("/telegram",methods=["GET","POST"])
def telegram():
    try:
        data = request.get_json()
        if not data:
            return render_template("telegram.html", r_text='Telegram Started')
            
        if 'message' not in data:
            return render_template("telegram.html", r_text='Invalid message format')
            
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        # console.log(f"Received message from chat_id {chat_id}: {text}")

        if text == '/start':
            r_text = "I'm a financial assistant. Ask me finance related questions?"
            return('ok', 200)
        else:
            system_prompt = "You are a financial expert. Answer ONLY questions related to finance, economics, investing, and financial markets. If the question is not related to finance, state that you cannot answer it."
            response = model.generate_content(f"{system_prompt}\n\nUser Query: {text}")
            r_text = response.text
            
            payload = {'chat_id': chat_id, 'text': r_text}
            response = requests.post(
                "https://api.telegram.org/bot8074722179:AAEPKM37HrgOzAwtPHEdd0fbCxKgALexRdo/sendMessage",
                json=payload
            )
            requests.post(send_message_url, data={"chat_id": chat_id, "text": r_text})
            # console.log(response)
            response.raise_for_status()
            return 'ok', 200
            
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return 'error', 404
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template("telegram.html", r_text='An error occurred')


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

@app.route("/logout",methods=["GET"])
def logout():
    return(render_template("index.html"))

if __name__ == "__main__":
    # app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    app.run(debug=True)