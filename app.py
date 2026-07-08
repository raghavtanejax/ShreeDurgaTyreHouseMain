import os
from flask import Flask, render_template, redirect, url_for, flash, request, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Tyre, QuoteRequest, SiteSettings, DispatchActivity
from forms import LoginForm, TyreForm, QuoteForm, SettingsForm, DispatchForm
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from datetime import datetime

load_dotenv()

cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreedurgatyrehouse_super_secret_key'

@app.context_processor
def inject_site_settings():
    from models import SiteSettings
    settings = SiteSettings.query.first()
    # Create default if not exists
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return dict(settings=settings)

if os.environ.get('DATABASE_URL'):
    # Neon provides 'postgres://', but SQLAlchemy requires 'postgresql://'
    db_url = os.environ.get('DATABASE_URL')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
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
    # Fetch settings, if none exist return a default empty object to avoid NoneType errors
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
    return {'year': datetime.now().year, 'site_settings': settings}

# PUBLIC ROUTES

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    base_url = request.url_root.rstrip('/')
    
    # Structured data allows specific SEO tuning per route
    pages = [
        {'loc': '/', 'changefreq': 'weekly', 'priority': '1.0'},
        {'loc': '/categories', 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': '/category/bike-scooter', 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': '/category/car-suv', 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': '/category/truck-crane', 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': '/contact', 'changefreq': 'monthly', 'priority': '0.5'}
    ]
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f"    <loc>{base_url}{page['loc']}</loc>\n"
        xml += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml += f"    <priority>{page['priority']}</priority>\n"
        xml += '  </url>\n'
        
    xml += '</urlset>'
    
    return Response(xml, mimetype='application/xml')

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
    tyres = Tyre.query.filter_by(category='Bike / Scooter').all()
    return render_template('2_bike_scooter_tyres.html', tyres=tyres)

@app.route('/category/car-suv')
def car_tyres():
    tyres = Tyre.query.filter_by(category='Car Tyre').all()
    return render_template('7_car_suv_tyres.html', tyres=tyres)

@app.route('/category/truck-crane')
def truck_tyres():
    tyres = Tyre.query.filter_by(category='Truck/Bus (All Commercial Tyre)').all()
    return render_template('5_truck_crane_tyres.html', tyres=tyres)

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
    
    # Dispatch Activity Stats
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_dispatches_count = DispatchActivity.query.filter(DispatchActivity.date_created >= today_start).count()
    recent_dispatches = DispatchActivity.query.order_by(DispatchActivity.date_created.desc()).limit(5).all()
    
    return render_template('1_admin_dashboard.html', 
                           total_inventory=total_inventory, 
                           total_stock=total_stock, 
                           low_stock=low_stock,
                           todays_dispatches_count=todays_dispatches_count,
                           recent_dispatches=recent_dispatches)

@app.route('/admin/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = TyreForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data and form.image.data.filename:
            # Upload to Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(form.image.data)
                filename = upload_result.get('secure_url')
            except Exception as e:
                error_msg = str(e)
                if 'API key' in error_msg:
                    error_msg = "Unknown API Key. Please check your Vercel Environment Variables."
                flash(f'Cloudinary Upload Error: {error_msg}', 'error')
                return redirect(url_for('inventory'))
                
        brand_val = form.brand.data
        if brand_val == 'Other' and form.custom_brand.data:
            brand_val = form.custom_brand.data.strip()
        tyre = Tyre(
            model=form.model.data,
            brand=brand_val,
            category=form.category.data,
            price=form.price.data,
            mrp_price=form.mrp_price.data,
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
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
    
    # Simple search handling
    search = request.args.get('q')
    if search:
        tyres = Tyre.query.filter(Tyre.model.ilike(f'%{search}%') | Tyre.brand.ilike(f'%{search}%')).all()
    else:
        tyres = Tyre.query.all()

    return render_template('3_inventory_manager.html', form=form, tyres=tyres)

@app.route('/admin/inventory/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tyre(id):
    tyre = Tyre.query.get(id)
    if not tyre:
        flash('Tyre not found or already deleted.', 'error')
        return redirect(url_for('inventory'))
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
        brand_val = form.brand.data
        if brand_val == 'Other' and form.custom_brand.data:
            brand_val = form.custom_brand.data.strip()
        tyre.model = form.model.data
        tyre.brand = brand_val
        tyre.category = form.category.data
        tyre.price = form.price.data
        tyre.mrp_price = form.mrp_price.data
        tyre.stock = form.stock.data
        tyre.sku = form.sku.data
        if form.image.data and form.image.data.filename:
            try:
                upload_result = cloudinary.uploader.upload(form.image.data)
                tyre.image_filename = upload_result.get('secure_url')
            except Exception as e:
                error_msg = str(e)
                if 'API key' in error_msg:
                    error_msg = "Unknown API Key. Please check your Vercel Environment Variables."
                flash(f'Cloudinary Upload Error: {error_msg}', 'error')
                return redirect(url_for('inventory'))
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

@app.route('/admin/quotes/delete/<int:quote_id>', methods=['GET', 'POST'])
@login_required
def delete_quote(quote_id):
    quote = QuoteRequest.query.get(quote_id)
    if not quote:
        flash('Quote not found or already deleted.', 'error')
        return redirect(url_for('admin_quotes'))
    db.session.delete(quote)
    db.session.commit()
    flash('Quote deleted successfully.', 'success')
    return redirect(url_for('admin_quotes'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
        
    form = SettingsForm(obj=settings)
    
    if form.validate_on_submit():
        try:
            if hasattr(form.home_shop_image.data, 'filename') and form.home_shop_image.data.filename:
                upload_result = cloudinary.uploader.upload(form.home_shop_image.data)
                settings.home_shop_image = upload_result.get('secure_url')
            if hasattr(form.truck_category_image.data, 'filename') and form.truck_category_image.data.filename:
                upload_result = cloudinary.uploader.upload(form.truck_category_image.data)
                settings.truck_category_image = upload_result.get('secure_url')
            if hasattr(form.car_category_image.data, 'filename') and form.car_category_image.data.filename:
                upload_result = cloudinary.uploader.upload(form.car_category_image.data)
                settings.car_category_image = upload_result.get('secure_url')
            if hasattr(form.bike_category_image.data, 'filename') and form.bike_category_image.data.filename:
                upload_result = cloudinary.uploader.upload(form.bike_category_image.data)
                settings.bike_category_image = upload_result.get('secure_url')
        except Exception as e:
            error_msg = str(e)
            if 'API key' in error_msg:
                error_msg = "Unknown API Key. Please check your Vercel Environment Variables."
            flash(f'Cloudinary Upload Error: {error_msg}', 'error')
            return redirect(url_for('settings'))

        settings.primary_contact_name = form.primary_contact_name.data
        settings.primary_contact = form.primary_contact.data
        settings.secondary_contact_name = form.secondary_contact_name.data
        settings.secondary_contact = form.secondary_contact.data
        settings.physical_address = form.physical_address.data
        settings.google_maps_url = form.google_maps_url.data
        settings.hindi_english_toggle = form.hindi_english_toggle.data
        db.session.commit()
        flash('Site settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
                
    return render_template('6_site_settings.html', form=form)

@app.route('/admin/dispatch', methods=['GET', 'POST'])
@login_required
def admin_dispatch():
    form = DispatchForm()
    if form.validate_on_submit():
        dispatch = DispatchActivity(
            customer_name=form.customer_name.data,
            phone=form.phone.data,
            destination=form.destination.data,
            tyre_details=form.tyre_details.data,
            total_amount=form.total_amount.data if form.total_amount.data else 0.0,
            amount_received=form.amount_received.data if form.amount_received.data else 0.0,
            status=form.status.data
        )
        db.session.add(dispatch)
        db.session.commit()
        flash('Dispatch activity recorded successfully.', 'success')
        return redirect(url_for('admin_dispatch'))
    
    dispatches = DispatchActivity.query.order_by(DispatchActivity.date_created.desc()).all()
    return render_template('10_admin_dispatch.html', form=form, dispatches=dispatches)

@app.route('/admin/dispatch/update_status/<int:dispatch_id>', methods=['POST'])
@login_required
def update_dispatch_status(dispatch_id):
    dispatch = DispatchActivity.query.get_or_404(dispatch_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Dispatched', 'Delivered']:
        dispatch.status = new_status
        db.session.commit()
        flash(f'Status for dispatch #{dispatch_id} updated to {new_status}.', 'success')
    return redirect(url_for('admin_dispatch'))

@app.route('/admin/dispatch/edit/<int:dispatch_id>', methods=['GET', 'POST'])
@login_required
def edit_dispatch(dispatch_id):
    dispatch = DispatchActivity.query.get_or_404(dispatch_id)
    form = DispatchForm(obj=dispatch)
    
    if form.validate_on_submit():
        dispatch.customer_name = form.customer_name.data
        dispatch.phone = form.phone.data
        dispatch.destination = form.destination.data
        dispatch.tyre_details = form.tyre_details.data
        dispatch.total_amount = form.total_amount.data if form.total_amount.data else 0.0
        dispatch.amount_received = form.amount_received.data if form.amount_received.data else 0.0
        dispatch.status = form.status.data
        
        db.session.commit()
        flash('Dispatch activity updated successfully.', 'success')
        return redirect(url_for('admin_dispatch'))
        
    return render_template('11_admin_dispatch_edit.html', form=form, dispatch=dispatch)

@app.route('/admin/dispatch/delete/<int:dispatch_id>', methods=['GET', 'POST'])
@login_required
def delete_dispatch(dispatch_id):
    dispatch = DispatchActivity.query.get(dispatch_id)
    if not dispatch:
        flash('Dispatch record not found or already deleted.', 'error')
        return redirect(url_for('admin_dispatch'))
    db.session.delete(dispatch)
    db.session.commit()
    flash('Dispatch record deleted successfully.', 'success')
    return redirect(url_for('admin_dispatch'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
