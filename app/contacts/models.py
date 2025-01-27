from app import db

# Додаткова модель - Група контактів
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Group {self.name}>"

# Основна модель - Контакт
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    group = db.relationship('Group', backref=db.backref('contacts', lazy=True))

    def __repr__(self):
        return f"<Contact {self.name}>"
