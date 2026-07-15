import os
from flask import Flask, request
from app import app
from models import db, User, Tyre
from flask_login import login_user
from io import BytesIO

with app.app_context():
    # create a test user if not exists
    user = User.query.filter_by(username='testadmin').first()
    if not user:
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt(app)
        user = User(username='testadmin', password_hash=bcrypt.generate_password_hash('test').decode('utf-8'))
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True
            
        # Try to post to inventory
        data = {
            'model': 'Test Model',
            'brand': 'MRF',
            'category': 'Car Tyre',
            'price': '100',
            'stock': '10',
            'images': [(BytesIO(b"dummy image data"), 'test.jpg'), (BytesIO(b"dummy image data"), 'test2.jpg')]
        }
        response = client.post('/admin/inventory', data=data, content_type='multipart/form-data')
        print("Status code:", response.status_code)
        if response.status_code == 500:
            print("500 ERROR CAUSE:")
            print(response.get_data(as_text=True))
