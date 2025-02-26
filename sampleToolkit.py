from typing import List
import sqlite3
from agno.agent import Agent
from agno.tools import Toolkit
from agno.utils.log import logger
from pydantic import BaseModel, Field,PositiveInt,ValidationError 
from agno.models.groq import Groq as gg
import gradio as gr
#------ User------
class Users(BaseModel):
    name:str = Field(..., description="name of the user")
    email:str = Field(..., description="email of the user")
    age: PositiveInt = Field(..., description="age of the user")


class Respose(BaseModel):
    res:list[str]
#------User-------


class DBHandler(Toolkit):
    def __init__(self, name = "dbTool",db_file='sunny.db'):
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

#if __name__ == '__main__':
    #db = DBHandler()
    #user = Users(name="sunny4",email="4@gmail.com",age = 30)
    #db.create_table()
    #db.create_item(user)
    #res = db.displayRecords('Users')
    #print(res)


agent = Agent(
    model = gg(id="llama-3.3-70b-versatile"),
    tools=[DBHandler()],
    description="you are an Ai assistant which can do curd operations. Don't hallosinate Data.",
    instructions=['if you get errors show them in redable form'],
    show_tool_calls=True, markdown=True,
    #response_model=Respose,
    
)

#text = "add these record in table Users sunny 1@gmai and age 30 and display the records"
#text = "create table myUsers"
#agent.print_response(text)
#agent.print_response('is it possible for you to display the records from the table Users')

#----ui-----
def process_input(text):
    try:
        res = agent.run(text)
        return res.content
    except Exception as e:
        return e

iface = gr.Interface(
    fn=process_input,
    inputs=gr.Textbox(lines=2, placeholder="Enter your input here..."),
    outputs="text",
    title="Phi Agent Gradio Interface",
    description="Send input to the Phi agent and see the processed result."
)
iface.launch()
#----ui-----