import sqlite3

from flask import Flask, jsonify, render_template, request

from quest_manager import create_quest
from quest_validation import validate_quest_input
from storage import initialize_database, insert_quest


def create_app(database_path="quests.db"):
    app = Flask(__name__)
    initialize_database(database_path)

    @app.get("/")
    def planner():
        return render_template("quest_form.html")

    @app.post("/quests")
    def post_quest():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Send a JSON object."), 400

        try:
            title, minutes = validate_quest_input(
                payload.get("title"),
                payload.get("durationMinutes"),
            )
        except ValueError as error:
            return jsonify(error=str(error)), 400

        quest = create_quest([], title, minutes)[0]

        try:
            insert_quest(database_path, quest)
        except sqlite3.Error:
            app.logger.exception("Could not insert quest")
            return jsonify(error="Could not save the quest."), 500

        return jsonify(quest), 201

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8000)