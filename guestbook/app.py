from flask import Flask, render_template, request, redirect, session
from database import (
    init_db, get_all_messages, add_message,
    delete_message, get_message_count, delete_all_messages
)
from datetime import date

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # для сессий (если понадобится)

init_db()

# ---------- Фильтр для даты по-русски (из пр10, оставим) ----------
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

# ---------- Главная страница (задание 6 - счётчик) ----------
@app.route('/')
def index():
    messages = get_all_messages('DESC')  # по умолчанию новые сверху
    total_count = get_message_count()
    today = date.today().isoformat()     # для выделения свежих (задание Б)
    return render_template('index.html',
                           messages=messages,
                           total_count=total_count,
                           today=today)

# ---------- Сортировка (задание А) ----------
@app.route('/sort/<order>')
def sort_messages(order):
    if order not in ['newest', 'oldest']:
        return redirect('/')
    sql_order = 'DESC' if order == 'newest' else 'ASC'
    messages = get_all_messages(sql_order)
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html',
                           messages=messages,
                           total_count=total_count,
                           today=today)

# ---------- Добавление сообщения ----------
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    if name and message:
        add_message(name, message)
    return redirect('/')

# ---------- Удаление одного (задание 2) ----------
@app.route('/delete/<int:message_id>')
def delete(message_id):
    delete_message(message_id)
    return redirect('/')

# ---------- Удаление всех (задание В) ----------
@app.route('/delete-all')
def delete_all_page():
    # Показываем страницу подтверждения
    return render_template('delete_all.html')

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    delete_all_messages()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)