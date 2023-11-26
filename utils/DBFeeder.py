from functools import cache


from DBDefinitions import \
    EventModel, EventTypeModel, EventCategoryModel, EventGroupModel, \
        InvitationTypeModel, PresenceModel, PresenceTypeModel

from sqlalchemy.future import select


import datetime

import asyncio
import os
import json
import uuid

from uoishelpers.feeders import ImportModels

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
            
            if (key in ["id", "changedby", "createdby"]) or ("_id" in key):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    pass
                    #print(key, value)

        return json_dict


    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData


async def initDB(asyncSessionMaker):

    defaultNoDemo = "_________"
    
    """
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        print("No Demo mode")
        dbModels = [
            EventTypeModel,           
            PresenceTypeModel, 
            InvitationTypeModel        ]
    else:
    """
    print("Demo mode")
    dbModels = [
        EventCategoryModel,
        EventTypeModel, 
        PresenceTypeModel, 
        InvitationTypeModel,
        EventModel, 
        EventGroupModel, 
        PresenceModel
    ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
