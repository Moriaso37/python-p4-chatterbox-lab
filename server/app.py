from flask import Flask, request, jsonify
from app import db
from models import Message  # Adjusted import for Message model

app = Flask(__name__)
# app config, etc.

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200


@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json() or request.form
    new_message = Message(
        body=data.get("body"),
        username=data.get("username")
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201


@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json() or request.form
    message = Message.query.get_or_404(id)
    message.body = data.get("body", message.body)
    db.session.commit()
    return jsonify(message.to_dict()), 200


@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return "", 204
