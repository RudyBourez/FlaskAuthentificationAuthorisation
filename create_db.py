from app import db, create_app
from app.models import User, Role
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()
db.create_all()

if not User.query.filter(User.email == 'admin@example.com').first():
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('1234'),
        name='Rudy'
    )
    admin.roles.append(Role(name='Admin'))
    admin.roles.append(Role(name='Agent'))
    db.session.add(admin)
    db.session.commit()

if not User.query.filter(User.email == 'user@example.com').first():       
    user = User(
        email="user@example.com",
        password=generate_password_hash('123456'),
        name="User"
    )
    user.roles.append(Role(name='User'))
    db.session.add(user)
    db.session.commit()