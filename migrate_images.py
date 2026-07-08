from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        commands = [
            "ALTER TABLE site_settings ADD COLUMN home_shop_image VARCHAR(255);",
            "ALTER TABLE site_settings ADD COLUMN truck_category_image VARCHAR(255);",
            "ALTER TABLE site_settings ADD COLUMN car_category_image VARCHAR(255);",
            "ALTER TABLE site_settings ADD COLUMN bike_category_image VARCHAR(255);"
        ]
        
        for cmd in commands:
            try:
                db.session.execute(text(cmd))
                print(f"Executed: {cmd}")
            except Exception as e:
                print(f"Error executing {cmd}: {e}")
                db.session.rollback()
        
        db.session.commit()
        print("Migration complete.")

if __name__ == '__main__':
    migrate()
