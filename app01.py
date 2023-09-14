from pathlib import PurePath, Path
from venv import logger

# from venv import logger

from flask import Flask, render_template, request, abort, redirect, url_for, flash, make_response
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask('__name__')
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/index/')
def index():
    context = {
        'title': 'seminar 2'
    }
    return render_template('base.html', **context)

@app.route('/task1/')
def task1():
    context = {
        'title': 'task 1'
    }
    return render_template('task1.html', **context)

@app.route('/task2/', methods=['GET', 'POST'])
def task2():
    context = {
        'title': 'task 2'
    }
    if request.method == 'POST':
        file = request.files.get('uploaded_img')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'static/img', 'uploaded_image.png'))
        return f'Image {escape(file_name)} uploaded!'
    return render_template('task2.html', **context)

@app.route('/task3/', methods=['GET', 'POST'])
def task3():
    context = {
        'title': 'task 3'
    }
    users = {
        '123@mail.ru': '1234',
        'a@gmail.com': '1234'
    }
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        if users.get(username) == password:
            return f'Login {username} correct'
        else:
            return f'Login or password incorrect'
    return render_template('task3.html', **context)

@app.route('/task4/', methods=['GET', 'POST'])
def task4():
    context = {
        'title': 'task 4'
    }
    if request.method == 'POST':
        input_text = request.form.get('text')
        return f'Your text contains {len(input_text.split())} words'
    return render_template('task4.html', **context)

@app.route('/task5/', methods=['GET', 'POST'])
def task5():
    context = {
        'title': 'task 5'
    }
    if request.method == 'POST':
        a = int(escape(request.form.get('a')))
        b = int(escape(request.form.get('b')))
        operation = request.form.get('operation')
        result = None
        match operation:
            case '+':
                result = a + b
            case '-':
                result = a - b
            case '*':
                result = a * b
            case '/':
                result = a / b
        return f'Result = {result}'
    return render_template('task5.html', **context)

@app.route('/task6/', methods=['GET', 'POST'])
def task6():
    MIN_AGE = 18
    context = {
        'title': 'task 6'
    }
    if request.method == 'POST':
        age = int(request.form.get('age'))
        if age >= MIN_AGE:
            return "Sign up success"
        abort(403)
    return render_template('task6.html', **context)

@app.errorhandler(403)
def too_young(e):
    logger.warning(e)
    context = {
        'title': 'You are too young',
        'url': request.base_url
    }
    return render_template('403.html', **context), 403

@app.route('/task7_answer/<num>')
def task7_answer(num):
    context = {
        'title': 'task 7',
        'num': int(num)
    }
    return render_template('task7_answer.html', **context)

@app.route('/task7_redirect/', methods=['GET', 'POST'])
def task7_redirect():
    if request.method == 'POST':
        num = request.form.get('num')
        return redirect(url_for('task7_answer', num=num))
    return render_template('task7.html')

@app.route('/task8', methods=['GET', 'POST'])
def task8():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('task8'))
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('task8'))
    return render_template('task8.html')

@app.route('/task9', methods=['GET', 'POST'])
def task9_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect('/task9_welcome'))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)
        return response
    return render_template('task9_form.html', title='Task 9 - FORM')

@app.route('/task9_welcome/')
def task9_welcome():
    context = {
        'title': 'Task 9',
        'name': request.cookies.get('user_name')
    }
    return render_template('task9_welcome.html', **context)

@app.route('/task9_logout/')
def task9_logout():
    response = redirect('/task9')
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')
    return response

if __name__ == '__main__':
    app.run(debug=True)