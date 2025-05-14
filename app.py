from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
# from google.generativeai import 

# import google.generativeai as genai
gemini_api = 'AIzaSyBf_C_bV9mPzvwOkwI9Hqzyxx_6QJdPYc8'
genai.configure(api_key=gemini_api)

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    # if request.method == "POST":
    #     t = request.form.get("txt")
    #     r = palm.generate_test(**defaults,messages=t)
    #     return(render_template("index.html",result=r.last))
    # else:
    #     return(render_template("index.html",result="waiting"))
    return(render_template("index.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    print('q', q)
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    # Initialize the model

    # r = model.generate_content(q)
    r = model.generate_content(q)

    r = r.text
#
    return(render_template("gemini_reply.html",r=r))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)