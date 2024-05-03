from app.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Sring(150))
    content = db.Column(db.Text)
