from flask import render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename

from flaskapp import *
import os


@app.route('/user_page/<int:current_user_id>', methods=['GET', 'POST'])
def user_page(current_user_id):
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(current_user_id)

        if user:
            return render_template('user_page.html', user=user)
        else:
            return render_template('error.html', error='User not found')
    else:
        return redirect('/login')

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)

        if user:
            if request.method == 'POST':
                user.name = request.form['name']
                user.username = request.form['username']
                user.about_me = request.form['about_me']
                user.email = request.form['email']


                if 'profile_image' in request.files:
                    file = request.files['profile_image']

                    if file.filename != '' and allowed_file(file.filename):

                        # Генерация уникального имени файла
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename)

                        # Сохранение файла на сервере
                        file.save(file_path)

                        # Сохранение пути к файлу изображения в базе данных
                        user.profile_image = file_path.replace('\\', '/')

                db.session.commit()

                return redirect('/user_page/' + str(user_id))

            else:
                return render_template('edit_user.html', user=user)
        else:
            return render_template('error.html', error='User not found')
    else:
        return redirect('/login')

def allowed_file(filename):
    # Проверка, является ли файл изображением
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
