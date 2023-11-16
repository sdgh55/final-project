from flask import render_template, url_for, request, redirect, session
from flaskapp import *


@app.route('/my_friends')
def my_friends():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)

        friends = (Friendship.query.filter(
            (Friendship.user_id == user_id) | (Friendship.user_id == user_id))
            .filter(Friendship.status == "accepted").all()
        )
        return render_template('friends.html', friends=friends)
    else:
        return redirect('/login')



@app.route('/add_friend', methods=['POST'])
def add_friend():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)

        friend_username = request.form.get('friend_username')
        friend = User.query.filter_by(username=friend_username).first()

        if friend:
            #checking friendship
            existing_friendship = Friendship.query.filter_by(user_id=user.id, friend_id=friend.id).first()
            if existing_friendship:
                return redirect('/friends')


            new_friendship = Friendship(user_id=user.id, friend_id=friend.id, status='pending')

            try:
                db.session.add(new_friendship)
                db.session.commit()
                return redirect('/friends')
            except:
                return 'Error while adding friend'

        else:
            return "Friend not found"

    else:
        return redirect('/login')


@app.route('/friends')
def view_friends():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)
        friendships = user.friends.filter_by(status='accepted').all()
        #friends = [friendships.friend for friendship in friendships]

        return render_template('friends.html', friendships=friendships)

    else:
        return redirect('/login')


@app.route('/friend_requests')
def view_friend_requests():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)

        friend_requests = Friendship.query.filter_by(friend_id=user_id, status='pending').all()

        return render_template('friend_requests.html', friend_requests=friend_requests)

    else:
        return redirect('/login')



@app.route('/accept_friend/<int:request_id>', methods=['POST', 'GET'])
def accept_friend(request_id):
    friendship_request = Friendship.query.get(request_id)

    if friendship_request:
        friendship_request.status = 'accepted'
        db.session.commit()

    return redirect('/friend_requests')
@app.route('/decline_friend/<int:request_id>', methods=['POST', 'GET'])
def decline_friend(request_id):
    friendship_request = Friendship.query.get(request_id)

    if friendship_request:
        friendship_request.status = 'declined'
        db.session.commit()

    return redirect('/friend_requests')