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

from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_events_groups = createResolveReferenceTest(tableName='events_groups', gqltype='EventGroupGQLModel', \
            attributeNames=["id", "lastchange"])

test_query_events_groups_by_id = createByIdTest(tableName="events_groups", queryEndpoint="eventGroupById")
test_query_events_groups_page = createPageTest(tableName="events_groups", queryEndpoint="eventGroupPage")

test_insert_event_group = createFrontendQuery(
    query="""mutation ($event_id: UUID!, $group_id: UUID!) {
        result: eventGroupInsert(eventGroup: {eventId: $event_id, groupId: $group_id}) {
            id
            msg
            eventGroup {
                id
                changedby { id }
                created
                createdby { id }
                rbacobject { id }
                event { id }
                group { id }
            }
        }
    }""",
    variables={"event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3b54-ae0f-11ed-9bd8-0242ac110002"}
)

# test_update_event_group = createUpdateQuery(
#     query="""mutation ($id: UUID!, $groupId: UUID!, $lastchange: DateTime!) {
#         result: eventGroupUpdate(event: {id: $id, groupId: $group_id, lastchange: $lastchange}) {
#             id
#             msg
#             event {
#                 id
#             }
#         }
#     }""",
#     variables={"id": "9baf3aaa-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3de8-ae0f-11ed-9bd8-0242ac110002"},
#     tableName="events_groups"
# )