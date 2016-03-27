from hello import db, User
db.drop_all()
db.create_all()
a = User()
a.password = '123'
hanlin = User(id=1, username='hanlin', password_hash=a.password_hash)
db.session.add(hanlin)
db.session.commit()
lilijuan = User(id=2, username='lilijuan', password_hash=a.password_hash)
db.session.add(lilijuan)
db.session.commit()

