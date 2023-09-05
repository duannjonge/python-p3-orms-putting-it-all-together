import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__(self,name,breed):
        self.id =None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        SQL = """
           CREATE TABLE IF NOT EXISTS dogs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
           );
        
        """
        CURSOR.execute(SQL)
    @classmethod
    def drop_table(cls):
        SQL = """
           DROP TABLE IF EXISTS dogs;
            
        """
        CURSOR.execute(SQL)
    
    def save(self):
        SQL = """
           INSERT INTO dogs(name,breed)
           VALUES (?,?);
        """
        CURSOR.execute(SQL,(self.name,self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    @classmethod
    def create(cls,name,breed):
        dog = Dog(name,breed)
        dog.save()
        return dog
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    @classmethod
    def get_all(cls):
        SQL = """
           SELECT * 
           FROM dogs;
           
        """
        all = CURSOR.execute(SQL).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    @classmethod
    def find_by_name(cls, name):
        SQL = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1;
        """

        dog = CURSOR.execute(SQL, (name,)).fetchone()
        # return cls.new_from_db(dog)
        
        if dog is not None:
            return cls.new_from_db(dog)
        
        return None

    @classmethod
    def find_by_id(cls, id):
        SQL = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1;
        """
        dog = CURSOR.execute(SQL, (id,)).fetchone()
        return cls.new_from_db(dog)
    @classmethod
    def find_or_create_by(cls, name, breed):  
        SQL = """
            SELECT * 
            FROM dogs  
            WHERE name =? AND breed =?
            LIMIT 1         
        """
        all = CURSOR.execute(SQL,(name, breed)).fetchone()
        if all is None:
            return cls.create(name, breed)
        else:
            return cls.new_from_db(all)
    def update(self):
        if self.id is not None:
            SQL ="""
                UPDATE dogs
                SET name = ?
                WHERE id =?
            """
            CURSOR.execute(SQL, (self.name, self.id))
            CONN.commit()