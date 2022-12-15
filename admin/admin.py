import base64
import fileinput
import os
import time
from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, session, request, flash, make_response
from sqlalchemy import text, func
from sqlalchemy.orm import aliased

from admin.forms import LoginForm, PostForm, DishForm
from app import db, app

from app.models import Users, Posts, Menu, Orders

from werkzeug.utils import secure_filename, send_from_directory

UPLOAD_FOLDER = 'admin/static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# импорт библиотек

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# инициализация blueprintа - шаблон внутри шаблона

menu = [{'name': 'Посты', 'url': '/admin/delete_post'},
        {'name': 'Блюда', 'url': '/admin/delete_dishes'}, {'name': 'Заказы', 'url': '/admin/orders'},
        {'name': 'О себе', 'url': '/admin/about'}, {'name': 'Выйти', 'url': '/admin/logout'}]


# словарь для меню

def login_admin():
    session['adminlogged'] = 1


# сессия

def is_logged():
    return True if session.get('adminlogged') else False


# проверка сессии

def logout_admin():
    session.pop('admin_logged', None)
    session.clear()


# конец сессии


def get_dish_image():
    image = db.session.query(Menu.photo).order_by(Menu.id).first()
    h = make_response(image)
    h.headers['Content-Type'] = 'image/png'
    return h


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin_index.html', title='Админ - панель', menu=menu)


# главная страница

@admin.route('/logout')
def logout():
    logout_admin()  # конец сессии
    return redirect(url_for('index'))


# выход из профиля, конец сессии
@admin.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if not is_logged():  # если сессия уже прекращена
        return redirect(url_for('.login'))
    elif is_logged():  # если сессия актуальна
        form = PostForm(request.form, csrf_enabled=False)  # объект класса PostForm
        if form.validate_on_submit():  # если форма валидна
            p = Posts(title=form.title.data, text=form.text.data)  # запрос к бд, создаем запись, которая берет данные
            # из формы
            db.session.add(p)
            db.session.commit()
            flash('Пост был добавлен',
                  category='success')
            return redirect(url_for('.delete_posts'))
        return render_template('add_post.html', title='Добавить пост', FlaskForm=form)


# добавление постов
@admin.route('/delete_post')
def delete_posts():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=4)  # создание запроса
        # выбираем ID поста, используем метод paginate - для постраничного вывода
        return render_template('delete_posts.html', title='Удалить пост', menu=menu, pagination=pagination)


# просмотр постов

@admin.route('/delete_post/<num>')
def delete_post(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        try:
            post = Posts.query.get_or_404(num)
            db.session.delete(post)
            db.session.commit()
            flash('Пост был удален',
                  category='success')
            return redirect(url_for('.delete_posts'))
        except:
            flash('Пост не был удален',
                  category='error')


# удаление поста
@admin.route('/update_post')
def update_posts():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=4)
        return render_template('delete_posts.html', title='Удалить пост', menu=menu, pagination=pagination)


# обновление поста - пагинация

@admin.route('/update_post/<num>', methods=['GET', 'POST'])
def update_post(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        post = Posts.query.get(num)  # создаем экземпляр класса Post
        form = PostForm(request.form, csrf_enabled=False)
        if request.method == "POST":  # если есть такой запрос
            post.title = form.title.data  # присваиваем значения
            post.text = form.text.data
            post.data = datetime.utcnow()
            db.session.commit()  # сохраняем изменения
            flash('Пост был изменен',
                  category='success')
            return redirect(url_for('.update_posts'))
        return render_template('update_posts.html', title='Удалить пост', posts=post, FlaskForm=form)


# обновление поста - форма обновления
@admin.route('/delete_dishes')
def delete_dishes():
    page = request.args.get('page', 1, type=int)
    pagination = Menu.query.order_by(Menu.id).paginate(page=page, per_page=6)
    return render_template('delete_dishes.html', title='Удалить блюдо', menu=menu, pagination=pagination)


@admin.route('/delete_dishes/<num>')
def delete_dish(num):
    try:
        dish = Menu.query.get_or_404(num)
        db.session.delete(dish)
        db.session.commit()
        flash('Блюдо было удалено',
              category='success')
        return redirect(url_for('.delete_dishes'))
    except:
        flash('Блюдо не было удалено',
              category='error')


@admin.route('/add_dishes', methods=['GET', 'POST'])
def add_dish():
    form = DishForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        f = request.files['photo']
        if f.filename.split(".")[-1] in ALLOWED_EXTENSIONS and "image" in f.mimetype:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            d = Menu(name=form.name.data, description=form.description.data, price=form.price.data,
                     photo=filename)
            db.session.add(d)
            db.session.commit()
            flash('Блюдо было добавлено',
                  category='success')
            return redirect(url_for('.delete_dishes'))
    return render_template('add_dish.html', title='Добавить блюдо', FlaskForm=form)


@admin.route("/downloads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["DOWNLOADS"], filename)


@admin.route('/update_dish')
def update_dishes():
    dish = db.session.query(Menu).order_by(Menu.id).all()
    return render_template('update_dishes.html', title='Удалить блюдо', menu=menu, dish=dish)


@admin.route('/update_dish/<num>', methods=['GET', 'POST'])
def update_dish(num):
    dish = Menu.query.get(num)
    form = DishForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        f = request.files['photo']
        if f.filename.split(".")[-1] in ALLOWED_EXTENSIONS and "image" in f.mimetype:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dish.name = form.name.data
            dish.description = form.description.data
            dish.price = form.price.data
            dish.photo = filename
            db.session.commit()
            flash('Информация о блюде была изменена',
                  category='success')
            return redirect(url_for('.delete_dishes'))
    return render_template('add_dish.html', title='Удалить блюдо', dish=dish, FlaskForm=form)


@admin.route('/orders')
def orders():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Orders).order_by(Orders.id).paginate(page=page, per_page=5)
    dishes = db.session.query(Menu.id, Menu.name, Menu.price).order_by(Menu.id).all()
    print(dishes)
    return render_template('orders.html', title='Заказы', menu=menu, pagination=pagination, dishes=dishes)


@admin.route('/orders/<num>')
def delete_order(num):
    try:
        order = Orders.query.get_or_404(num)
        db.session.delete(order)
        db.session.commit()
        flash('Информация о заказе была удалена',
              category='success')
        return redirect(url_for('.orders'))
    except:
        flash('Произошел сбой',
              category='error')


@admin.route('/about')
def about():
    return render_template('about.html', title='О себе', menu=menu)
