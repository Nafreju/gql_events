
import logging
import pytest
from .gt_utils import createFrontendQuery






test_reference_users = createFrontendQuery(
    query= (
            'query($id: UUID!) { _entities(representations: [{ __typename: '+ 'UserGQLModel, id: $id' + 
                 ' }])' +
                 '{' +
                 '...on UserGQLModel' + 
                    '{id events(where: {_and: [{startdate: {_ge: "2023-04-20T00:00:00"}},' + 
                    '{enddate: {_le: "2023-04-21T00:00:00"}}]}) {id name startdate enddate}}' +
                 '}' + 
                 '}'),
    variables={"id": "89d1e724-ae0f-11ed-9bd8-0242ac110002"})



test_reference_groups = createFrontendQuery(
    query= (
            'query($id: UUID!) { _entities(representations: [{ __typename: '+ 'GroupGQLModel, id: $id' + 
                 ' }])' +
                 '{' +
                 '...on GroupGQLModel' + 
                    '{id events(where: {_and: [{startdate: {_ge: "2023-04-20T00:00:00"}},' + 
                    '{enddate: {_le: "2023-04-21T00:00:00"}}]}) {id name startdate enddate}}' +
                 '}' + 
                 '}'),
    variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003"})


