from flask import Blueprint,render_template,request,flash,url_for,redirect
from flask_login import login_required,current_user
from .models import *
from . import db
views = Blueprint('views', __name__,static_folder='static')

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method=="POST":
        note=request.form.get('note')
        print(note)
        if len(note) < 4:
         flash("note is too short make it long a little!",category="error")
        else:
           addnote=Note(data=note, user_id=current_user.id)
           db.session.add(addnote);
           db.session.commit() 
           flash("Added note successfully",category="success") 

    return render_template('index.html',user=current_user)