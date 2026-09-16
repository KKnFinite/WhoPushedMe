from __future__ import annotations

import os
from typing import Final

from flask import Flask, jsonify, redirect, render_template, request, url_for

APP_VERSION: Final = "0.1.0"
VALID_MODES: Final = {"individual", "scramble"}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL", "")

    @app.get("/")
    def home():
        return render_template("home.html", version=APP_VERSION)

    @app.get("/new-round")
    def new_round():
        mode = request.args.get("mode", "individual").strip().lower()
        if mode not in VALID_MODES:
            return redirect(url_for("home"))
        return render_template("new_round.html", mode=mode, error=None, values={})

    @app.post("/round-preview")
    def round_preview():
        mode = request.form.get("mode", "").strip().lower()
        if mode not in VALID_MODES:
            return redirect(url_for("home"))

        course = request.form.get("course", "").strip()
        holes_raw = request.form.get("holes", "18")
        holes = 9 if holes_raw == "9" else 18
        players = [
            request.form.get(f"player_{index}", "").strip()
            for index in range(1, 5)
        ]
        players = [player for player in players if player]

        values = {
            "course": course,
            "holes": str(holes),
            **{f"player_{index}": request.form.get(f"player_{index}", "") for index in range(1, 5)},
        }

        minimum_players = 2 if mode == "scramble" else 1
        if not course:
            return render_template(
                "new_round.html",
                mode=mode,
                error="Give us a course name. Even bad decisions need an address.",
                values=values,
            ), 400
        if len(players) < minimum_players:
            message = (
                "A scramble needs at least two victims."
                if mode == "scramble"
                else "Add at least one golfer willing to accept public ridicule."
            )
            return render_template(
                "new_round.html", mode=mode, error=message, values=values
            ), 400

        return render_template(
            "round_preview.html",
            mode=mode,
            course=course,
            holes=holes,
            players=players,
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "service": "who-pushed-me-scorecard",
                "version": APP_VERSION,
                "database_configured": bool(app.config["DATABASE_URL"]),
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
