from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://build-a-blog:@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    likes = db.Column(db.Integer)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.likes = 0



@app.route('/')
def index():
    return render_template('base.html')

@app.route("/blog")
def blog():
    posts = Post.query.all()
    return render_template('posts.html', title="Blog", posts=posts)  
 
@app.route('/post_form', methods=["POST", "GET"])   
def post_form():
    if request.method == "POST":
        postit = request.form["postit"]
        new_post = Post(postit, "")
        db.session.add(new_post)
        db.session.commit()

    return render_template("blog.html", title="New Post")

@app.route("/delete_post", methods=['POST', 'GET'])
def delete():
    if request.method == "POST":
        post_id = int(request.form["post-id"])
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
    return redirect('/blog')
if __name__ == '__main__':
    app.run()