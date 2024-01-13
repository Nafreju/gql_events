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

test_reference_event_presence_types = createResolveReferenceTest(tableName='eventpresencetypes', gqltype='PresenceTypeGQLModel', \
            attributeNames=["id", "name", "lastchange"])

test_query_event_presence_type_by_id = createByIdTest(tableName="eventpresencetypes", queryEndpoint="presenceTypeById")
test_query_event_presence_type_page = createPageTest(tableName="eventpresencetypes", queryEndpoint="presenceTypePage")

test_insert_event_presence_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: presenceTypeInsert(presenceType: {id: $id, name: $name}) {
            id
            msg
            type {
                id
                name
                nameEn
                valid
                created
                createdby { id }
                changedby { id }
                rbacobject { id }
                presences { id }
            }
        }
    }""",
    variables={"id": "f6f79926-ac0e-4832-9a38-4272cae33fa9", "name": "new name"}
)

test_update_presence_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: presenceTypeUpdate(presenceType: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            type {
                id
                name
            }
        }
    }""",
    variables={"id": "46639812-a79c-11ed-b76e-0242ac110002", "name": "new name"},
    tableName="eventpresencetypes"
)