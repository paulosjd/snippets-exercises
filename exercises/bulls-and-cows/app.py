from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Regexp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

class NumberForm(FlaskForm):
    guess = StringField('Input number:', validators=[InputRequired(), Regexp(r"[1-9]{4}",
                                                                            message='Enter 4 digits between 1 and 9')])


if __name__ == '__main__':
    app.run(debug=True)
