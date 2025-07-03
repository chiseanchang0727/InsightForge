from fastapi import FastAPI 
from enum import Enum 
from pydantic import BaseModel
from typing import Annotated, Optional, Dict, Any
from fastapi import Query

from mysql_connector import MySqlConnector
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()


app = FastAPI()

@app.get("/")
async def submit(file_name: str, page_num:str, description: str):
    """
    update into my dataframe in pandas and then upload to MySQL database
    """

    connector = MySqlConnector(
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DATABASE"),
        userN=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD") 
    )
    # df = pd.read_sql("data", connector.engine)
    # print(df)
    # Create a new row with the provided data
    new_row = {
        "file_name": file_name,
        "page_num": page_num,
        "description": description
    }
    
    # Append the new row to the DataFrame
    
    # df = pd.concat([df, pd.DataFrame(new_row)], axis=)
    df = pd.DataFrame([new_row])
    
    # Upload the updated DataFrame to MySQL
    df.to_sql("data", connector.engine, if_exists='append', index=False)
    # connector.disconnect()
    return {"message": "Data submitted successfully", "data": new_row}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8070)