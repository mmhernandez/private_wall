from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "private_wall"

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_by = data["created_by"]
        self.updated_by = data["updated_by"]
        self.sender_id = data["sender_id"]
        self.recipient_id = data["recipient_id"]
        self.sender = []
        self.recipent = []

    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data["content"]) < 1:
            flash("Message cannot be blank", "message")
            is_valid = False
        return is_valid