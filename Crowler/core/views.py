from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Crowler import db
from werkzeug.security import generate_password_hash,check_password_hash
from Crowler.models import User
from Crowler.core.spider import Spider
from Crowler.core.filtrs import User_Filtr
from Crowler.core.forms import FilterForm
from Crowler.users.forms import LoginForm

core = Blueprint('core', __name__)
floats_to_show = []
photos_to_show = []
length = []

@core.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            username = user.username
            if next == None or not next[0]=='/':
                next = url_for('core.user_page', username = user.username)

            return redirect(next)
    return render_template('index.html', form=form)

@core.route('/<username>', methods=['GET', 'POST'])
def user_page(username):

    form = FilterForm()
    if form.validate_on_submit():
        global floats_to_show 
        global photos_to_show 
        global length
        user = User.query.filter_by(username=username).first_or_404()
        checked_links = [user.viewed_floats_links]
        checked_photos = [user.viewed_floats_photos]
        user_input = User_Filtr(form.number_of_rooms.data, form.price_from.data, form.price_to.data, form.localization.data)
        release_spider = Spider(user_input.make_taget_url(), checked_links, checked_photos)
        release_spider.add_pages()
        pages = len(release_spider.next_pages)
        i = 0
        while i < pages:
            scanning = Spider(release_spider.next_pages[i], checked_links, checked_photos)
            scanning.crowl()
            #scanning.crawling_on_photos()
            i += 1
        
        floats_to_show = scanning.take_all_info()
        #photos_to_show = scanning.photos
        """if floats_to_show[0]==None:
            floats_to_show = floats_to_show[1:]
            photos_to_show = photos_to_show[1:]"""
        length = list(range(len(floats_to_show)))
    return render_template('user_page.html',form=form, floats_to_show=floats_to_show, length=length)
