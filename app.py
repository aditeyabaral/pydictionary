from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, redirect,url_for
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .PyDictionary import web_get_records

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

csrf = CSRFProtect(app)

class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = WordForm()
    if form.validate_on_submit():
        word = form.word.data
        return redirect(url_for('word',word=word))
    return render_template("search.html", title="PyDictionary",form=form)

@app.route('/word/<word>', methods=['GET', 'POST'])
def word(word):
    resp =  web_get_records(word)
    resp = resp.split('\n')
    return render_template("result.html", title="PyDictionary",resp=resp)




if __name__ == "__main__":
    app.run()