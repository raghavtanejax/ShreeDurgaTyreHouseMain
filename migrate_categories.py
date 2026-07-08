from app import app, db
from models import Tyre

with app.app_context():
    # Update Truck & Crane
    truck_tyres = Tyre.query.filter_by(category='Truck & Crane').all()
    for t in truck_tyres:
        t.category = 'Truck/Bus (All Commercial Tyre)'
        
    # Update Car & SUV
    car_tyres = Tyre.query.filter_by(category='Car & SUV').all()
    for t in car_tyres:
        t.category = 'Car Tyre'
        
    # Update Bike & Scooter
    bike_tyres = Tyre.query.filter_by(category='Bike & Scooter').all()
    for t in bike_tyres:
        t.category = 'Bike / Scooter'
        
    db.session.commit()
    print(f"Updated {len(truck_tyres)} Truck tyres, {len(car_tyres)} Car tyres, {len(bike_tyres)} Bike tyres.")
