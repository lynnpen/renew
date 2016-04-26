import os
from flask import request, redirect, render_template, url_for, session, flash, g
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from .. import login_manager
from ..models import User, ChatLog
from . import main
from .forms import *

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/index')
@login_required
def index():
    return render_template('index.html')

@main.route('/gallary')
@login_required
def gallary():
    pic_tuple = os.listdir('app/upload')
    return render_template('gallary.html', pic_tuple=pic_tuple)

@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/modpass', methods=['GET', 'POST'])
@login_required
def modpass():
    form = ModPassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
                current_user.password = form.newpassword.data
                current_user.password_hash
                db.session.commit()
                flash('modify password success!')
    return render_template('mod.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))
