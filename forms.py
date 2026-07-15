from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, SelectField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TyreForm(FlaskForm):
    model = StringField('Model', validators=[Optional(), Length(max=150)])
    brand = SelectField('Brand', choices=[('APOLLO', 'APOLLO'), ('BIRLA', 'BIRLA'), ('CEAT', 'CEAT'), ('JK', 'JK'), ('MRF', 'MRF'), ('Other', 'Other')], validators=[Optional()])
    custom_brand = StringField('Custom Brand', validators=[Optional(), Length(max=150)])
    category = SelectField('Category', choices=[('Bike / Scooter', 'Bike / Scooter'), ('Car Tyre', 'Car Tyre'), ('Truck/Bus (All Commercial Tyre)', 'Truck/Bus (All Commercial Tyre)'), ('Other', 'Other')], validators=[Optional()])
    mrp_price = FloatField('MRP Price (₹)', validators=[Optional()])
    price = FloatField('Price (₹)', validators=[Optional()])
    stock = IntegerField('Stock Level', validators=[Optional()])
    sku = StringField('SKU', validators=[Optional(), Length(max=50)])
    images = MultipleFileField('Tyre Images', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp', 'avif', 'heic', 'heif', 'bmp', 'tiff'], 'Images only!')])
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
    home_shop_image = FileField('Home Shop Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'avif', 'heic', 'heif'], 'Images only!')])
    truck_category_image = FileField('Truck Category Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'avif', 'heic', 'heif'], 'Images only!')])
    car_category_image = FileField('Car Category Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'avif', 'heic', 'heif'], 'Images only!')])
    bike_category_image = FileField('Bike Category Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'avif', 'heic', 'heif'], 'Images only!')])
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
