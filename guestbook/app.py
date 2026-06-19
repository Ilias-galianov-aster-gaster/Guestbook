from flask import Flask, render_template, request, redirect, session
from database import (
    init_db, get_all_messages, add_message,
    delete_message, get_message_count, delete_all_messages,
    check_user
)
from datetime import date
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey_for_guestbook'

init_db()

# ---------- Фильтр даты ----------
@app.template_filter('ru_date')
def ru_date_filter(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        months = {
            1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
            5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
            9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
        }
        return f"{dt.day} {months[dt.month]} {dt.year}"
    except:
        return date_str

# ---------- ГЛАВНАЯ СТРАНИЦА (меню) ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- ГОСТЕВАЯ КНИГА ----------
@app.route('/guestbook')
def guestbook():
    messages = get_all_messages('DESC')
    total_count = get_message_count()
    today = date.today().isoformat()
    logged_in = session.get('logged_in', False)
    username = session.get('username')
    return render_template(
        'guestbook.html',
        messages=messages,
        total_count=total_count,
        today=today,
        logged_in=logged_in,
        username=username
    )

@app.route('/sort/<order>')
def sort_messages(order):
    if order not in ['newest', 'oldest']:
        return redirect('/guestbook')
    sql_order = 'DESC' if order == 'newest' else 'ASC'
    messages = get_all_messages(sql_order)
    total_count = get_message_count()
    today = date.today().isoformat()
    logged_in = session.get('logged_in', False)
    username = session.get('username')
    return render_template(
        'guestbook.html',
        messages=messages,
        total_count=total_count,
        today=today,
        logged_in=logged_in,
        username=username
    )

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    if name and message:
        add_message(name, message)
    return redirect('/guestbook')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    if not session.get('logged_in'):
        return redirect('/login')
    delete_message(message_id)
    return redirect('/guestbook')

@app.route('/delete-all')
def delete_all_page():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('delete_all.html')

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    if not session.get('logged_in'):
        return redirect('/login')
    delete_all_messages()
    return redirect('/guestbook')

# ---------- АВТОРИЗАЦИЯ ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if check_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/guestbook')
        else:
            error = 'Неверный логин или пароль'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/guestbook')

# ---------- BOOTSTRAP ПЕСОЧНИЦА (пр13) ----------
@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')

if __name__ == '__main__':
    app.run(debug=True)