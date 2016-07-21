from app import db
from app.models import User
db.drop_all()
db.create_all()
a = User()
a.password = '123'
hanlin = User(id=1, username='test1', password_hash=a.password_hash)
db.session.add(hanlin)
db.session.commit()
lilijuan = User(id=2, username='test2', password_hash=a.password_hash)
db.session.add(lilijuan)
db.session.commit()

