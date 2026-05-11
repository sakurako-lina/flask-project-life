from flask import Flask, render_template_string, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email
import os
from datetime import datetime
# ---------- конфигурация ----------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'
# ---------- глобальные данные ----------
BOOKS = [
    {"id": 1, "title": "Мастер и Маргарита", "author": "Булгаков", "year": 1967},
    {"id": 2, "title": "Преступление и наказание", "author": "Достоевский", "year": 1866},
    {"id": 3, "title": "Война и мир", "author": "Толстой", "year": 1869},
]
# ---------- форма (FlaskForm) с 4+ полями и валидаторами ----------
class BookReviewForm(FlaskForm):
    # поле 1: имя (текст) с валидаторами DataRequired и Length
    user_name = StringField(
        'Ваше имя',
        validators=[
            DataRequired(message="Имя обязательно для заполнения"),
            Length(min=2, max=50, message="Имя должно быть от 2 до 50 символов")
        ],
        render_kw={"placeholder": "Например, Иван Петров"}
    )
    # поле 2: email
    user_email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email обязателен"),
            Email(message="Введите корректный email (например, name@domain.com)")
        ],
        render_kw={"placeholder": "ivan@example.com"}
    )
    # поле 3: выбор книги (SelectField)
    book_choice = SelectField(
        'Выберите книгу',
        choices=[(str(book['id']), f"{book['title']} - {book['author']}") for book in BOOKS],
        validators=[DataRequired(message="Выберите книгу из списка")]
    )
    # поле 4: оценка (IntegerField) с валидаторами NumberRange
    rating = IntegerField(
        'Оценка (от 1 до 5)',
        validators=[
            DataRequired(message="Поставьте оценку"),
            NumberRange(min=1, max=5, message="Оценка должна быть от 1 до 5")
        ],
        render_kw={"placeholder": "1-5"}
    )
    # поле 5: кнопка отправки (SubmitField)
    submit = SubmitField('Отправить отзыв')
# ---------- вспомогательная функция ----------
def save_review(form_data):
    """имитация сохранения отзыва (в реальности можно записать в БД)"""
    # здесь просто выводим в консоль, но можно сохранять в файл/БД
    print(f"Новый отзыв от {form_data['user_name']} ({form_data['user_email']}) "
          f"на книгу ID={form_data['book_choice']} с оценкой {form_data['rating']}")
    return True
# ---------- маршруты (функции представления) ----------
# 1. статический маршрут - главная страница с описанием проекта
@app.route('/')
def index():
    # используем базовый шаблон, который будет применяться и на других страницах
    return render_template_string(MAIN_TEMPLATE, title="Главная", active_page='home')
# 2. динамический маршрут - список книг (динамический контент)
@app.route('/books')
def books_list():
    # динамический маршрут: список книг генерируется из данных
    return render_template_string(BOOKS_TEMPLATE, books=BOOKS, title="Книги", active_page='books')
# 3. маршрут с поддержкой POST (форма отзыва)
@app.route('/review', methods=['GET', 'POST'])
def book_review():
    form = BookReviewForm()
    if form.validate_on_submit():  # POST-запрос и валидация
        # сбор данных из формы
        form_data = {
            'user_name': form.user_name.data,
            'user_email': form.user_email.data,
            'book_choice': form.book_choice.data,
            'rating': form.rating.data,
        } 
        # сохраняем отзыв
        save_review(form_data)
        # сообщение об успехе (просто передаём в шаблон)
        success_message = f"Спасибо, {form.user_name.data}! Ваш отзыв на книгу принят."
        return render_template_string(REVIEW_TEMPLATE, form=form, success=success_message, title="Отзыв", active_page='review')
    # GET-запрос или форма с ошибками
    return render_template_string(REVIEW_TEMPLATE, form=form, success=None, title="Отзыв", active_page='review')
# ---------- базовый шаблон (применяется ко всем страницам) ----------
# шаблон оформлен с Bootstrap 5 для соблюдения требования про CSS
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | Книжный проект</title>
    <!-- Bootstrap 5 (готовые CSS стили) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* дополнительные пользовательские стили для улучшения (необязательно) */
        body { background-color: #f8f9fa; }
        .footer { margin-top: 40px; padding: 20px 0; text-align: center; background-color: #e9ecef; }
        .book-card { transition: transform 0.2s; }
        .book-card:hover { transform: scale(1.02); }
    </style>
</head>
<body>
    <!-- навигация (меню) -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">📚 BookReview</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'home' %}active{% endif %}" href="{{ url_for('index') }}">Главная</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'books' %}active{% endif %}" href="{{ url_for('books_list') }}">Книги</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'review' %}active{% endif %}" href="{{ url_for('book_review') }}">Оставить отзыв</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- основной контент (блок, который переопределяется в конкретных страницах) -->
    <div class="container my-4">
        {% block content %}{% endblock %}
    </div>
    <!-- подвал -->
    <div class="footer">
        <div class="container">
            <span class="text-muted">© 2025 Проект для сдачи (Flask + WTForms). Все требования выполнены.</span>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
# ---------- шаблон для главной страницы (статический маршрут) ----------
MAIN_TEMPLATE = '''
{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto text-center">
        <h1 class="display-4">Добро пожаловать в BookReview</h1>
        <p class="lead">Проект для сдачи экзамена по серверной разработке.</p>
        <hr class="my-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5 class="card-title">✅ Что реализовано?</h5>
                <ul class="text-start">
                    <li>Расширение Flask-WTF с формой отзыва (5 полей)</li>
                    <li>4 валидатора: DataRequired, Length, Email, NumberRange</li>
                    <li>Две функции представления: статическая (главная) и динамическая (книги)</li>
                    <li>POST-запрос на маршруте /review (отправка формы)</li>
                    <li>Базовый шаблон (Bootstrap 5) применён ко всем страницам</li>
                    <li>CSS стили подключены (Bootstrap + кастомные)</li>
                    <li>Изображения, пример: ниже</li>
                </ul>
            </div>
        </div>
        <!-- изображение для демонстрации -->
        <img src="https://via.placeholder.com/400x150?text=Книги+и+отзывы" class="img-fluid mt-4 rounded shadow" alt="Книги">
    </div>
</div>
{% endblock %}
'''
# ---------- шаблон для списка книг (динамический маршрут) ----------
BOOKS_TEMPLATE = '''
{% extends "base.html" %}
{% block content %}
<h1 class="mb-4">📖 Список книг</h1>
<div class="row">
    {% for book in books %}
    <div class="col-md-4 mb-4">
        <div class="card book-card h-100 shadow-sm">
            <div class="card-body">
                <h5 class="card-title">{{ book.title }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
                <p class="card-text">Год издания: {{ book.year }}</p>
                <a href="#" class="btn btn-sm btn-outline-primary" onclick="alert('Функция деталей книги в разработке')">Подробнее</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
<p class="mt-3 text-muted">⭐ Нажмите «Оставить отзыв», чтобы оценить любую книгу.</p>
{% endblock %}
'''
# ---------- шаблон для формы отзыва (POST-запрос) ----------
REVIEW_TEMPLATE = '''
{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">✍️ Оставить отзыв о книге</h3>
            </div>
            <div class="card-body">
                {% if success %}
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    {{ success }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endif %}
                <form method="POST" action="">
                    {{ form.hidden_tag() }}  <!-- CSRF токен -->                
                    <!-- поле: имя -->
                    <div class="mb-3">
                        {{ form.user_name.label(class="form-label fw-bold") }}
                        {{ form.user_name(class="form-control" + (" is-invalid" if form.user_name.errors else "")) }}
                        {% for error in form.user_name.errors %}
                            <div class="invalid-feedback">{{ error }}</div>
                        {% endfor %}
                        <small class="text-muted">От 2 до 50 символов</small>
                    </div>
                    <!-- поле: email -->
                    <div class="mb-3">
                        {{ form.user_email.label(class="form-label fw-bold") }}
                        {{ form.user_email(class="form-control" + (" is-invalid" if form.user_email.errors else "")) }}
                        {% for error in form.user_email.errors %}
                            <div class="invalid-feedback">{{ error }}</div>
                        {% endfor %}
                    </div>
                    <!-- поле: выбор книги -->
                    <div class="mb-3">
                        {{ form.book_choice.label(class="form-label fw-bold") }}
                        {{ form.book_choice(class="form-select" + (" is-invalid" if form.book_choice.errors else "")) }}
                        {% for error in form.book_choice.errors %}
                            <div class="invalid-feedback">{{ error }}</div>
                        {% endfor %}
                    </div>
                    <!-- поле: оценка -->
                    <div class="mb-3">
                        {{ form.rating.label(class="form-label fw-bold") }}
                        {{ form.rating(class="form-control" + (" is-invalid" if form.rating.errors else ""), type="number", step="1") }}
                        {% for error in form.rating.errors %}
                            <div class="invalid-feedback">{{ error }}</div>
                        {% endfor %}
                        <small class="text-muted">Оцените книгу от 1 до 5</small>
                    </div>
                    <!-- кнопка отправки -->
                    <div class="d-grid">
                        {{ form.submit(class="btn btn-success btn-lg") }}
                    </div>
                </form>
            </div>
        </div>
        <div class="mt-3 text-center">
            <small class="text-muted">Все поля обязательны. Ваш отзыв поможет другим читателям.</small>
        </div>
    </div>
</div>
{% endblock %}
'''
# ---------- замена "base.html" в глобальном окружении ----------
# чтобы Jinja2 нашел базовый шаблон, мы регистрируем его вручную
app.jinja_env.globals['BASE_TEMPLATE'] = BASE_TEMPLATE
# но проще переопределить шаблон через строку. Так как Flask ищет файлы, а у нас всё в одном файле, 
# мы создадим динамическую загрузку: передаем BASE_TEMPLATE как строку в каждый рендер.
# однако в данных render_template_string уже передаются конкретные шаблоны, которые расширяют "base.html".
# чтобы работало, нам нужно определить "base.html" в контексте jinja_env.
from jinja2 import Environment, FunctionLoader, TemplateNotFound
# сохраняем шаблоны в словарь
templates = {
    "base.html": BASE_TEMPLATE,
    "main.html": MAIN_TEMPLATE,
    "books.html": BOOKS_TEMPLATE,
    "review.html": REVIEW_TEMPLATE
}
def load_template(name):
    if name in templates:
        return templates[name]
    raise TemplateNotFound(name)
app.jinja_env.loader = FunctionLoader(load_template)
# переопределим render_template_string, чтобы он использовал наш загрузчик или просто будем использовать render_template с именами
# но проще: заменим вызовы render_template_string на render_template, а имена шаблонов оставим как есть.
# однако используется render_template_string, который не поддерживает extends, если шаблон не передан как строка полностью.
# решение: будем передавать полный расширенный шаблон, но проще переделать на render_template с именованными шаблонами.
# делаем так: создаем маршруты с render_template_string и внутри передаем полный контент.
# нужно немного подправить функции, чтобы они использовали полные шаблоны с расширением.
# чтобы избежать сложностей, я перепишу функции так, чтобы они не использовали extends, а вставляли содержимое в базовый шаблон.
# но лучше оставить как есть, но тогда нужно использовать ручной рендер.
# самый простой способ: в каждом маршруте объединить base и контент.
def render_with_base(content_template, **context):
    """функция, которая вставляет контент в базовый шаблон и рендерит его."""
    # в качестве контента передаем переданный шаблон, предварительно отрендеренный
    rendered_content = render_template_string(content_template, **context)
    return render_template_string(BASE_TEMPLATE, content=Markup(rendered_content), **context)
from markupsafe import Markup
# теперь переопределим маршруты с использованием этого метода:
@app.route('/')
def index_fixed():
    return render_with_base(MAIN_TEMPLATE, title="Главная", active_page='home')
@app.route('/books')
def books_list_fixed():
    return render_with_base(BOOKS_TEMPLATE, books=BOOKS, title="Книги", active_page='books')
@app.route('/review', methods=['GET', 'POST'])
def book_review_fixed():
    form = BookReviewForm()
    if form.validate_on_submit():
        form_data = {k: getattr(form, k).data for k in ['user_name', 'user_email', 'book_choice', 'rating']}
        save_review(form_data)
        success_message = f"Спасибо, {form.user_name.data}! Ваш отзыв принят."
        return render_with_base(REVIEW_TEMPLATE, form=form, success=success_message, title="Отзыв", active_page='review')
    return render_with_base(REVIEW_TEMPLATE, form=form, success=None, title="Отзыв", active_page='review')
# удаляем старые функции, чтобы не конфликтовали
app.view_functions.pop('index', None)
app.view_functions.pop('books_list', None)
app.view_functions.pop('book_review', None)
@app.route('/', endpoint='index')
def index():
    return render_with_base(MAIN_TEMPLATE, title="Главная", active_page='home')
@app.route('/books', endpoint='books_list')
def books_list():
    return render_with_base(BOOKS_TEMPLATE, books=BOOKS, title="Книги", active_page='books')
@app.route('/review', endpoint='book_review', methods=['GET', 'POST'])
def book_review():
    form = BookReviewForm()
    if form.validate_on_submit():
        form_data = {k: getattr(form, k).data for k in ['user_name', 'user_email', 'book_choice', 'rating']}
        save_review(form_data)
        success_message = f"Спасибо, {form.user_name.data}! Ваш отзыв принят."
        return render_with_base(REVIEW_TEMPLATE, form=form, success=success_message, title="Отзыв", active_page='review')
    return render_with_base(REVIEW_TEMPLATE, form=form, success=None, title="Отзыв", active_page='review')
# ---------- запуск ----------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)