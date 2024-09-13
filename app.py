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

    # LESSONS... 

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


    # Endpoint for deleting a lesson
@app.route("/lesson/<id>", methods=["DELETE"])
def lesson_delete(id):
    lesson = Lesson.query.get(id)
    db.session.delete(lesson)
    db.session.commit()

    return "That LESSON has now been DELETED"




    # VOCABULARY... 
class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)  # Foreign key to Lesson 
    lesson = db.relationship('Lesson', backref=db.backref('vocab', lazy=True))  # Relationship with Lesson 
    english = db.Column(db.String(40), unique=False)
    basque = db.Column(db.String(40), unique=False)

    def __init__(self, english, basque, lesson_id):
        self.lesson_id = lesson_id
        self.english = english
        self.basque = basque

class VocabSchema(ma.Schema):
    class Meta:
        fields = ('id', 'lesson_id', 'english', 'basque')

vocab_schema = VocabSchema()
vocab_list_schema = VocabSchema(many=True) 


    # endpoint to creating new vocab... 

@app.route('/vocab', methods=["POST"])
def add_vocab():
    lesson_id = request.json['lesson_id']
    english = request.json['english']
    basque = request.json['basque']

    new_vocab = Vocab(english, basque, lesson_id )

    db.session.add(new_vocab)
    db.session.commit()

    tester = Vocab.query.get(new_vocab.id)

    return vocab_schema.jsonify(tester)


    # endpoint to query all vocab 

@app.route('/vocab_list/all', methods=["GET"])
def get_full_vocab_list():
    vocab_list = Vocab.query.all()
    result = vocab_list_schema.dump(vocab_list)
    return jsonify(result)

    # endpoint to query all vocab (in a specified lesson)...

@app.route('/vocab_list/<lesson_id>', methods=["GET"])
def get_vocab_list(lesson_id):
    vocab_list = Vocab.query.filter_by(lesson_id=lesson_id).all()
    result = vocab_list_schema.dump(vocab_list)
    return jsonify(result)



    # Endpoint for querying single vocab

@app.route("/vocab/<id>", methods=["GET"])
def get_vocab(id):
    vocab = Vocab.query.get(id)
    return vocab_schema.jsonify(vocab)


    # Endpoint for updating a vocab line

@app.route("/vocab/<id>", methods=["PUT"])
def vocab_update(id):
    vocab = Vocab.query.get(id)
    lesson_id = request.json['lesson_id']
    english = request.json['english']
    basque = request.json['basque']

    vocab.lesson_id = lesson_id
    vocab.english = english
    vocab.basque = basque

    db.session.commit()
    return vocab_schema.jsonify(vocab)



    # Endpoint for deleting vocab entry

@app.route("/vocab/<id>", methods=["DELETE"])
def vocab_delete(id):
    vocab = Vocab.query.get(id)
    db.session.delete(vocab)
    db.session.commit()

    return "That VOCAB entry has been DELETED"




    # to run the code (when this file is executed)...
if __name__ == '__main__':
    app.run(debug=True)