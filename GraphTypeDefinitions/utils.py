from contextlib import asynccontextmanager
import logging

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session   
        finally:
            pass

def getLoaders(info):
    return info.context["loaders"]


demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUser(info):
    context = info.context
    result = context.get("user", None)
    """
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if 'Bearer ' in authorization:
                token = authorization.split(' ')[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    """
    return result