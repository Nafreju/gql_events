import pytest
from GraphTypeDefinitions import schema


from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_eventcategories = createResolveReferenceTest(tableName="eventcategories", gqltype="EventCategoryGQLModel", attributeNames=["id", "name", "lastchange"])

test_query_event_category_by_id = createByIdTest(tableName="eventcategories", queryEndpoint="eventCategoryById")