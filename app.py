from flask import Flask, render_template, jsonify
import requests
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    # Отображаем главную страницу с кнопкой для новой цитаты
    return render_template('index.html')

@app.route('/quote')
def get_quote():
    # Запрос случайной цитаты с API
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        quote = data.get('content')
        author = data.get('author')
        # Переводим цитату на русский
        translated = translator.translate(quote, src='en', dest='ru')
        translated_quote = translated.text
    else:
        quote = "Не удалось получить цитату."
        author = ""
        translated_quote = quote

    # Возвращаем данные в формате JSON для использования в AJAX-запросе
    return jsonify(quote=quote, translated_quote=translated_quote, author=author)

if __name__ == '__main__':
    app.run(debug=True)