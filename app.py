import re

import nltk
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .PyDictionary import web_get_records

nltk.download("wordnet")

app = Flask(__name__)
app.config["SECRET_KEY"] = "any secret string"
Bootstrap(app)
csrf = CSRFProtect(app)


class WordForm(FlaskForm):
    style = {
        "style": "width:60%; font-size: 1.5vw; padding:10px; border-radius: 10px; border: 1px solid #eee; text-align: center;  transition: .3s border-color;  border: 1px solid #aaa;"
    }
    word = StringField("Word", validators=[DataRequired()], render_kw=style)
    submit = SubmitField("Find")


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    match_item_number = re.compile(r"\d+\.")

    form = WordForm()
    word = " "
    if form.validate_on_submit():
        word = form.word.data
    resp = web_get_records(word)

    resp = match_item_number.sub("", resp).strip()

    resp = (
        resp
        if resp == "Word not found in dictionary." or word == ""
        else resp.split("\n")
    )

    words = []

    if "not found" not in resp:
        loop_index = -1
        match_usage_item_letter = re.compile(r"^\w+\.")

        for res in resp:
            if "-" in  res:
                pos = res.split("-")
                words.append({"part_of_speech": pos[0], "value": pos[1]})
                is_in_usage = False
                loop_index += 1
            elif "Definition" in res:
                words[loop_index]["definition"] = res.replace("Definition : ", "")
            elif match_usage_item_letter.search(res):
                if "usage" not in words[loop_index]:
                    words[loop_index]["usage"] = []

                # words[loop_index]["usage"].append(match_usage_item_letter.sub("", res))
                words[loop_index]["usage"].append(res)

    return render_template("search.html", title="PyDictionary", form=form, resp=words)

if __name__ == "__main__":
    app.run()
