import os

# Ensure the app connects to your remote Neon database
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_TWOql4I9AbLz@ep-soft-hat-ath522v4-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

from app import app, bcrypt
from models import db, User

def update_admin_credentials(old_username, new_username, new_password):
    with app.app_context():
        user = User.query.filter_by(username=old_username).first()
        
        if not user:
            print(f"Error: Could not find user with username '{old_username}'.")
            return
            
        user.username = new_username
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        
        print("Success! Admin credentials updatsed.")
        print(f"New Login ID: {new_username}")

if __name__ == '__main__':
    # REPLACE THESE VALUES WITH YOUR DESIRED LOGIN ID AND PASSWORD
    CURRENT_USERNAME = 'OwnerAshu5'
    NEW_USERNAME = 'OwnerAshu5'
    NEW_PASSWORD = 'Prayag5@Sejal!*'
    
    update_admin_credentials(CURRENT_USERNAME, NEW_USERNAME, NEW_PASSWORD)
