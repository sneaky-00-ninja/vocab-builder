from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hey Flasky McFlaskface!"


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=False)
    description = db.Column(db.String(80), unique=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

class LessonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

lesson_schema = LessonSchema()
lesson_list_schema = LessonSchema(many=True)


    # endpoint to creating new lesson... 
@app.route('/lesson', methods=["POST"])
def add_lesson():
    title = request.json['title']
    description = request.json['description']

    new_lesson = Lesson(title, description)

    db.session.add(new_lesson)
    db.session.commit()

    tester = Lesson.query.get(new_lesson.id)

    return lesson_schema.jsonify(tester)


    # endpoint to query all lessons...
@app.route('/lesson_list', methods=["GET"])
def get_lesson_listb():
    lesson_list = Lesson.query.all()
    result = lesson_list_schema.dump(lesson_list)
    return jsonify(result)



    # Endpoint for querying a single lesson
@app.route("/lesson/<id>", methods=["GET"])
def get_lesson(id):
    lesson = Lesson.query.get(id)
    return lesson_schema.jsonify(lesson)


    # Endpoint for updating a lesson
@app.route("/lesson/<id>", methods=["PUT"])
def lesson_update(id):
    lesson = Lesson.query.get(id)
    title = request.json['title']
    description = request.json['description']

    lesson.title = title
    lesson.description = description

    db.session.commit()
    return lesson_schema.jsonify(lesson)


    # Endpoint for deleting a record
@app.route("/lesson/<id>", methods=["DELETE"])
def lesson_delete(id):
    lesson = Lesson.query.get(id)
    db.session.delete(lesson)
    db.session.commit()

    return "That lesson has now been deleted"
    # alternativly showed the deleted item... return lesson_schema.jsonify(lesson)


    # to run the code (when this file is executed)...
if __name__ == '__main__':
    app.run(debug=True)