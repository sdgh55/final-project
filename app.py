from flask import render_template, url_for, request, redirect, session
from flaskapp import *
from werkzeug.security import generate_password_hash, check_password_hash
from messages import *
from friends import *

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page:" + name + "-" + str(id)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return redirect(url_for("register_user", error="Passwords do not match!"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for("register_user", error="Already registered!"))

        hashed_password = generate_password_hash(password1, method='pbkdf2:sha1')

        new_user = User(username=username, name=name, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        except Exception as e:
            app.logger.error(f"Error while registering: {str(e)}")

    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']

        user = db.session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["authenticated"] = True
            session["id"] = user.id
            session["username"] = user.username
            return redirect('/posts')
        else:
            return render_template("login.html", context="The username or password is incorrect")

    return render_template("login.html", context=None)



@app.route('/update_account/<int:id>', methods=['POST', 'GET'])
def update_account(id):
    user = User.query.get(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.name = request.form['name']
        user.password = generate_password_hash(request.form['password'], method='sha256')

        try:
            db.session.commit()
            return redirect(url_for("user_page", user_id=user.id))
        except:
            return 'Error while updating account'

    return render_template('update_account.html', user=user)





@app.route('/create', methods=['POST', 'GET'])
def create():

    if 'id' in session:
        user_id = session['id']

        if request.method == 'POST':
            title = request.form['title']
            text = request.form['text']

            article = Article(title=title, text=text, user_id=user_id)
            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/posts')

            except:
                return 'Error while adding new post'


        else:
            return render_template('create.html')

    else:
        return redirect('/login')



@app.route('/posts')
def posts():
    if 'id' in session:
        user_id = session['id']
        articles = Article.query.order_by(Article.date.desc()).all()
        return render_template('posts.html', posts=articles)
    else:
        return redirect('/login')



@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


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




if __name__ == "__main__":
        app.run(debug=True)