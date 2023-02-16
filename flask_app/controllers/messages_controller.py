from flask_app import app   
from flask import redirect, session, request
from flask_app.models import message

@app.route("/send_message", methods=['POST'])
def insert_message():
    if "id" in session:
        message_data = {
            "content": request.form["content"],
            "sender_id": session["id"],
            "recipient_id": request.form["user"]
        }
        if message.Message.validate_message(message_data):
            message.Message.insert_message(message_data)
        return redirect("/wall")
    return redirect("/")
