from app import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(60), nullable=False)
    # profile_img = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
        }