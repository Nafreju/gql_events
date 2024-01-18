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

test_reference_event_invitation_types = createResolveReferenceTest(tableName='eventinvitationtypes', gqltype='InvitationTypeGQLModel', \
            attributeNames=["id", "name", "lastchange"])

test_query_event_invitation_type_by_id = createByIdTest(tableName="eventinvitationtypes", queryEndpoint="invitationTypeById")
test_query_event_invitation_type_page = createPageTest(tableName="eventinvitationtypes", queryEndpoint="invitationTypePage")

test_insert_event_invitation_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: invitationTypeInsert(invitationType: {id: $id, name: $name}) {
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
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa9", "name": "new name"}
)

test_update_event_invitation_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: invitationTypeUpdate(invitationType: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            type {
                id
                name
            }
        }
    }""",
    variables={"id": "e8713b6e-a79c-11ed-b76e-0242ac110002", "name": "new name"},
    tableName="eventinvitationtypes"
)