from flask import render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename

from flaskapp import *
import os


@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)

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
                # Обработка данных, отправленных пользователем для редактирования профиля
                user.name = request.form['name']
                user.username = request.form['username']

                if 'profile_image' in request.files:
                    file = request.files['profile_image']

                    if file.filename != '' and allowed_file(file.filename):

                        # Генерация уникального имени файла
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename)

                        # Сохранение файла на сервере
                        file.save(file_path)

                        # Сохранение пути к файлу изображения в базе данных
                        user.profile_image = file_path

                db.session.commit()

                return redirect('/user_page')

            else:
                return render_template('edit_user.html', user=user)
        else:
            return render_template('error.html', error='User not found')
    else:
        return redirect('/login')

def allowed_file(filename):
    # Проверка, является ли файл изображением
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
