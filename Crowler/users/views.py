from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Crowler import db
from werkzeug.security import generate_password_hash,check_password_hash
from Crowler.models import User
from Crowler.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        user.viewed_flats_links = ''           
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('core.index'))
    return render_template('register.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))

