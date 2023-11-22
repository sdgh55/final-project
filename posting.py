from werkzeug.utils import secure_filename
from flask import send_from_directory

from flaskapp import *
from flask import render_template, url_for, request, redirect, session, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os

from user_page import allowed_file


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Create Post')


@app.route('/create', methods=['POST', 'GET'])
def create():
    form = ArticleForm()

    if 'id' in session:
        user_id = session['id']

        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data

            # Обработка фото
            if form.image.data:
                file = form.image.data

                # Папка для сохранения загруженных изображений
                upload_folder = app.config['UPLOAD_FOLDER_POST_IMAGE']
                os.makedirs(upload_folder, exist_ok=True)

                # Генерация уникального имени файла
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)

                # Сохранение файла на сервере
                file.save(file_path)

                # Сохранение пути к файлу изображения в базе данных
                image_path = file_path
            else:
                flash("error while adding post image")
                image_path = None

            # Сохранение поста в базе данных
            article = Article(title=title, text=text, image_path=image_path, user_id=user_id)
            db.session.add(article)
            db.session.commit()

            return redirect('/posts')

        return render_template('create.html', form=form)

    return redirect('/login')



@app.route('/posts')
def posts():
    if 'id' in session:
        user_id = session['id']
        articles = Article.query.order_by(Article.date.desc()).all()
        return render_template('posts.html', posts=articles)
    else:
        return redirect('/login')


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", post=article)

@app.route('/static/images/posts/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_POST_IMAGE'], filename)

@app.route('/posts/<int:id>/del')
def delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error while deleting post"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_post(id):
    article = Article.query.get(id)
    form = ArticleForm(obj=article)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(article)

        # Обработка загрузки нового изображения
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER_POST_IMAGE'], filename)
                image.save(image_path)
                article.image_path = image_path

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Error while updating new post'

    return render_template('post_update.html', form=form)