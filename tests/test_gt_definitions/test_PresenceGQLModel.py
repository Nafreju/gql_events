import pytest



from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)


test_reference_events_users = createResolveReferenceTest(tableName='events_users', gqltype='PresenceGQLModel', \
            attributeNames=["id", "lastchange"])

test_query_events_users_by_id = createByIdTest(tableName="events_users", queryEndpoint="presenceById", attributeNames=["id"])
test_query_events_users_page = createPageTest(tableName="events_users", queryEndpoint="presencePage", attributeNames=["id"])

test_insert_events_users = createFrontendQuery(
    query="""mutation ($user_id: UUID!, $event_id: UUID!, $invitationtype_id: UUID!, $presencetype_id: UUID!) {
        result: presenceInsert(presence: {userId: $user_id, eventId: $event_id, invitationtypeId: $invitationtype_id, presencetypeId: $presencetype_id}) {
            id
            msg
            presence {
                id
                changedby { id }
                created
                createdby { id }
                rbacobject { id }
                eventId
                userId
                invitationtypeId
                presencetypeId
                event { id }
                user { id }
                invitationType { id }
                presenceType { id }
            }
        }
    }""",
    variables={ "user_id": "89d1f34a-ae0f-11ed-9bd8-0242ac110002", \
                "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", \
                "invitationtype_id": "e871403c-a79c-11ed-b76e-0242ac110002", \
                "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"}
)

test_update_events_users = createUpdateQuery(
    query="""mutation ($id: UUID!, $invitationtype_id: UUID!, $lastchange: DateTime!) {
        result: presenceUpdate(presence: {id: $id, invitationtypeId: $invitationtype_id, lastchange: $lastchange}) {
            id
            msg
            presence {
                id
            }
        }
    }""",
    variables={"id": "89d1f2d2-ae0f-11ed-9bd8-0242ac110002", "invitationtype_id": "e871403c-a79c-11ed-b76e-0242ac110002"},
    tableName="events_users"
)


# id should exist in systemdata
test_delete_events_users = createDeleteQuery(tableName="events_users", queryBase="presence", attributeNames=["id"],
        id="89d1e684-ae0f-11ed-9bd8-0242ac110002")
