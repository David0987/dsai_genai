from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
from config import Config

# Configure the Gemini API with the key from Config
genai.configure(api_key=Config.GEMINI_API_KEY)

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    print('q', q)
    model = genai.GenerativeModel('gemini-1.5-flash-8b')

    r = model.generate_content(q)
    r = r.text

    return(render_template("gemini_reply.html",r=r))

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)