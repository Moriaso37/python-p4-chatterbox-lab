from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Message

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/messages", methods=["GET"])
    def get_messages():
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200

    @app.route("/messages", methods=["POST"])
    def create_message():
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username")
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

    @app.route("/messages/<int:id>", methods=["PATCH"])
    def update_message(id):
        data = request.get_json()
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

    return app

# Only for development server usage
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
