from flask import render_template, redirect, url_for, request, session
from flaskapp import *




@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/chat/<int:receiver_id>')
def chat(receiver_id):
    if 'id' in session:
        user_id = session['id']
        receiver = User.query.get(receiver_id)

        if receiver:
            # Generate a unique conversation ID using user IDs
            conversation_id = f"{user_id}_{receiver_id}"

            # Retrieve messages for the conversation
            messages = Chat.query.filter_by(conversation_id=conversation_id).all()

            return render_template('chat.html', receiver=receiver, conversation_id=conversation_id, messages=messages)
        else:
            return render_template('error.html', error='User not found')

    else:
        return redirect('/login')


@socketio.on('message')
def handle_message(msg):
    print('Message:', msg)
    sender_id = msg['sender_id']
    content = msg['content']
    receiver_id = msg['receiver_id']

    # Generate conversation_id based on user IDs
    user_ids = sorted([sender_id, receiver_id])
    conversation_id = '_'.join(map(str, user_ids))

    # Save the message to the database
    message = Chat(content=content, sender_id=sender_id, receiver_id=receiver_id, conversation_id=conversation_id)
    db.session.add(message)
    db.session.commit()

    # Broadcast the message to all clients in the conversation
    socketio.emit('message', {
        'content': msg['content'],
        'sender': User.query.get(sender_id).name,
    }, room=conversation_id)


@socketio.on('join')
def handle_join(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']

    # Generate conversation_id based on user IDs
    user_ids = sorted([sender_id, receiver_id])
    conversation_id = '_'.join(map(str, user_ids))

    # Join the conversation room
    join_room(conversation_id)
    print(f'User {sender_id} joined conversation {conversation_id}')


@socketio.on('leave')
def handle_leave(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']

    # Generate conversation_id based on user IDs
    user_ids = sorted([sender_id, receiver_id])
    conversation_id = '_'.join(map(str, user_ids))

    # Leave the conversation room
    leave_room(conversation_id)
    print(f'User {sender_id} left conversation {conversation_id}')
