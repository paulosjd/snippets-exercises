import os
import re
from collections import Counter
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['UPLOAD_FOLDER'] = 'uploads/'


class UploadForm(FlaskForm):
    txt_file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['txt'], 'txt files only')])


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.txt_file.data.filename)
        form.txt_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), encoding='utf-8') as f:
            file_content = f.read()
        return redirect(url_for('analysis', content=file_content))
    return render_template('upload.html', form=form)


def calc_stats(content):
    numbers = []
    for a in content.split():
        try:
            numbers.append(round(float(a)))
        except ValueError:
            pass
    return {'count': len(numbers), 'mean': np.mean(numbers), 'std': np.std(numbers), 'med': np.median(numbers),
            'max': np.max(numbers), 'min': np.min(numbers)}


def count_letters(content):
    letters = re.sub(r'[\W+\d]', '', content).upper()
    let_counts = Counter(a for a in letters)
    let_sum = sum(let_counts.values())
    lets_pc = dict(zip(let_counts.keys(), [a/let_sum*100 for a in let_counts.values()]))
    return lets_pc


@app.route('/<content>')
def analysis(content=None):
    plt.gcf().clear()
    lets = count_letters(content)
    plt.bar(range(len(lets)), list(lets.values()), align='center')
    plt.xticks(range(len(lets)), list(lets.keys()))
    plt.title('Letter counts (%)')
    plt.ylabel('%')
    plt.savefig('static/letters.png')
    plt.gcf().clear()
    word_lens = [len(w) for w in content.split()]
    plt.hist(word_lens, normed=True, bins=30)
    plt.title('Distributions of word lengths')
    plt.xlabel('Word lengths')
    plt.savefig('static/words.png')
    return render_template('analysis.html', **calc_stats(content))


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
