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


test_reference_eventcategories = createResolveReferenceTest(tableName='eventcategories', \
        gqltype='EventCategoryGQLModel', attributeNames=["id", "name", "lastchange", "nameEn", "valid", "created", "createdby", "changedby"])

test_query_event_category_by_id = createByIdTest(tableName="eventcategories", queryEndpoint="eventCategoryById")
test_query_event_category_page = createPageTest(tableName="eventcategories", queryEndpoint="eventCategoryPage")

test_insert_event_category = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: eventCategoryInsert(eventCategory: {id: $id, name: $name}) {
            id
            msg
            category {
                id
                name
                resolveRbacobject { id }
                eventTypes { id }
            }
        }
    }""",
    variables={"id": "5aaf820d-5acd-4406-b18d-47f161e75eba", "name": "new name"}
)

test_update_event_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: eventCategoryUpdate(eventCategory: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            category {
                id
                name
            }
        }
    }""",
    variables={"id": "5aaf820d-5acd-4406-b18d-47f161e75ebb", "name": "new name"},
    tableName="eventcategories"
)