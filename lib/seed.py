from models.__init__ import CURSOR, CONN
from models.employer import Employer
from models.nanny import Nanny

def initialize_database():
    CURSOR.execute('PRAGMA foreign_keys = ON')  # Enable foreign key constraints
    CONN.commit()

    # Drop existing tables
    Nanny.drop_table()
    Employer.drop_table()

    # Create new tables
    Employer.create_table()
    Nanny.create_table()

    # Add some initial records
    add_initial_records()

def add_initial_records():
    # Add employers
    employer1 = Employer.create("Jacklyn Atieno", "Nakuru", 2)
    employer2 = Employer.create("Jane Simiyu", "Nanyuki", 3)
    employer3 = Employer.create("Brenda Wanjiru", "Mombasa", 1)
    employer4 = Employer.create("Rebecca Kamau", "Nyeri", 4)
    employer5 = Employer.create("Emily Amani", "Nairobi", 2)

    # Add nannies
    Nanny.create("Anna Wambui", 25, 120.0, employer1.id)
    Nanny.create("Sophia Mumbua", 30, 120.0, employer1.id)
    Nanny.create("Emma Gachoki", 22, 130.0, employer2.id)
    Nanny.create("Isabella Atieno", 28, 130.0, employer2.id)
    Nanny.create("Moureen Waititu", 26, 100.0, employer3.id)
    Nanny.create("Olivia Bahati", 27, 100.0, employer3.id)
    Nanny.create("Amanda Muchoki", 24, 140.0, employer4.id)
    Nanny.create("Melody Seela", 29, 140.0, employer4.id)
    Nanny.create("Diana Mueni", 23, 140.0, employer4.id)
    Nanny.create("Evelyn Nekesa", 31, 120.0, employer5.id)
    Nanny.create("Hellen Cherotich", 28, 120.0, employer5.id)

# Initialize database when this module is imported
if __name__ == "__main__":
    initialize_database()