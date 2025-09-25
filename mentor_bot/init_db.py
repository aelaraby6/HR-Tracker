from db import create_tables
from seed_data import seed_groups, seed_mentors

if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    seed_groups()
    seed_mentors()
    print("Database initialized successfully!")