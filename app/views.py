from pip._internal.vcs import git

from admin.admin import admin
from app import app, db
from flask import render_template, request, flash
from app.forms import OrderForm
from app.models import Posts, Menu, Orders

app.register_blueprint(admin, url_prefix='/admin')
# подтягиваем блу-принт, это дает возможность обратиться к урлу /admin - чтобы перейти в другой шаблон

menu = [{'name': 'Главная', 'url': '/index'}, {'name': 'Новости', 'url': '/posts'}, {'name': 'Меню', 'url': '/dishes'},
        {'name': 'Контакты', 'url': '/index#contacts'}, {'name': 'Оформить заказ', 'url': '/do_order'}]

footer = [{'url': 'https://vk.com/lolofmeistahhz', 'class': 'fa-brands fa-vk'},
          {'url': 'https://github.com/Lolofmeistahhz', 'class': 'fa-brands fa-github'},
          {'url': 'https://t.me/lolofmeistahhz', 'class': 'fa-brands fa-telegram'}]


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


@app.route('/update_server', methods=['POST'])


def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
