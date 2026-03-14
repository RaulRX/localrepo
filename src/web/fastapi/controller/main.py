import os
from dotenv import load_dotenv

if not os.getenv("environment"):
    #Local testing purposes
    print("Using local environment")
    load_dotenv('.env')

from fastapi import FastAPI, APIRouter, Body
from .responses.Responses import Message_list_response, Message_response
from .requests.Requests import Message_req
from ..logger.Logger import Logger
# from ..repository.SQLite_native.Message_repository_native import Repository
from ..repository.SQLlite_SQLalchemy.Message_repository_orm import Repository
# from ..repository.SQLite_native.model.Message import Message_classic
from ..repository.SQLlite_SQLalchemy.model.Message import Message_modern

router = APIRouter(prefix="/api/v1")

logger = Logger("main")
repo = Repository("MessageFolder.db")

@router.get(path="/messages",
        status_code=200,
        summary="",
        operation_id="getting_messages",
        tags=["GET_MESSAGE"],
        response_model=Message_list_response
)
def getting_messages():
    messages = repo.get_all()

    messages_list = []
    for m in messages:
        messages_list.append(Message_response(
            chain = m.chain,
            updated_date = m.updated_date,
            user = m.user,
            user_id = m.user_id
        ))

    return Message_list_response(message_list=messages_list)

@router.get(path="/messages",
        status_code=200,
        summary="",
        operation_id="getting_all_messages",
        tags=["GET_MESSAGE"],
        response_model=Message_list_response
)
def getting_all_messages():
    messages = repo.get_all()

    messages_list = []
    for m in messages:
        messages_list.append(Message_response(
            chain = m.chain,
            updated_date = m.updated_date,
            user = m.user,
            user_id = m.user_id
        ))

    return Message_list_response(message_list=messages_list)

@router.post(path="/messages",
        status_code=200,
        summary="",
        operation_id="create_message",
        tags=["POST_MESSAGE"],
        response_model=Message_response
)
def create_message(request_body: Message_req):
    logger.debug("THIS SHOULD NOT BE PRINTED")
    message = Message_modern(user= request_body.user, user_id = request_body.user_id, chain = request_body.chain)
    saved_message = repo.save(message=message)

    return Message_response(chain=saved_message.chain, updated_date = saved_message.updated_date, user = saved_message.user, user_id = saved_message.user_id)

# @router.put(path="/greeting",
#         status_code=200,
#         summary="",
#         operation_id="modify_message",
#         tags=["PUT_MESSAGE"])
# def modify_message():
#     return {"msg": "Put endpoint" }

@router.patch(path="/messages",
        status_code=204,
        summary="",
        operation_id="modify_message_partially",
        tags=["PATCH_MESSAGE"])
def modify_message_partially(
    user_id:str = Body(validation_alias="userId", description="User identification number", examples=["11111111A", "Y1234432R"], min_length=9, max_length=9, 
                       pattern = "^(?:[0-9]{8}|[XYZ][0-9]{7})[A-Z]$"),
    user: str = Body(validation_alias="name", description="Name of the person", min_length=5, max_length=64)):
    repo.update(user_id, user)

@router.delete(path="/messages/{id}",
        status_code=204,
        summary="",
        operation_id="remove_message",
        tags=["DELETE_MESSAGE"])
def remove_message(id: int):
    repo.remove(id)

@router.delete(path="/messages",
        status_code=204,
        summary="",
        operation_id="remove_all_message",
        tags=["DELETE_MESSAGE"])
def remove_all_message():
    repo.remove_all()

app = FastAPI(
    title="First FastAPI",
    version="1.0.0",
    summary="First try of FastAPI app from Master",
    contact={
        "name": "Raul",
        "email": "rulox.github@gmail.com"
    },
    servers=[
        {"url": "http://localhost:9080", "description":"Url for local requests"}
    ],
    openapi_url="/v1/swagger-ui.html"
)

app.include_router(router)