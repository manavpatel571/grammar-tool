from flask import Flask, render_template, request
from spello.model import SpellCorrectionModel
import re

app = Flask(__name__)

# Load and preprocess data
with open("big.txt", "r") as f:
    big = f.readlines()
big_preprocessed = [re.sub(r'\\t', ' ', text) for text in big if text.strip()]

# Train the model
sp = SpellCorrectionModel(language='en')
sp.train(big_preprocessed)

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'\\t', ' ', text)
    text = re.sub("\\'", "", text)
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    text = text.strip()
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        corrected_text = sp.spell_correct(preprocess_text(user_input))
        return render_template('index.html', user_input=user_input, corrected_text=corrected_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
