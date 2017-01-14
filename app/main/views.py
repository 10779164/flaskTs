from datetime import datetime  
from flask import flash,render_template,session,redirect,url_for,current_app,request
from . import main  
from .forms import NameForm,RegisterForm,PostForm
from .. import db  
from ..models import User,Post
from ..email import send_email
from .. import mail  
from flask_login import login_user,logout_user,current_user,login_required
 
 
@main.route('/',methods=['GET','POST'])  
def index():  
    page=request.args.get('page',1,type=int)
    pagination=Post.query.paginate(page,per_page=1,error_out=False)
    posts=pagination.items
    return render_template('index.html',posts=posts,pagination=pagination)  

@main.route('/login',methods=['GET','POST'])
def login():
    form=NameForm()
    user=User.query.filter_by(username=form.name.data).first()
    if form.validate_on_submit():
        if user is not None and user.confirm_password(form.password.data):
            if current_user.is_authenticated:
                logout_user()
                flash('User Logout')
            else:
                login_user(user,True)
                flash('User Login')
    return render_template('login.html',form=form)

@main.route('/loginrq',methods=['GET','POST'])
@login_required
def loginrq():
    return 'I''m a private url'

@main.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.name.data,password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_token()
        send_email(form.email.data,'Confirm Account','mail/new_user',user=user,token=token)
    return render_template('register.html',form=form)

@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if not current_user.confirmed:
        if current_user.confirm(token):
            flash('Confirm succeed')
        else: 
            flash('Confirm fail')
    return redirect(url_for('main.register'))

@main.route('/post')
def post():
    form=PostForm()
    return render_template('post.html',form=form)
