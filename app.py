import os
import secrets
import sqlite3

from flask import Flask, jsonify, render_template, request, session

from progression import calculate_level
from quest_manager import change_quest_duration, create_quest, get_quest, rename_quest
from quest_validation import validate_quest_input
from storage import (
    complete_quest,
    delete_pending_quest,
    initialize_database,
    insert_quest,
    load_progress,
    load_quests,
    update_pending_quest,
)


def create_app(database_path="quests.db"):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        SESSION_COOKIE_SAMESITE="Strict",
    )
    initialize_database(database_path)

    def csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        return session["csrf_token"]

    @app.before_request
    def check_csrf():
        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return None

        origin = request.headers.get("Origin")
        if origin is not None and origin != request.host_url.rstrip("/"):
            return jsonify(error="Request origin is not allowed."), 403

        expected = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token", "")
        if not expected or not secrets.compare_digest(expected.encode(), supplied.encode()):
            return jsonify(error="Refresh the page and try again."), 403

    @app.get("/csrf-token")
    def get_csrf_token():
        response = jsonify(csrfToken=csrf_token())
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/")
    def planner():
        return render_template("planner.html", csrf_token=csrf_token())

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

    @app.get("/progress")
    def progress_detail():
        try:
            progress = load_progress(database_path)
            level = calculate_level(progress["totalXP"])
        except (ValueError, sqlite3.Error):
            app.logger.exception("Could not load progress")
            return jsonify(error="Could not load progress."), 500

        response = jsonify(totalXP=progress["totalXP"], level=level)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.post("/quests/<quest_id>/complete")
    def finish_quest(quest_id):
        if not quest_id.strip():
            return jsonify(error="Enter a quest ID."), 400

        if request.get_data():
            payload = request.get_json(silent=True)
            if not isinstance(payload, dict) or payload:
                return jsonify(error="Send no body or an empty JSON object."), 400

        try:
            result = complete_quest(database_path, quest_id)
        except KeyError:
            return jsonify(error="Quest not found."), 404
        except (ValueError, sqlite3.Error):
            app.logger.exception("Could not complete quest")
            return jsonify(error="Could not complete the quest."), 500

        response = jsonify(result)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.patch("/quests/<quest_id>")
    def patch_quest(quest_id):
        if not quest_id.strip():
            return jsonify(error="Enter a quest ID."), 400

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return jsonify(error="Send a title or duration to update."), 400
        if set(payload) - {"title", "durationMinutes"}:
            return jsonify(error="Only title and durationMinutes can be updated."), 400

        try:
            quests = load_quests(database_path)
            quest = get_quest(quests, quest_id)
        except KeyError:
            return jsonify(error="Quest not found."), 404
        except sqlite3.Error:
            app.logger.exception("Could not load quest for editing")
            return jsonify(error="Could not update the quest."), 500

        if quest["status"] != "pending":
            return jsonify(error="Only pending quests can be edited."), 409

        try:
            title, minutes = validate_quest_input(
                payload.get("title", quest["title"]),
                payload.get("durationMinutes", quest["durationMinutes"]),
            )
        except ValueError as error:
            return jsonify(error=str(error)), 400

        try:
            if "title" in payload:
                quests = rename_quest(quests, quest_id, title)
            if "durationMinutes" in payload:
                quests = change_quest_duration(quests, quest_id, minutes)
            updated = get_quest(quests, quest_id)
            update_pending_quest(database_path, updated, expected_quest=quest)
        except KeyError:
            return jsonify(error="Quest not found."), 404
        except ValueError:
            return jsonify(error="Quest changed or is no longer pending. Reload and try again."), 409
        except sqlite3.Error:
            app.logger.exception("Could not update quest")
            return jsonify(error="Could not update the quest."), 500

        return jsonify(updated)

    @app.delete("/quests/<quest_id>")
    def remove_quest(quest_id):
        if not quest_id.strip():
            return jsonify(error="Enter a quest ID."), 400

        try:
            delete_pending_quest(database_path, quest_id)
        except KeyError:
            return jsonify(error="Quest not found."), 404
        except ValueError:
            return jsonify(error="Only pending quests can be deleted."), 409
        except sqlite3.Error:
            app.logger.exception("Could not delete quest")
            return jsonify(error="Could not delete the quest."), 500

        return jsonify(deleted=quest_id)

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


