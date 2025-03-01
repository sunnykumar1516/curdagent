from pydantic import BaseModel, Field,PositiveInt,ValidationError
import sqlite3
from agno.tools import Toolkit

#------ User------
class Users(BaseModel):
    name:str 
    email:str 
    age: PositiveInt 

class Table(BaseModel):
    name:str 
     

#------User-------


class DataRetriver(Toolkit):
    path = "./sample.db"
    def __init__(self, name = "dbTool",db_file=path):
        super().__init__(name)
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file,check_same_thread=False)
        self.register(self.addRecords)
        self.register(self.displayRecords)
        #self.register(self.updateRecords)
        #self.register(self.displaySelectedRecords)
        self.register(self.listTables)

    def displayRecords(self,table:str='test'):
        """
            Retrieves all records from the specified table.
        Args:
             table (str): The name of the table to fetch records from.
        Returns:
             A list of records or an error message.        
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table};")
                records = cursor.fetchall()
                text_output= "records in table"
                for record in records:
                    text_output += " | ".join(map(str, record)) + "\n"

            return text_output

                
        except sqlite3.OperationalError:
            return f"Error: Table '{table}' does not exist."
        except Exception as e:
            return f"Error retrieving records: {e}"
    def addRecords(self,name,email,age,table):
        """
        add records to the table
        args:
           name: name of the user
           email:email of the user
           age: age of the user
           table: name of the table
        return:
            returns sucess if the records are added if any error return error
        """
        try:
            user = Users(name=name,email=email,age = age)
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()

           
                cursor.execute(
                    f"INSERT INTO {table} (name, email, age) VALUES (?, ?, ?)", 
                    (user.name, user.email, user.age)
                    )
                conn.commit()
            
            return "Record added successfully."
        except ValidationError as e:
            return "value not proper "
        except Exception as e:
            return "unknown error while adding record"
    
    def listTables(self):
        """
        Lists all tables in the SQLite database.
        Returns:
            A list of table names or an error message.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                res = "all tables in database "
                for table in tables:
                    print("----",table[0])
                    res = res +" "+ table[0]
                return res
        except Exception as e:
            return f"Error retrieving tables: {e}"
            
    def updateRecords(table_name,user:dict):
        pass
    def displaySelectedRecords(table_name:str,email:str):
        pass

'''db_tool = DataRetriver()
print(db_tool.displayRecords('test'))
result = db_tool.addRecords(
    name="Sunny Kumar",
    email="sunny@example.com",
    age=30,
    table="test"
)

print(result)'''