import os

# Set Vercel env var so app.py picks it up
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_TWOql4I9AbLz@ep-soft-hat-ath522v4-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

from app import app
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_neon():
    with app.app_context():
        # Create all tables in Neon
        print("Creating tables in Neon...")
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            hashed_pw = bcrypt.generate_password_hash('password').decode('utf-8')
            new_admin = User(username='admin', password_hash=hashed_pw)
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created (username: admin, password: password)")
        else:
            print("Admin user already exists.")
            
        print("Neon Database successfully initialized!")

if __name__ == '__main__':
    init_neon()
