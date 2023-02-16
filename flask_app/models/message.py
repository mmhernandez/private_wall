from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "private_wall"

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.sender_id = data["sender_id"]
        self.recipient_id = data["recipient_id"]
        self.sender = None
        self.recipent = None

    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data["content"]) < 1:
            flash("Message cannot be blank", "message")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_by_user_with_sender(cls, data):
        query = '''
            SELECT * 
            FROM messages M
            LEFT JOIN users SU on M.sender_id = SU.id
            LEFT JOIN users RU on M.recipient_id = SU.id
            WHERE RU.id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        messages = []
        for row in results:
            message_obj = cls(row)
            sender_info = {
                "id": row["SU.id"],
                "first_name": row["SU.first_name"],
                "last_name": row["SU.last_name"],
                "email": row["SU.email"],
                "password": row["SU.password"],
                "created_at": row["SU.created_at"],
                "updated_at": row["SU.updated_at"]
            }
            message_obj.sender = user.User(sender_info)
            recipient_info = {
                "id": row["RU.id"],
                "first_name": row["RU.first_name"],
                "last_name": row["RU.last_name"],
                "email": row["RU.email"],
                "password": row["RU.password"],
                "created_at": row["RU.created_at"],
                "updated_at": row["RU.updated_at"]
            }
            message_obj.recipent = user.User(recipient_info)
            messages.append(message_obj)
        return messages

    @classmethod
    def insert_message(cls, data):
        query = '''
            INSERT INTO messages (content, sender_id, recipient_id)
            VALUES (%(content)s, %(sender_id)s, %(recipient_id)s);
        '''
        connectToMySQL(db).query_db(query, data)