from flask import Blueprint,render_template,request,flash,url_for,redirect
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . views import *
from . import db
from .models import User
# making the blueprint.. here
auths=Blueprint('auths',__name__)



@auths.route('/login', methods=['POST','GET'])
def login ():
    if request.method=="POST":
        email=request.form.get('email');
    
        password=request.form.get('password');

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("YOu have succesfully loged in",category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
             flash("Incorrect Password ",category="error")
        else:
         
         flash("Email does not exits",category="error")
    
    return render_template('login.html',user=current_user)
@auths.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auths.login'))
@auths.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method=="POST":
        print(request.form)
        email=request.form.get('email')
        first_name=request.form.get('firstname');
        password=request.form.get('password');
        confirm_password=request.form.get('confirm-password');
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exits try another one",category="error")
        elif len(first_name) < 5:
            flash("first Nam must be at least 5 character",category="error")
        elif len(password)<5:
            flash("must must be at least 5 character",category="error")
        
        elif password != confirm_password:
        
            flash("Password doesn't matched",category="error")
        else:
            create_user=User(email=email,first_name=first_name,password=generate_password_hash(password, method='sha256'))
            
            db.session.add(create_user);
            db.session.commit()
            flash("successfully Account Created",category="success")
            
            # flash(" Give differenet email",category="success")
            # return redirect(url_for('auths.sign_up'))
            
            return redirect(url_for('auths.login'))
    

    return render_template('sign-up.html',user=current_user)

  