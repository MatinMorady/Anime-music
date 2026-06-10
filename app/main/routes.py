from flask import Blueprint, render_template, request
from ..models import Song

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    q = request.args.get("q")
    if q:
        songs = Song.query.filter(Song.title.contains(q)).all()
    else:
        songs = Song.query.all()

    return render_template("index.html", songs=songs)