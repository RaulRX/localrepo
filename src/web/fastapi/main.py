from fastapi import FastAPI, params
from requests.Greeting_request import Greeting_request

app = FastAPI()

@app.get("/greeting/{name}")
def getting_message(name: str = "world", detail = None):
    return {"msg": f"Hello, {name} {',' + detail if detail is not None else ''}!!"}

@app.post("/greeting/")
def create_message(request_body: Greeting_request):
    surname = request_body.surname
    detail = request_body.detail
    return {"msg": f"Hello {request_body.name}{surname if not surname.isspace() else ''}{', ' + detail if not detail.isspace() else ''}".strip()}

@app.put("/greeting")
def modify_message():
    return {"msg": "Put endpoint" }

@app.patch("/greeting")
def modify_message_partially():
    return {"msg": "Patch endpoint"}

@app.delete("/greeting")
def remove_message():
    return {"msg": "Delete endpoint"}