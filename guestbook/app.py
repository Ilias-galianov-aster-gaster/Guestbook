from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # требуется для сессий, если будут использоваться

init_db()

# ---------- Фильтр для отображения даты по-русски (задание Д) ----------
@app.template_filter('ru_date')
def ru_date_filter(date_str):
    """Преобразует дату вида 'YYYY-MM-DD' в 'дд месяц YYYY' на русском."""
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        months = {
            1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
            5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
            9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
        }
        return f"{dt.day} {months[dt.month]} {dt.year}"
    except:
        return date_str  # если что-то пошло не так

# ---------- Маршруты ----------
@app.route('/')
def index():
    messages = get_all_messages()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    # Проверка на пустые поля (задание Г – можно раскомментировать при желании)
    # if not name or not message:
    #     return render_template('index.html', messages=get_all_messages(), error='Заполните все поля!')

    if name and message:
        add_message(name, message)
        # Задание В (уведомление) – можно добавить сессию
        # session['success'] = 'Сообщение добавлено!'

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)