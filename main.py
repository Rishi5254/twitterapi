from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urlunparse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allPosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
API_KEY = 'GiaHIHhiod686@gRN23'


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    post = db.Column(db.String(250), nullable=False, )

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


db.create_all()


@app.route('/')
def homepage():
    return redirect('https://documenter.getpostman.com/view/18998972/UVXomZWZ#0395bbe2-0f48-4481-8276-243bb8e4b59d')


@app.route('/all', methods=['GET', 'POST'])
def all_posts():
    if request.method == 'GET':
        data = db.session.query(Posts).all()
        posts = [n.to_dict() for n in data]
        return jsonify(posts=posts)


@app.route('/search', methods=['GET', 'POST'])
def search():
    name = request.args.get('name')
    if request.method == 'GET':
        data = db.session.query(Posts).filter_by(name=name).all()
        if len(data) == 0:
            return jsonify(error={"not found": "No post with that Name "})
        else:
            posts = [n.to_dict() for n in data]
            return jsonify(posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def add():
    api_key = request.args.get('api_key')
    name = request.args.get('name')
    post = request.args.get('post')
    if api_key == API_KEY:
        if name and post:
            if len(post) > 10000:
                return jsonify(error={"over limit": "the post should not be over 10000 letters"})
            else:
                data = Posts(name=name, post=post)
                db.session.add(data)
                db.session.commit()
                return jsonify(post={"success": "posted successfully"})
        else:
            return jsonify(post={"error": "name and post is mandatory"})
    elif api_key == None:
        return jsonify(post={"api_key error": "Api key mandatory"})
    else:
        return jsonify(post={"api_key error": "Api key invalid"})


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    api_key = request.args.get('api_key')
    user_id = request.args.get('id')
    if api_key == API_KEY:
        if user_id:
            data = db.session.query(Posts).get(user_id)
            if data:
                db.session.delete(data)
                db.session.commit()
                return jsonify(post={"success": "Deleted successfully"})
            else:
                return jsonify(error={"Not Found": "Sorry the post with that id was not found in the database."})
        else:
            return jsonify(error='you are not authorized to delete')
    elif api_key == None:
        return jsonify(post={"api_key error": "Api key mandatory"})
    else:
        return jsonify(post={"api_key error": "Api key invalid"})


@app.route('/update', methods=['GET', 'PATCH'])
def update():
    api_key = request.args.get('api_key')
    user_id = request.args.get('id')
    new_post = request.args.get('new_post')
    data = db.session.query(Posts).get(user_id)
    if api_key == API_KEY:
        if user_id and new_post:
            if data:
                data.post = new_post
                db.session.commit()
                return jsonify(post={"success": "updated successfully"})
            else:
                return jsonify(error={"Not Found": "Sorry the post with that id was not found in the database."})
        else:
            return jsonify(post={"error": "id and new_post is mandatory"})
    elif api_key == None:
        return jsonify(post={"api_key error": "Api key mandatory"})
    else:
        return jsonify(post={"api_key error": "Api key invalid"})


if __name__ == '__main__':
    app.run(debug=True)