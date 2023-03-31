from flask import Flask, render_template,redirect,session,request
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.user import User


@app.route('/paintings/new')
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("new.html", user=User.get_by_id(data))

@app.route('/painting/add',methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_show(request.form):
        data = {
        "id":session['user_id']
    }
        return render_template("new.html", user=User.get_by_id(data))
    data ={ 
        "title": request.form['title'],
        "description": request.form['description'],
        "price": request.form['price'],
        "users_id": session['user_id']
    }
    id = Painting.save(data)
    return redirect('/dashboard')

@app.route('/painting/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }    
    user_data = {
        "id":session['user_id']
    }
    return render_template("painting_details.html",painting=Painting.get_all_by_id(data),user=User.get_by_id(user_data))

@app.route('/edit/painting/<int:id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_painting.html",painting=Painting.get_all_by_id(data),user=User.get_by_id(user_data))

@app.route('/painting/update',methods=['POST'])
def update_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_show(request.form):
        user_data = {
        "id":session['user_id']
    }
        data = {
        "id":request.form['id']
    }
        return render_template("edit_painting.html",painting=Painting.get_all_by_id(data),user=User.get_by_id(user_data))
    data = {
        "title": request.form['title'],
        "description": request.form['description'],        
        "price": request.form['price'],
        "users_id": session['user_id'],
        "id": request.form['id']
    }
    Painting.update(data)
    return redirect('/dashboard')

@app.route('/delete/painting/<int:id>')
def delete_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Painting.delete(data)
    return redirect('/dashboard')