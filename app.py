from flask import Flask, render_template, request, redirect, url_for

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)