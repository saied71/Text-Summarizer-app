from flask import Flask,render_template, request
import pickle
from summarizer import Summarizer
import re


summ = Summarizer()
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    text=""
    summary=""
    if request.method == "POST":
        text = request.form.get("claim")
        cltext = re.sub('[\s]', " ", text)
        summary = summ.generate_summary(cltext)
    return render_template("index.html",org_text=text, summ=summary)


if __name__ == "__main__":
    app.run(debug=True)