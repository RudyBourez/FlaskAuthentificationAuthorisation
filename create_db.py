from app import db, app
from app.models import User, Role
from werkzeug.security import generate_password_hash

app.app_context().push()
db.create_all()

new_user = Role(name="User")
new_agent = Role(name="Agent")
new_admin = Role(name="Admin")

db.session.add(new_user)
db.session.add(new_agent)
db.session.add(new_admin)
db.session.commit()

if not User.query.filter(User.email == 'admin@example.com').first():
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('1234'),
        name='Rudy'
    )
    admin.roles.append("Admin")
    admin.roles.append('Agent')
    db.session.add(admin)
    db.session.commit()

if not User.query.filter(User.email == 'user@example.com').first():       
    user = User(
        email="user@example.com",
        password=generate_password_hash('123456'),
        name="User"
    )
    user.roles.append('User')
    user.roles.append('Agent')
    db.session.add(user)
    db.session.commit()