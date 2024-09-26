from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# Временное хранилище для данных пользователей
users = []

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Добро пожаловать!</title>
        <style>
            body {
                background-color: #E6F4EA; /* Нежно-зеленый цвет */
                font-family: Arial, sans-serif;
            }
            h1 {
                text-align: center;
            }
            form {
                max-width: 400px;
                margin: auto; /* Центруем форму */
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            label, input, button {
                display: block;
                width: 100%;
                margin-bottom: 10px;
            }
            button {
                background-color: #66CDAA; /* Зеленый цвет для кнопки */
                color: white;
                border: none;
                padding: 10px;
                cursor: pointer;
            }
            button:hover {
                background-color: #20B2AA; /* Темно-зеленый при наведении */
            }

            /* Стиль для всплывающего окна */
            .modal {
                display: none; /* Скрыто по умолчанию */
                position: fixed; /* Окно фиксируется */
                z-index: 1000; /* Слой над другими элементами */
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон */
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            .close {
                cursor: pointer;
                color: #66CDAA; /* Цвет кнопки закрытия */
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать!</h1>
        <form id="userForm">
            <label for="first_name">Имя:</label>
            <input type="text" id="first_name" name="first_name" required>
            <label for="last_name">Фамилия:</label>
            <input type="text" id="last_name" name="last_name" required>
            <label for="phone">Номер телефона:</label>
            <input type="text" id="phone" name="phone" required>
            <label for="email">Электронная почта:</label>
            <input type="email" id="email" name="email">
            <button type="submit">Отправить</button>
        </form>

        <!-- Всплывающее окно -->
        <div id="modal" class="modal">
            <div class="modal-content">
                <span id="close" class="close">&times;</span>
                <div id="response"></div>
            </div>
        </div>

        <script>
            document.getElementById('userForm').onsubmit = async function(e) {
                e.preventDefault();
                const first_name = document.getElementById('first_name').value;
                const last_name = document.getElementById('last_name').value;
                const phone = document.getElementById('phone').value;
                const email = document.getElementById('email').value;

                const response = await fetch('/check', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ first_name: first_name, last_name: last_name, phone: phone, email: email })
                });

                const data = await response.json();
                document.getElementById('response').textContent = data.message || data.status;
                document.getElementById('modal').style.display = 'flex'; // Показываем модальное окно
            };

            // Закрытие модального окна
            document.getElementById('close').onclick = function() {
                document.getElementById('modal').style.display = 'none';
            };

            // Закрытие модального окна при клике вне него
            window.onclick = function(event) {
                const modal = document.getElementById('modal');
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            };
        </script>
    </body>
    </html>
    ''')


@app.route('/check', methods=['POST'])
def check_data():
    data = request.json

    # Проверка имени
    if 'first_name' not in data or not data['first_name'].strip() or len(data['first_name'].strip()) < 2:
        return jsonify({"status": "error", "message": "Имя должно содержать не менее 2 символов!"}), 400

    # Проверка фамилии
    if 'last_name' not in data or not data['last_name'].strip() or len(data['last_name'].strip()) < 2:
        return jsonify({"status": "error", "message": "Фамилия должна содержать не менее 2 символов!"}), 400

    # Проверка номера телефона
    if 'phone' not in data or not data['phone'].strip():
        return jsonify({"status": "error", "message": "Номер телефона не может быть пустым!"}), 400

    phone_pattern = r"^\d{11}$"
    if not re.match(phone_pattern, data['phone']):
        return jsonify({"status": "error", "message": "Номер телефона должен содержать 11 цифр!"}), 400

    # Проверка эл. почты
    if 'email' in data and data['email'].strip():
        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_pattern, data['email']):
            return jsonify({"status": "error", "message": "Некорректный формат электронной почты!"}), 400

    # Сохранение пользователя в памяти
    users.append({
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "phone": data['phone'],
        "email": data.get('email')
    })

    return jsonify({"status": "success", "message": "Данные успешно сохранены! Спасибо что слили все ваши данные :)"}), 200


if __name__ == '__main__':
    app.run(debug=True)
