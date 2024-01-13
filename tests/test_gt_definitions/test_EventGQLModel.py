import pytest

# import os
# os.environ["GQLUG_ENDPOINT_URL"] = "http://localhost:8124/gql"
# print(os.environ.get("GQLUG_ENDPOINT_URL", None))

# from ..gqlshared import (
#     createByIdTest, 
#     createPageTest, 
#     createResolveReferenceTest, 
#     createFrontendQuery, 
#     createUpdateQuery
# )

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_events = createResolveReferenceTest(tableName='events', gqltype='EventGQLModel', \
            attributeNames=["id", "name", "lastchange", "groups { id }", "presences { id }", "subEvents { id }"])

test_query_event_by_id = createByIdTest(tableName="events", queryEndpoint="eventById")
test_query_event_page = createPageTest(tableName="events", queryEndpoint="eventPage")

test_insert_event = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $eventtype_id: UUID!) {
        result: eventInsert(event: {id: $id, name: $name, eventtypeId: $eventtype_id}) {
            id
            msg
            event {
                id
                name
                changedby { id }
                nameEn
                valid
                created
                startdate
                enddate
                mastereventId
                masterEvent { id }
                createdby { id }
                eventtypeId
                rbacobject { id }
                eventType { id }
            }
        }
    }""",
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new name", "eventtype_id": "b87d3ff0-8fd4-11ed-a6d4-0242ac110002"}
)

test_update_event = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: eventUpdate(event: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            event {
                id
                name
            }
        }
    }""",
    variables={"id": "0945ad17-3a36-4d33-b849-ad88144415ba", "name": "new name"},
    tableName="events"
)