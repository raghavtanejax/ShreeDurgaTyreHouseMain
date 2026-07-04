import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Tyre, QuoteRequest
from forms import LoginForm, TyreForm, QuoteForm
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreedurgatyrehouse_super_secret_key'

if os.environ.get('VERCEL') == '1':
    import shutil
    db_path = '/tmp/app.db'
    src_db = os.path.join(app.instance_path, 'app.db')
    if not os.path.exists(db_path) and os.path.exists(src_db):
        shutil.copyfile(src_db, db_path)
    # Absolute path requires four slashes
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context Processor for injecting into all templates
@app.context_processor
def inject_now():
    return {'year': 2026}

# PUBLIC ROUTES

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = QuoteRequest(
            full_name=form.full_name.data,
            phone=form.phone.data,
            vehicle_type=form.vehicle_type.data,
            message=form.message.data
        )
        db.session.add(quote)
        db.session.commit()
        flash('Your request has been sent! We will contact you shortly.', 'success')
        return redirect(url_for('index'))
    return render_template('9_home.html', form=form)

@app.route('/categories')
def categories():
    return render_template('4_select_tyre_category.html')

@app.route('/category/bike-scooter')
def bike_tyres():
    return render_template('2_bike_scooter_tyres.html')

@app.route('/category/car-suv')
def car_tyres():
    return render_template('7_car_suv_tyres.html')

@app.route('/category/truck-crane')
def truck_tyres():
    return render_template('5_truck_crane_tyres.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = QuoteRequest(
            full_name=form.full_name.data,
            phone=form.phone.data,
            vehicle_type=form.vehicle_type.data,
            message=form.message.data
        )
        db.session.add(quote)
        db.session.commit()
        flash('Your request has been sent! We will contact you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('8_contact_us.html', form=form)

# AUTHENTICATION ROUTES

@app.route('/admin.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# PROTECTED ADMIN ROUTES

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_inventory = Tyre.query.count()
    total_stock = sum([t.stock for t in Tyre.query.all()])
    low_stock = Tyre.query.filter(Tyre.stock > 0, Tyre.stock < 10).count()
    return render_template('1_admin_dashboard.html', total_inventory=total_inventory, total_stock=total_stock, low_stock=low_stock)

@app.route('/admin/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = TyreForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            if filename:
                form.image.data.save(os.path.join(UPLOAD_FOLDER, filename))
                
        tyre = Tyre(
            model=form.model.data,
            brand=form.brand.data,
            category=form.category.data,
            price=form.price.data,
            stock=form.stock.data,
            sku=form.sku.data,
            image_filename=filename
        )
        db.session.add(tyre)
        try:
            db.session.commit()
            flash('Tyre added successfully!', 'success')
            return redirect(url_for('inventory'))
        except IntegrityError:
            db.session.rollback()
            flash('SKU already exists!', 'error')
    
    # Simple search handling
    search = request.args.get('q')
    if search:
        tyres = Tyre.query.filter(Tyre.model.ilike(f'%{search}%') | Tyre.brand.ilike(f'%{search}%')).all()
    else:
        tyres = Tyre.query.all()

    return render_template('3_inventory_manager.html', form=form, tyres=tyres)

@app.route('/admin/inventory/delete/<int:id>', methods=['POST'])
@login_required
def delete_tyre(id):
    tyre = Tyre.query.get_or_404(id)
    db.session.delete(tyre)
    db.session.commit()
    flash('Tyre deleted successfully!', 'success')
    return redirect(url_for('inventory'))

@app.route('/admin/inventory/edit/<int:id>', methods=['POST'])
@login_required
def edit_tyre(id):
    tyre = Tyre.query.get_or_404(id)
    form = TyreForm()
    if form.validate_on_submit():
        tyre.model = form.model.data
        tyre.brand = form.brand.data
        tyre.category = form.category.data
        tyre.price = form.price.data
        tyre.stock = form.stock.data
        tyre.sku = form.sku.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            if filename:
                form.image.data.save(os.path.join(UPLOAD_FOLDER, filename))
                tyre.image_filename = filename
        try:
            db.session.commit()
            flash('Tyre updated successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('SKU already exists!', 'error')
    return redirect(url_for('inventory'))

@app.route('/admin/quotes')
@login_required
def admin_quotes():
    quotes = QuoteRequest.query.order_by(QuoteRequest.date_submitted.desc()).all()
    return render_template('admin_quotes.html', quotes=quotes)

@app.route('/admin/settings')
@login_required
def settings():
    return render_template('6_site_settings.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
