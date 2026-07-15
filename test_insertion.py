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
    try:
        tyre = Tyre(
            model="Test Model",
            brand="Test Brand",
            category="Car Tyre",
            price=100.0,
            mrp_price=120.0,
            stock=10,
            sku="TESTSKU-1"
        )
        db.session.add(tyre)
        db.session.flush()
        print(f"Flushed tyre ID: {tyre.id}")
        
        tyre_img = TyreImage(tyre_id=tyre.id, image_filename="http://test.com/img.jpg", sequence=0)
        db.session.add(tyre_img)
        db.session.commit()
        print("Success!")
        
        # Cleanup
        db.session.delete(tyre)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
