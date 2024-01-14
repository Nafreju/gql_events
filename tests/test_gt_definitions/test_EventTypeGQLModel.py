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

test_reference_eventtypes = createResolveReferenceTest(tableName='eventtypes', gqltype='EventTypeGQLModel', \
            attributeNames=["id", "name", "lastchange"])

test_query_event_type_by_id = createByIdTest(tableName="eventtypes", queryEndpoint="eventTypeById")
test_query_event_type_page = createPageTest(tableName="eventtypes", queryEndpoint="eventTypePage")

test_insert_event_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $category_id: UUID!) {
        result: eventTypeInsert(eventType: {id: $id, name: $name, categoryId: $category_id}) {
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
                categoryId
                rbacobject { id }
                events { id }
                category { id }
            }
        }
    }""",
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name", "category_id": "5aaf820d-5acd-4406-b18d-47f161e75ebb"}
)

test_update_event_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: eventTypeUpdate(eventType: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            type {
                id
                name
            }
        }
    }""",
    variables={"id": "c0a12392-ae0e-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="eventtypes"
)