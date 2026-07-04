import os
from werkzeug.datastructures import FileStorage
from io import BytesIO
from wtforms import Form
from flask_wtf.file import FileField, FileAllowed

class F(Form):
    image = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])

fs1 = FileStorage(stream=BytesIO(b''), filename='')
f1 = F(image=fs1)
f1.validate()
print("Empty file errors:", f1.errors)

fs2 = FileStorage(stream=BytesIO(b'data'), filename='test.HEIC')
f2 = F(image=fs2)
f2.validate()
print("HEIC file errors:", f2.errors)

fs3 = FileStorage(stream=BytesIO(b'data'), filename='test.JPG')
f3 = F(image=fs3)
f3.validate()
print("JPG file errors:", f3.errors)
