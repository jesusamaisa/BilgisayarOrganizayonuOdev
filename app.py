from flask import Flask, render_template, request
from pipeline import simulate_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        code = request.form['code']
        commands = [line.strip() for line in code.strip().splitlines() if line.strip()]
        result = simulate_pipeline(commands)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)