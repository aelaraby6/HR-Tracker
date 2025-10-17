from mentor_bot.db import create_tables
from mentor_bot.seed_data import seed_groups, seed_mentors

def initialize():
    print("Initializing database...")
    create_tables()
    seed_groups()
    seed_mentors()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize()
