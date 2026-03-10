from fastapi import FastAPI, APIRouter
from requests.Greeting_request import Greeting_request
from logger.Logger import Logger

router = APIRouter(prefix="/api/v1")

logger = Logger("main")

@router.get(path="/greeting/{name}", 
        status_code=200,
        summary="",
        operation_id="getting_message",
        tags=["GET_MESSAGE"]
)
def getting_message(name: str = "world", detail = None):
    return {"msg": f"Hello, {name} {',' + detail if detail is not None else ''}!!"}

@router.post(path="/greeting",
        status_code=200,
        summary="",
        operation_id="create_message",
        tags=["POST_MESSAGE"])
def create_message(request_body: Greeting_request):
    logger.debug("THIS SHOULD NOT BE PRINTED")
    surname = request_body.surname
    detail = request_body.detail
    logger.info(f"surname {surname} and detail {detail}")
    return {"msg": f"Hello {request_body.name} {surname if not surname.isspace() else ''}{', ' + detail if detail is not None  else ''}".strip()}

@router.put(path="/greeting",
        status_code=200,
        summary="",
        operation_id="modify_message",
        tags=["PUT_MESSAGE"])
def modify_message():
    return {"msg": "Put endpoint" }

@router.patch(path="/greeting",
        status_code=200,
        summary="",
        operation_id="modify_message_partially",
        tags=["PATCH_MESSAGE"])
def modify_message_partially():
    return {"msg": "Patch endpoint"}

@router.delete(path="/greeting",
        status_code=200,
        summary="",
        operation_id="remove_message",
        tags=["DELETE_MESSAGE"])
def remove_message():
    return {"msg": "Delete endpoint"}

app = FastAPI(
    title="First FastAPI",
    version="1.0.0",
    summary="First try of FastAPI app from Master",
    contact={
        "name": "Raul",
        "email": "rulox.github@gmail.com"
    },
    servers=[
        {"url": "https://localhost:9080", "description":"Url for local requests"}
    ],
    openapi_url="/v1/swagger-ui.html"
)

app.include_router(router)