import os
from flask import Flask
from models import db, Tyre, TyreImage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

if os.environ.get('DATABASE_URL'):
    db_url = os.environ.get('DATABASE_URL')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("Creating TyreImage table...")
    TyreImage.__table__.create(db.engine, checkfirst=True)
    
    print("Migrating existing tyre images to TyreImage table...")
    tyres = Tyre.query.all()
    count = 0
    for tyre in tyres:
        if tyre.image_filename:
            # Check if it already exists to avoid duplicates if run multiple times
            existing = TyreImage.query.filter_by(tyre_id=tyre.id, image_filename=tyre.image_filename).first()
            if not existing:
                new_img = TyreImage(tyre_id=tyre.id, image_filename=tyre.image_filename, sequence=0)
                db.session.add(new_img)
                count += 1
    
    db.session.commit()
    print(f"Migration completed. {count} images migrated.")
