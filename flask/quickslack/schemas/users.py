from quickslack.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(24), unique=True, index=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        pass
