from flask import Flask, request, jsonify
from user import UserManager
from user_course import UserCourseManager
from course import CourseManager
from database import Base, engine

# Создаем таблицы при запуске
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# =============================================================================
# МИКРОСЕРВИС ДЛЯ ПОЛЬЗОВАТЕЛЕЙ (Main Page ↔ Auth/Users)
# =============================================================================

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    manager = UserManager()
    success = manager.post(
        email=data["email"],
        password=data["password"],
        role=data.get("role", "user")
    )
    
    if success:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 400

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    manager = UserManager()
    user = manager.get(user_id)
    
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email,
            "role": user.role
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["GET"])
def get_all_users():
    manager = UserManager()
    users = manager.get_all()
    
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "email": user.email,
            "role": user.role
        })
    
    return jsonify(users_list), 200

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    
    manager = UserManager()
    success = manager.edit(
        user_id=user_id,
        new_role=data.get("role"),
        new_email=data.get("email"),
        new_password=data.get("password")
    )
    
    if success:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update user"}), 400

# =============================================================================
# МИКРОСЕРВИС ДЛЯ СВЯЗИ ПОЛЬЗОВАТЕЛЬ-КУРС (Main Page ↔ Courses)
# =============================================================================

@app.route("/user-courses", methods=["POST"])
def enroll_user_to_course():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'course_id' not in data:
        return jsonify({"error": "user_id and course_id are required"}), 400
    
    manager = UserCourseManager()
    success = manager.post(
        user_id=data["user_id"],
        course_id=data["course_id"]
    )
    
    if success:
        return jsonify({"message": "User enrolled in course successfully"}), 201
    else:
        return jsonify({"error": "Failed to enroll user in course"}), 400

@app.route("/users/<int:user_id>/courses", methods=["GET"])
def get_user_courses(user_id):
    manager = UserCourseManager()
    user_courses = manager.get_by_user(user_id)
    
    courses_list = []
    for uc in user_courses:
        courses_list.append({
            "user_course_id": uc.id,
            "user_id": uc.user_id,
            "course_id": uc.course_id
        })
    
    return jsonify(courses_list), 200

@app.route("/user-courses", methods=["DELETE"])
def unenroll_user_from_course():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'course_id' not in data:
        return jsonify({"error": "user_id and course_id are required"}), 400
    
    manager = UserCourseManager()
    success = manager.delete_by_ids(
        user_id=data["user_id"],
        course_id=data["course_id"]
    )
    
    if success:
        return jsonify({"message": "User unenrolled from course successfully"}), 200
    else:
        return jsonify({"error": "Failed to unenroll user from course"}), 400

# =============================================================================
# ДОПОЛНИТЕЛЬНО: ЭНДПОИНТЫ ДЛЯ КУРСОВ
# =============================================================================

@app.route("/courses", methods=["GET"])
def get_all_courses():
    manager = CourseManager()
    courses = manager.get_all()
    
    courses_list = []
    for course in courses:
        courses_list.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "author": course.author,
            "is_published": course.is_published
        })
    
    return jsonify(courses_list), 200

@app.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    manager = CourseManager()
    success = manager.post(
        title=data["title"],
        description=data.get("description", ""),
        author=data.get("author", "unknown")
    )
    
    if success:
        return jsonify({"message": "Course created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create course"}), 400

@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    manager = CourseManager()
    course = manager.get(course_id)
    
    if course:
        return jsonify({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "author": course.author,
            "is_published": course.is_published
        }), 200
    else:
        return jsonify({"error": "Course not found"}), 404

if __name__ == "__main__":
    print("Микросервис запущен: http://localhost:5000")
    print("Эндпоинты:")
    print("  POST   /users - создать пользователя")
    print("  GET    /users - все пользователи") 
    print("  GET    /users/<id> - пользователь по ID")
    print("  PUT    /users/<id> - изменить пользователя")
    print("  POST   /user-courses - записать на курс")
    print("  GET    /users/<id>/courses - курсы пользователя")
    print("  DELETE /user-courses - отписать от курса")
    print("  GET    /courses - все курсы")
    print("  POST   /courses - создать курс")
    print("  GET    /courses/<id> - курс по ID")
    
    app.run(debug=True, port=5000)