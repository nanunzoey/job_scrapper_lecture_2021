from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_so_jobs
from indeed import get_indeed_jobs
from save import save_to_file

app = Flask("JobScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_indeed_jobs(word) + get_so_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file('jobs.csv', mimetype='text/csv', attachment_filename='jobs.csv', as_attachment=True)
    except:
        return redirect("/")


# app.run(host="0.0.0.0")
