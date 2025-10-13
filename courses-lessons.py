from flask import Blueprint, request, jsonify
from database import db
from models import Lessons

lessons_bp = Blueprint("lessons_bp", __name__)

@lessons_bp.route("/courses/lessons", methods=["GET"])
def get_lessons():
    lessons = Lessons.query.all()
    return jsonify([{
        "id": c.id,
        "tittle": c.title,
        "description": c.description,
        "author": c.author,
        "is_published": c.is_published,
        "time_start": c.time_start,
        "time_end": c.time_ebd,
        "amount_tasks": c.amount_tasks,
        "if_done": c.if_done
    } for c in lessons]), 200


@lessons_bp.route("courses/lessons", methods=["POST"])
def create_lesson():
    data = request.get_json()
    new_lesson = Lessons(
        tittle=data["title"],
        description=data.get("description", ""),
        author=data.get("author", "Неизвестен"),
        time_start=data.get("start", "Бессрочно"),
        time_end=data.get("end", "")
    )
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({"message": "Урок успешно создан", "id": new_lesson.id}), 201


@lessons_bp.route("courses/lessons/<int:lesson_id>", methods=["PUT"])
def update_lesson(lesson_id):
    data = request.get_json()
    lesson = Lessons.query.get_or_404(lesson_id)
    lesson.title = data.get("title", lesson.title)
    lesson.description = data.get("description", lesson.description)
    lesson.is_published = data.get("is_published", lesson.is_published)
    lesson.time_start = data.get("start", lesson.start)
    lesson.time_end = data.get("end", lesson.end)
    db.session.commit()
    return jsonify({"message": "Урок успешно обновлен"}), 200


@lessons_bp.route("courses/lessons/<int:lesson_id>", methods=["DELETE"])
def delete_lesson(lesson_id):
    lesson = Lessons.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": "Урок удалён"}), 200