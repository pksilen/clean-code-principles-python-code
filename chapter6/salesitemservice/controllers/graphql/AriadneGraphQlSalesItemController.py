from ariadne import MutationType, QueryType, gql, make_executable_schema
from dependency_injector.wiring import Provide

from ..dtos.InputSalesItem import InputSalesItem
from ..service.SalesItemService import SalesItemService

sales_item_service: SalesItemService = Provide['sales_item_service']

schema = gql(
    """
type SalesItem {
  id: ID!
  createdAtTimestampInMs: String!
  name: String!
  priceInCents: Int!
  images: [Image!]!
}

type Image {
  id: ID!
  rank: Int!
  url: String!
}

input InputImage {
  rank: Int!
  url: String!
}

input InputSalesItem {
  name: String!
  priceInCents: Int!
  images: [InputImage!]!
}

type IdResponse {
  id: ID!
}

type Query {
  salesItems: [SalesItem!]!
  salesItem(id: ID!): SalesItem!
}

type Mutation {
  createSalesItem(inputSalesItem: InputSalesItem!): SalesItem!

  updateSalesItem(
    id: ID!,
    inputSalesItem: InputSalesItem
  ): IdResponse!

  deleteSalesItem(id: ID!): IdResponse!
}
"""
)

query = QueryType()


@query.field('salesItems')
def resolve_sales_items(*_):
    return sales_item_service.get_sales_items()


@query.field('salesItem')
def resolve_sales_item(*_, id: str):
    return sales_item_service.get_sales_item(id)


mutation = MutationType()


@mutation.field('createSalesItem')
def resolve_create_sales_item(*_, inputSalesItem):
    input_sales_item = InputSalesItem.model_validate(inputSalesItem)
    return sales_item_service.create_sales_item(input_sales_item)


@mutation.field('updateSalesItem')
def resolve_update_sales_item(*_, id: str, inputSalesItem):
    input_sales_item = InputSalesItem.model_validate(inputSalesItem)
    sales_item_service.update_sales_item(id, input_sales_item)
    return {'id': id}


@mutation.field('deleteSalesItem')
def resolve_delete_sales_item(*_, id: str):
    sales_item_service.delete_sales_item(id)
    return {'id': id}


executable_schema = make_executable_schema(schema, [query, mutation])
