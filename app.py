from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
import openai

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = "your_secret_key"  # Replace with your actual secret key

openai.api_key = "sk-XwbAc2MeAX_DtqnrNF9H4UuIiny1fVtFeK8QJFwysDT3BlbkFJhHuirSGEpfhCytAhbJ1R1F0uWSB9TwfDJkDTILo9AA"


# Decorator for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def generate_script(prompt, style="humorous", length="medium"):
    script_prompt = f"Write a {length} script in a {style} style. Prompt: {prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a script generator."},
            {"role": "user", "content": script_prompt}
        ],
        max_tokens=600,
        temperature=0.8
    )

    return response['choices'][0]['message']['content'].strip()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate login (placeholder, implement actual validation logic)
        if username and password:  # Replace with actual validation
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Register user logic (placeholder, implement actual registration logic)
        if username and password:  # Replace with actual registration logic
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/generate-script', methods=['POST'])
@login_required
def generate_script_endpoint():
    data = request.json
    prompt = data.get('prompt')
    style = data.get('style', 'dramatic')
    length = data.get('length', 'short')
    script = generate_script(prompt, style, length)
    return jsonify({"script": script})

if __name__ == "__main__":
    app.run(debug=True)
