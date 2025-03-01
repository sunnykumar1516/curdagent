from pydantic import BaseModel, Field,PositiveInt,ValidationError
import sqlite3
from agno.tools import Toolkit

#------ User------
class Users(BaseModel):
    name:str = Field(..., description="name of the user")
    email:str = Field(..., description="email of the user")
    age: PositiveInt = Field(..., description="age of the user")


class Respose(BaseModel):
    res:list[str]
#------User-------

path = "/Volumes/sunny333/code/genAI/AgenticAI/Ai_CurdAgent/sample.db"
class DBHandler(Toolkit):
    def __init__(self, name = "dbTool",db_file=path):
        super().__init__(name)
        self.conn = sqlite3.connect(db_file,check_same_thread=False)
        self.register(self.displayRecords)
        self.register(self.create_table)
        self.register(self.create_item)

    def displayRecords(self,tableName):
        '''
        display and return all the records in a table
        args:
            takes in table name as argument
        returns:
            returns all the records
        '''
        cursor = self.conn.cursor()
        query = f"SELECT * FROM {tableName}"
        cursor.execute(query)
        records = cursor.fetchall()
        result_text = "\n".join(
        ", ".join(str(field) for field in record) for record in records
        )
                
        
        self.conn.commit()

        return result_text

    def create_table(self,tableName):
        '''
        create table with table in the databse
        args:
            takes in table name as argument
        returns:
            returns created table name
        
        '''
        cursor = self.conn.cursor()
        query = f"""CREATE TABLE IF NOT EXISTS {tableName}(
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age int)"""
        cursor.execute(query)
        self.conn.commit()
        return f"table created{tableName}"

    def create_item(self, user:Users):
        '''
        add User to the table 
        args:
            takes in User object as argument object contains name,email and age
        returns:
            if sucessful returns added user  along with all users 
            if any error returns the error
        '''
        print("-----------",user)
        try:
            t = Users(name = user.name, email = user.email, age = user.age)
        except ValidationError as ve:
            return ve

        try:
            
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Users (name, email, age) VALUES (?, ?, ?)",
                (user.name,user.email,user.age)
            )
            self.conn.commit()
            return "records added" , str(self.displayRecords('Users'))
        except Exception as e:
            return {"error": "Unhandled error", "details": str(e)}

if __name__ == '__main__':
    db = DBHandler()
    user = Users(name="sunny4",email="477@gmail.com",age = 30)
    db.create_table(tableName="sunnytest")
    #db.create_item(user)
    #res = db.displayRecords('Users')
    #print(res)