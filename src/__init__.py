from flask import Flask, render_template

app = Flask(__name__)

# Маршрут для Главной
@app.route('/')
def home():
    return render_template('home.html')

# Маршрут для Контактов
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Обработчик ошибки 404 (Страница не найдена)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Обработчик ошибки 500 (Внутренняя ошибка сервера)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
