from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Crowler import db
from werkzeug.security import generate_password_hash,check_password_hash
from Crowler.models import User
from Crowler.core.spider import Spider
from Crowler.core.filtrs import User_Filtr
from Crowler.core.forms import FilterForm
from Crowler.users.forms import LoginForm

import requests
from bs4 import BeautifulSoup
import re

core = Blueprint('core', __name__)
offerts = []
length = ""

name = ""


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

    global offerts
    global length
    global name

    offerts = []
    length = []

    name = username

    form = FilterForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=username).first_or_404()

        # make url and download olx page
        user_input = User_Filtr(form.number_of_rooms.data, form.price_from.data, form.price_to.data, form.localization.data)
        olxpage = user_input.make_taget_url()
        result = requests.get(olxpage)

        # if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
        if result.status_code == 200:
            soup = BeautifulSoup(result.content, "html.parser")
    
        # find the object with HTML class wibitable sortable
        table = soup.find('table',{'class':'fixed offers breakword redesigned'})

        # loop through all the rows and get all informations 
        #offerts = []
        for row in table.find_all('tr', {'class':'wrap'}):
            img = row.find_all('img', {'class':'fleft'})
            title = row.find_all('a', {'class':'marginright5 link linkWithHash detailsLink'})
            price = row.find_all('p', {'class':'price'})

            link = [t.get('href') for t in title]
            # deal with errors
            if len(link) != 0:
                url = link[0]
                if "www.olx.pl/oferta" in url:
                    response = requests.get(url)
                    html = response.content.decode('utf-8')

                    offert_id = re.findall('(ID ogłoszenia: )(.*?)<', html)[0][1]
                else:
                    offert_id = '0'

            if offert_id not in user.viewed_flats_links:
                # order: img, title, link, price
                column = ([i.get('src') for i in img], [t.get_text() for t in title], [t.get('href') for t in title], [p.get_text() for p in price])
                offerts.append(column)

                user.viewed_flats_links += offert_id + ","
                db.session.add(user)
                db.session.commit()

        length = list(range(len(offerts)))
        

        

    return render_template('user_page.html',form=form, offerts=offerts, length=length)

@core.route('/delete_history')
def delete_history():

    global name

    user = User.query.filter_by(username=name).first_or_404()
    user.viewed_flats_links = ""
    db.session.add(user)
    db.session.commit()

    flash("Historia usunięta")

    return redirect(url_for('core.user_page', username = user.username))