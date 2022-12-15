import os
from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename

from admin.forms import LoginForm, PostForm, DishForm, OrderSatus
from app import db, app

from app.models import Users, Posts, Menu, Orders

# импорт библиотек

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# инициализация blueprintа - шаблон внутри шаблона

menu = [{'name': 'Вход', 'url': '/admin/login'}, {'name': 'Посты', 'url': '/admin/delete_post'},
        {'name': 'Блюда', 'url': '/admin/delete_dishes'}, {'name': 'Заказы', 'url': '/admin/orders'},
        {'name': 'О себе', 'url': '/admin/about'}, {'name': 'Выйти', 'url': '/admin/logout'}]

# словарь для меню

UPLOAD_FOLDER = 'admin/static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

@admin.route('/')
@admin.route('/index')
def index():
    # u = Users(login='root')
    # u.set_password('root')
    # db.session.add(u)
    # db.session.commit()
    return render_template('admin_index.html', title='Админ - панель', menu=menu)


# главная страница

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged():  # если уже авторизован
        flash('Вы уже успешно авторизовались в системе',
              category='error')
        return redirect(url_for('.index'))
    form = LoginForm()  # инициализация объекта класса LoginForm
    if form.validate_on_submit():  # если данные формы валидны, то
        user = Users.query.filter_by(login=form.login.data).first()  # запрос - выбираем
        # пользователей, где данные совпадают с значениями из формы
        if user and user.check_password(form.password.data):
            login_admin()  # сессия успешно
            return redirect(url_for('admin.index'))
        else:
            flash('Неверный логин и/или пароль',
                  category='error')
    return render_template('login.html', title='Авторизация', FlaskForm=form)


# страница входа

@admin.route('/logout')
def logout():
    if not is_logged():  # если сессия уже прекращена
        flash('Вы уже успешно вышли из системы',
              category='error')
        return redirect(url_for('.index'))
    logout_admin()  # конец сессии
    flash('Вы  успешно вышли из системы',
          category='success')
    return redirect(url_for('.index'))


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
        pagination = Posts.query.order_by(Posts.id.desc()).paginate(page=page, per_page=4)  # создание запроса
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
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Menu.query.order_by(Menu.id.desc()).paginate(page=page, per_page=6)
        return render_template('delete_dishes.html', title='Удалить блюдо', menu=menu, pagination=pagination)


@admin.route('/delete_dishes/<num>')
def delete_dish(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
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
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
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


@admin.route('/update_dish')
def update_dishes():
    dish = db.session.query(Menu).order_by(Menu.id).all()
    return render_template('update_dishes.html', title='Удалить блюдо', menu=menu, dish=dish)


@admin.route('/update_dish/<num>', methods=['GET', 'POST'])
def update_dish(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
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
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        form = OrderSatus(request.form, csrf_enabled=False)  # объект класса PostForm
        page = request.args.get('page', 1, type=int)
        name1 = aliased(Menu)
        name2 = aliased(Menu)
        name3 = aliased(Menu)
        name4 = aliased(Menu)
        name5 = aliased(Menu)
        pagination = db.session.query(Orders.id, Orders.order_name, Orders.adress, Orders.status, Orders.amount,
                                      name1.name.label('n1'), name2.name.label('n2'), name3.name.label('n3'),
                                      name4.name.label('n4'), name5.name.label('n5')).filter(name1.id == Orders.dish1,
                                                                                             name2.id == Orders.dish2,
                                                                                             name3.id == Orders.dish3,
                                                                                             name4.id == Orders.dish4,
                                                                                             name5.id == Orders.dish5).order_by(
            Orders.id.desc()).paginate(page=page, per_page=5)
        return render_template('orders.html', title='Заказы', menu=menu, pagination=pagination, FlaskForm=form)


@admin.route('/orders/del/<num>')
def delete_order(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
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


@admin.route('/orders/edit/<num>', methods=['GET', 'POST'])
def edit_satus(num):
    page = request.args.get('page', 1, type=int)
    pagination = Orders.query.order_by(Orders.id).paginate(page=page, per_page=5)
    dishes = db.session.query(Menu.id, Menu.name, Menu.price).order_by(Menu.id).all()
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        form = OrderSatus(request.form, csrf_enabled=False)  # объект класса PostForm
        ord = Orders.query.get(num)
        if request.method == 'POST' and form.validate_on_submit():
            ord.status = form.status.data
            print(form.status.data)
            db.session.commit()
            flash('Информация о блюде была изменена',
                  category='success')
            return redirect(url_for('.orders'))
    return render_template('update_order_status.html', title='Заказы', menu=menu, pagination=pagination, dishes=dishes,
                           FlaskForm=form, order=ord)


@admin.route('/about')
def about():
    return render_template('about.html', title='О себе', menu=menu)
