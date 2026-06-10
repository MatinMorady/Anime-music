import os
import uuid
from flask import Blueprint, render_template, request, redirect, send_from_directory
from flask_login import login_required, current_user
from ..models import db, Song, Like, Comment

music_bp = Blueprint("music", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@music_bp.route("/upload", methods=["GET","POST"])
@login_required
def upload():
    if not current_user.is_admin:
        return "No access"

    if request.method == "POST":
        file = request.files["file"]
        filename = str(uuid.uuid4()) + "_" + file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        song = Song(title=file.filename, filename=filename)
        db.session.add(song)
        db.session.commit()

        return redirect("/")
    return render_template("upload.html")


@music_bp.route("/song/<int:id>")
def song(id):
    song = Song.query.get_or_404(id)
    song.views += 1
    db.session.commit()

    likes = Like.query.filter_by(song_id=id).count()
    comments = Comment.query.filter_by(song_id=id).all()

    return render_template("song.html", song=song, likes=likes, comments=comments)


@music_bp.route("/like/<int:id>")
@login_required
def like(id):
    exist = Like.query.filter_by(user_id=current_user.id, song_id=id).first()
    if not exist:
        db.session.add(Like(user_id=current_user.id, song_id=id))
        db.session.commit()
    return redirect(f"/song/{id}")


@music_bp.route("/comment/<int:id>", methods=["POST"])
@login_required
def comment(id):
    c = Comment(user_id=current_user.id, song_id=id, text=request.form["text"])
    db.session.add(c)
    db.session.commit()
    return redirect(f"/song/{id}")


@music_bp.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)