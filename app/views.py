from admin.admin import admin
from app import app, db
from flask import render_template, request, flash, redirect, url_for, session
from app.forms import OrderForm, LoginForm
from app.models import Posts, Menu, Orders, Users

app.register_blueprint(admin, url_prefix='/admin')
# подтягиваем блу-принт, это дает возможность обратиться к урлу /admin - чтобы перейти в другой шаблон

menu = [{'name': 'Главная', 'url': '/index'}, {'name': 'Новости', 'url': '/posts'}, {'name': 'Меню', 'url': '/dishes'},
        {'name': 'Контакты', 'url': '/index#contacts'}, {'name': 'Оформить заказ', 'url': '/do_order'}]

footer = [{'url': 'https://vk.com/lolofmeistahhz', 'class': 'fa-brands fa-vk'},
          {'url': 'https://github.com/Lolofmeistahhz', 'class': 'fa-brands fa-github'},
          {'url': 'https://t.me/lolofmeistahhz', 'class': 'fa-brands fa-telegram'}]

def login_user():
    session['userlogged'] = 1

def is_logged():
    return True if session.get('userlogged') else False
# проверка сессии

def logout_user():
    session.pop('userlogged', None)
    session.clear()
# конец сессии
@app.route('/')
@app.route('/index')
def index():
    posts = Posts.query.order_by(Posts.id.desc()).limit(5).all()  # запрос, выводим 5 последних постов
    return render_template('index.html', title='Главная', menu=menu, footer=footer, posts=posts)


@app.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=5)  # запрос
    # выводим посты, используем метод пагинейт для постраничного вывода
    return render_template("posts.html", pagination=pagination, menu=menu, footer=footer)


@app.route('/dishes')
def dishes():
    page = request.args.get('page', 1, type=int)
    pagination = Menu.query.order_by(Menu.id).paginate(page=page, per_page=6)
    return render_template("dishes.html", pagination=pagination, menu=menu, footer=footer)


@app.route('/post/<num>')
def post(num):
    post = Posts.query.filter(Posts.id == num)
    # запрос для перехода к выбранному посту
    return render_template("post.html", menu=menu, post=post)


@app.route('/do_order', methods=['GET', 'POST'])
def do_order():
    if not is_logged(): # если уже авторизован
        flash('Вы уже успешно авторизовались в системе',
              category='error')
        return redirect(url_for('login'))
    elif is_logged():
        dishes = Menu.query.order_by(Menu.id).all()
        form = OrderForm(request.form, csrf_enabled=False)
        flash('Для того - чтобы совершить заказ, вам необходимо выбрать все знаечния из выпадающего списка',
              category='success')
        if form.validate_on_submit():
            price1 = db.session.query(Menu.price).filter_by(id=int(*form.dish1.raw_data)).first()
            price2 = db.session.query(Menu.price).filter_by(id=int(*form.dish2.raw_data)).first()
            price3 = db.session.query(Menu.price).filter_by(id=int(*form.dish3.raw_data)).first()
            price4 = db.session.query(Menu.price).filter_by(id=int(*form.dish4.raw_data)).first()
            price5 = db.session.query(Menu.price).filter_by(id=int(*form.dish5.raw_data)).first()
            amo = int(*price1) + int(*price2) + int(*price3) + int(*price4) + int(*price5)
            if form.submit2.__call__():
                o = Orders(order_name=form.order_name.data, phone=form.phone.data, adress=form.adress.data,
                           dish1=form.dish1.data, dish2=form.dish2.data, dish3=form.dish3.data, dish4=form.dish4.data,
                           dish5=form.dish5.data, amount=amo)
                db.session.add(o)
                db.session.commit()
                return render_template("do_order.html", menu=menu, footer=footer, dishes=dishes, FlaskForm=form, amo=amo)
        return render_template("do_order.html", menu=menu, footer=footer, dishes=dishes, FlaskForm=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # u = Users(login='root',usertype=0)
    # u.set_password('root')
    # db.session.add(u)
    # db.session.commit()
    if is_logged(): # если уже авторизован
        flash('Вы уже успешно авторизовались в системе',
              category='error')
        return redirect(url_for('.index'))
    form = LoginForm() # инициализация объекта класса LoginForm
    if form.validate_on_submit(): # если данные формы валидны, то
        user = Users.query.filter_by(login=form.login.data).first() # запрос - выбираем
        # пользователей, где данные совпадают с значениями из формы
        if user and user.check_password(form.password.data):
            login_user() # сессия успешно
            if user.usertype==1:
                return redirect(url_for('admin.index'))
            elif user.usertype==0:
                user_id = user.id
                return redirect(url_for('profile',id=user_id))
        else:
            flash('Неверный логин и/или пароль',
                  category='error')
    return render_template('login.html', title='Авторизация', FlaskForm=form)

@app.route('/logout')
def logout():
    if not is_logged(): # если сессия уже прекращена
        flash('Вы уже успешно вышли из системы',
              category='error')
        return redirect(url_for('.index'))
    logout_user() # конец сессии
    flash('Вы  успешно вышли из системы',
          category='success')
    return redirect(url_for('.index'))

