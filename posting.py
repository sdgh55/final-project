from werkzeug.utils import secure_filename

from flaskapp import *
from flask import render_template, url_for, request, redirect, session, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os



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
def update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']


        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Error while updating new post'


    else:
        article = Article.query.get(id)
        return render_template('post_update.html', posts=article)

