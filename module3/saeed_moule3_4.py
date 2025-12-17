# module3/saeed_moule3_4.py
# A simple FastAPI application to create and retrieve a person's name and phone number.
# Run this app and use POST /person to create a person and GET /person to retrieve the person's data.
## To run the app, use the command: uvicorn module3.saeed_moule3_4:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name: str
    phone: str

person_data = {}

@app.post("/person")
async def create_person(person: Person):
    global person_data
    person_data = person.dict()
    return {"message": "Person created", "person": person_data}

@app.get("/person")
async def get_person():
    return person_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
