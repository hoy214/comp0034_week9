from werkzeug.security import generate_password_hash, check_password_hash

from my_app import db


class User(db.Model):
    # Uncomment the following line and remove all the field definitions if you want to experiment with
    # reflection
    # __table__ = db.Model.metadata.tables['user']
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.firstname} {self.lastname} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
