from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # для сессий (задание В, Г)

init_db()

# ---------- Фильтр для даты по-русски (задание Д) ----------
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

# ---------- Главная страница ----------
@app.route('/')
def index():
    messages = get_all_messages()
    success = session.pop('success', None)   # задание В
    error = session.pop('error', None)       # задание Г
    return render_template('index.html', messages=messages, success=success, error=error)

# ---------- Добавление сообщения ----------
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    # Проверка на пустые поля (задание Г)
    if not name or not message:
        session['error'] = 'Заполните все поля!'
        return redirect('/')

    add_message(name, message)
    session['success'] = 'Сообщение добавлено!'   # задание В
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)