from app import app, db, bcrypt
from models import User

def init_db():
    with app.app_context():
        db.create_all()
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = User(username='admin', password_hash=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created (admin / admin123).")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
