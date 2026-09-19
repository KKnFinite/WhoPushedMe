from __future__ import annotations

import os
from typing import Final

from flask import Flask, jsonify, redirect, render_template, send_from_directory, url_for

from who_pushed_me.api import api

APP_VERSION: Final = "0.3.0"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DATABASE_URL"] = (
        os.getenv("DATABASE_URL")
        or os.getenv("DATABASE_URL_UNPOOLED", "")
    )
    app.register_blueprint(api)

    @app.get("/")
    def home():
        return render_template("home.html", version=APP_VERSION)

    @app.get("/new-round")
    def new_round():
        return redirect(url_for("home"))

    @app.post("/round-preview")
    def round_preview():
        return redirect(url_for("home"))

    @app.get("/service-worker.js")
    def service_worker():
        response = send_from_directory(
            app.static_folder,
            "service-worker.js",
            mimetype="application/javascript",
        )
        response.headers["Cache-Control"] = "no-cache"
        return response

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
