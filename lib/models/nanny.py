from models.__init__ import CURSOR, CONN

class Nanny:
    """
    Represents a nanny in the nanny bureau system.
    """
    all = {}  

    def _init_(self, name, age, salary_expectation, employer_id, id=None):
        """
        Initializes a new Nanny instance.
        """
        self.id = id
        self.name = name
        self.age = age
        self.salary_expectation = salary_expectation
        self.employer_id = employer_id

    def _repr_(self):
        """
        Returns a string representation of the nanny.
        """
        return f"<Nanny {self.id}: {self.name}, Age: {self.age}, Salary Expectation: ${self.salary_expectation:.2f}, Employer ID: {self.employer_id}>"

    @property
    def name(self):
        """
        Gets or sets the name of the nanny.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Validates and sets the name of the nanny.
        """
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def age(self):
        """
        Gets or sets the age of the nanny.
        """
        return self._age

    @age.setter
    def age(self, age):
        """
        Validates and sets the age of the nanny.
        """
        if isinstance(age, int) and age > 0:
            self._age = age
        else:
            raise ValueError("Age must be a positive integer")

    @property
    def salary_expectation(self):
        """
        Gets or sets the salary expectation of the nanny.
        """
        return self._salary_expectation

    @salary_expectation.setter
    def salary_expectation(self, salary_expectation):
        """
        Validates and sets the salary expectation of the nanny.
        """
        if isinstance(salary_expectation, (int, float)) and salary_expectation >= 0:
            self._salary_expectation = salary_expectation
        else:
            raise ValueError("Salary expectation must be a non-negative number")

    @property
    def employer_id(self):
        """
        Gets or sets the employer ID of the nanny.
        """
        return self._employer_id

    @employer_id.setter
    def employer_id(self, employer_id):
        from models.employer import Employer

        """
        Validates and sets the employer ID of the nanny.
        """
        if isinstance(employer_id, int) and Employer.find_by_id(employer_id):
            self._employer_id = employer_id
        else:
            raise ValueError("employer_id must reference an employer in the database")

    @classmethod
    def create_table(cls):
        """
        Creates the nannies table in the database.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS nannies (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            salary_expectation REAL,
            employer_id INTEGER,
            FOREIGN KEY (employer_id) REFERENCES employers(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """
        Drops the nannies table in the database.
        """
        sql = "DROP TABLE IF EXISTS nannies"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """
        Saves the nanny to the database.
        """
        sql = "INSERT INTO nannies (name, age, salary_expectation, employer_id) VALUES (?, ?, ?, ?)"
        CURSOR.execute(sql, (self.name, self.age, self.salary_expectation, self.employer_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self        

    @classmethod
    def create(cls, name, age, salary_expectation, employer_id):
        """
        Creates a new nanny and saves it to the database.
        """
        nanny = cls(name, age, salary_expectation, employer_id)
        nanny.save()
        return nanny

    def update(self):
        """
        Updates the nanny in the database.
        """
        sql = "UPDATE nannies SET name = ?, age = ?, salary_expectation = ?, employer_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.age, self.salary_expectation, self.employer_id, self.id))
        CONN.commit()

    def delete(self):
        """
        Deletes the nanny from the database.
        """
        sql = "DELETE FROM nannies WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]       
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """
        Creates a Nanny instance from a database row.
        """
        nanny = cls.all.get(row[0])     
        if nanny:
            nanny.name = row[1]
            nanny.age = row[2]
            nanny.salary_expectation = row[3]
            nanny.employer_id = row[4]
        else:
            nanny = cls(row[1], row[2], row[3], row[4])
            nanny.id = row[0]
            cls.all[nanny.id] = nanny       
        return nanny

    @classmethod
    def get_all(cls):
        """
        Returns a list of all nannies in the database.
        """
        sql = "SELECT * FROM nannies"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """
        Finds a nanny by ID in the database.
        """
        sql = "SELECT * FROM nannies WHERE id =?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """
        Finds a nanny by name in the database.
        """
        sql = "SELECT * FROM nannies WHERE name = ?"  
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def employer(self):
        """
        Returns the employer for this nanny.
        """
        from models.employer import Employer
        return Employer.find_by_id(self.employer_id)