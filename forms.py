from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TyreForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired(), Length(max=150)])
    brand = SelectField('Brand', choices=[('MRF', 'MRF'), ('Apollo', 'Apollo'), ('CEAT', 'CEAT'), ('Michelin', 'Michelin'), ('Bridgestone', 'Bridgestone'), ('Other', 'Other')], validators=[DataRequired()])
    category = SelectField('Category', choices=[('Bike & Scooter', 'Bike & Scooter'), ('Car & SUV', 'Car & SUV'), ('Truck & Crane', 'Truck & Crane'), ('Other', 'Other')], validators=[DataRequired()])
    price = FloatField('Price (₹)', validators=[DataRequired()])
    stock = IntegerField('Stock Level', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired(), Length(max=50)])
    image = FileField('Tyre Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp', 'avif', 'heic', 'heif', 'bmp', 'tiff'], 'Images only!')])
    submit = SubmitField('Save Tyre')

class QuoteForm(FlaskForm):
    full_name = StringField('FULL NAME', validators=[DataRequired(), Length(max=150)])
    phone = StringField('PHONE NUMBER', validators=[DataRequired(), Length(max=50)])
    vehicle_type = SelectField('VEHICLE / TYRE TYPE', choices=[('MRF', 'MRF'), ('Apollo', 'Apollo'), ('Birla', 'Birla'), ('Other', 'Other')], validators=[DataRequired()])
    message = StringField('MESSAGE', validators=[DataRequired()])
    submit = SubmitField('Send Request')

class SettingsForm(FlaskForm):
    primary_contact_name = StringField('Primary Contact Name', validators=[DataRequired(), Length(max=100)])
    primary_contact = StringField('Primary Contact', validators=[DataRequired(), Length(max=50)])
    secondary_contact_name = StringField('Secondary Contact Name', validators=[Length(max=100)])
    secondary_contact = StringField('Secondary Contact', validators=[Length(max=50)])
    physical_address = StringField('Physical Address', validators=[DataRequired()])
    google_maps_url = StringField('Google Maps URL', validators=[DataRequired(), Length(max=255)])
    hindi_english_toggle = BooleanField('Hindi / English Toggle')
    submit = SubmitField('Save Changes')

class DispatchForm(FlaskForm):
    customer_name = StringField('Customer / Dealer Name', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=50)])
    destination = StringField('Destination / Address', validators=[DataRequired(), Length(max=255)])
    tyre_details = StringField('Tyres Sent (e.g. 2x MRF ZLX)', validators=[DataRequired()])
    total_amount = FloatField('Total Price (₹)', default=0.0)
    amount_received = FloatField('Amount Received (₹)', default=0.0)
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Dispatched', 'Dispatched'), ('Delivered', 'Delivered')], default='Pending')
    submit = SubmitField('Record Dispatch')
