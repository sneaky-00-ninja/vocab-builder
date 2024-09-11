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

vocab_schema = LessonSchema()
full_vocab_schema = LessonSchema(many=True)





if __name__ == '__main__':
    app.run(debug=True)