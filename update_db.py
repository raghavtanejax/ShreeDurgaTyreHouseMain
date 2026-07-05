import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_TWOql4I9AbLz@ep-soft-hat-ath522v4-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE site_settings ADD COLUMN primary_contact_name VARCHAR(100) DEFAULT 'Ashutosh Batra'"))
        db.session.execute(text("ALTER TABLE site_settings ADD COLUMN secondary_contact_name VARCHAR(100) DEFAULT 'Aman'"))
        db.session.commit()
        print('SiteSettings schema updated successfully.')
    except Exception as e:
        print(f'Error: {e}')
