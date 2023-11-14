from flask import render_template, url_for, request, redirect, session
from flaskapp import *


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'id' in session:
        sender_id = session['id']
        receiver_username = request.form['receiver_username']  # Предполагается, что имя получателя вводится пользователем
        receiver = User.query.filter_by(username=receiver_username).first()

        if receiver:
            message_text = request.form['message']
            new_message = Message(sender_id=sender_id, receiver_id=receiver.id, message=message_text)

            try:
                db.session.add(new_message)
                db.session.commit()
                return "Message sent successfully"
            except:
                return "Error while sending the message"
        else:
            return "Receiver not found"
    else:
        return redirect('/login')


@app.route('/view_messages')
def view_messages():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)
        received_messages = user.received_messages  # Получить все сообщения, которые пользователь получил
        return render_template('messages.html', messages=received_messages)
    else:
        return redirect('/login')
