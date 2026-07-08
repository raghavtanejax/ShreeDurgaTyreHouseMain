from app import app, db
from models import Tyre
with app.app_context():
    print(f"Total tyres: {Tyre.query.count()}")
    for t in Tyre.query.all():
        print(f"ID: {t.id}, Category: {t.category}")
