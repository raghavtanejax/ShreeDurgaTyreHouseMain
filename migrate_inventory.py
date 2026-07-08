import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def migrate():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        db_url = 'sqlite:///app.db'
    elif db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    print(f"Connecting to {db_url}")
    engine = create_engine(db_url)

    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE tyre ADD COLUMN mrp_price FLOAT;"))
            print("Added mrp_price column.")
        except Exception as e:
            print(f"Error adding mrp_price: {e}")
        
        try:
            conn.execute(text("ALTER TABLE tyre ALTER COLUMN model DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE tyre ALTER COLUMN brand DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE tyre ALTER COLUMN category DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE tyre ALTER COLUMN price DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE tyre ALTER COLUMN sku DROP NOT NULL;"))
            print("Dropped NOT NULL constraints on tyre table.")
        except Exception as e:
            print(f"Error dropping constraints (might be SQLite): {e}")

        conn.commit()
    print("Migration complete.")

if __name__ == '__main__':
    migrate()
