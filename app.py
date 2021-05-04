from flask import Flask, render_template, request

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    searchingword = request.args.get('searchingword')
    return render_template("report.html", word=searchingword)


app.run(host="0.0.0.0")
