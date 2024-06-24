from models.__init__ import CURSOR, CONN

class Employer:
    """
    Represents an employer in the nanny bureau system.
    """
    all = {}  

    def _init_(self, name, location, number_of_kids, id=None):
        """
        Initializes a new Employer instance.
        """
        self.id = id
        self.name = name
        self.location = location
        self.number_of_kids = number_of_kids

    def _repr_(self):
        """
        Returns a string representation of the employer.
        """
        return f"<Employer {self.id}: {self.name}, {self.location}, Kids: {self.number_of_kids}>"

    @property
    def name(self):
        """
        Gets or sets the name of the employer.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Validates and sets the name of the employer.
        """
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def location(self):
        """
        Gets or sets the location of the employer.
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Validates and sets the location of the employer.
        """
        if isinstance(location, str) and len(location):
            self._location = location
        else:
            raise ValueError("Location must be a non-empty string")

    @property
    def number_of_kids(self):
        """
        Gets or sets the number of kids of the employer.
        """
        return self._number_of_kids

    @number_of_kids.setter
    def number_of_kids(self, number_of_kids):
        """
        Validates and sets the number of kids of the employer.
        """
        if isinstance(number_of_kids, int) and number_of_kids >= 0:
            self._number_of_kids = number_of_kids
        else:
            raise ValueError("Number of kids must be a non-negative integer")

    @classmethod
    def create_table(cls):
        """
        Creates the employers table in the database.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            number_of_kids INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """
        Drops the employers table in the database.
        """
        sql = "DROP TABLE IF EXISTS employers"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """
        Saves the employer to the database.
        """
        sql = "INSERT INTO employers (name, location, number_of_kids) VALUES (?, ?, ?)"
        try:
            CURSOR.execute(sql, (self.name, self.location, self.number_of_kids))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self 
        except Exception as e:
            CONN.rollback()
            raise e

    @classmethod
    def create(cls, name, location, number_of_kids):
        """
        Creates a new employer and saves it to the database.
        """
        employer = cls(name, location, number_of_kids)
        employer.save()
        return employer

    def update(self):
        """
        Updates the employer in the database.
        """
        sql = "UPDATE employers SET name = ?, location = ?, number_of_kids = ? WHERE id = ?"
        try:
            CURSOR.execute(sql, (self.name, self.location, self.number_of_kids, self.id))
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            raise e

    def delete(self):
        """
        Deletes the employer from the database.
        """
        sql = "DELETE FROM employers WHERE id = ?"
        try:
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del type(self).all[self.id]  
            self.id = None    
        except Exception as e:
            CONN.rollback()
            raise e

    @classmethod
    def instance_from_db(cls, row):
        """
        Creates an Employer instance from a database row.
        """
        try:
            employer = cls.all.get(row[0])    
            if employer:
                employer.name = row[1]
                employer.location = row[2]
                employer.number_of_kids = row[3]
            else:
                employer = cls(row[1], row[2], row[3])
                employer.id = row[0]
                cls.all[employer.id] = employer   
            return employer
        except Exception as e:
            raise ValueError(f"Invalid data in row: {row}")

    @classmethod
    def get_all(cls):
        """
        Returns a list of all employers in the database.
        """
        sql = "SELECT * FROM employers"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """
        Finds an employer by ID in the database.
        """
        sql = "SELECT * FROM employers WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """
        Finds an employer by name in the database.
        """
        sql = "SELECT * FROM employers WHERE name = ?"   
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def nannies(self):
        """
        Returns a list of nannies for this employer.
        """
        from models.nanny import Nanny
        sql = "SELECT * FROM nannies WHERE employer_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Nanny.instance_from_db(row) for row in rows]