# note: This is a FastAPI application that responds with a greeting message.
# It defines a single endpoint "/hello" that takes a query parameter "name".
# When accessed, it returns a JSON response with a greeting message. 

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello(name: str = "mohammmed"):
    return {"message": f"Hello {name}"}


