import re
import nltk
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from utils import web_get_records, get_suggestions

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
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

        words = []
        suggestions = []

        if resp:
            resp = match_item_number.sub("", resp).strip().split("\n")
            loop_index = -1
            match_usage_item_letter = re.compile(r"^\w+\.")

            for res in resp:
                if "-" in res and " " not in res:
                    pos = res.split("-")
                    words.append({"part_of_speech": pos[0], "value": pos[1]})
                    loop_index += 1
                elif "Definition" in res:
                    words[loop_index]["definition"] = res.replace(
                        "Definition : ", "")
                elif match_usage_item_letter.search(res):
                    if "usage" not in words[loop_index]:
                        words[loop_index]["usage"] = []

                    words[loop_index]["usage"].append(res)
        else:
            suggestions = get_suggestions(word)

        return render_template("search.html", title="PyDictionary", form=form, resp=words, found=len(words) >= 1, suggestions=suggestions[:5] if len(suggestions) > 5 else suggestions)
    return render_template("search.html", title="PyDictionary", form=form, resp=[], found=True, suggestions=[])


if __name__ == "__main__":
    app.run()
