from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from PyDictionary import web_get_records

app = Flask(__name__)
app.config["SECRET_KEY"] = "any secret string"
Bootstrap(app)
csrf = CSRFProtect(app)


class WordForm(FlaskForm):
    style = {
        "style": " width:60%;font-size: 1.5vw; padding:10px;  border-radius:10px;border: 1px solid #eee; text-align: center;  transition: .3s border-color;  border: 1px solid #aaa;"
    }
    word = StringField("Word", validators=[DataRequired()], render_kw=style)
    submit = SubmitField("Find")


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = WordForm()
    word = " "
    if form.validate_on_submit():
        word = form.word.data
    resp = web_get_records(word)
    resp = (
        resp
        if resp == "Word not found in dictionary." or word == ""
        else resp.split("\n")
    )
    return render_template("search.html", title="PyDictionary", form=form, resp=resp)


if __name__ == "__main__":
    app.run()
