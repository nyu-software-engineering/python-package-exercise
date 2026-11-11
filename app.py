import sqlite3

from flask import Flask, jsonify, render_template, request

from quest_manager import create_quest, get_quest
from quest_validation import validate_quest_input
from storage import initialize_database, insert_quest, load_quests


def create_app(database_path="quests.db"):
    app = Flask(__name__)
    initialize_database(database_path)

    @app.get("/")
    def planner():
        return render_template("quest_form.html")

    @app.get("/quests")
    def quest_list():
        status = request.args.get("status")
        if status not in (None, "pending", "completed"):
            return jsonify(error="Status must be pending or completed."), 400

        try:
            quests = load_quests(database_path, status)
        except sqlite3.Error:
            app.logger.exception("Could not load quests")
            return jsonify(error="Could not load quests."), 500

        return jsonify(quests)

    @app.get("/quests/<quest_id>")
    def quest_detail(quest_id):
        if not quest_id.strip():
            return jsonify(error="Enter a quest ID."), 400

        try:
            quest = get_quest(load_quests(database_path), quest_id)
        except KeyError:
            return jsonify(error="Quest not found."), 404
        except sqlite3.Error:
            app.logger.exception("Could not load quests")
            return jsonify(error="Could not load quests."), 500

        return jsonify(quest)

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
