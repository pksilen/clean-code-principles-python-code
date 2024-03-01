from asyncio import gather
import os

from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from httpx import AsyncClient

query = QueryType()

type_defs = gql(
    """
  type UserAccount {
    id: ID!,
    userName: String!
    # Define additional properties...
  }

  type SalesItem {
    id: ID!,
    name: String!
    # Define additional properties...
  }

  type Order {
    id: ID!,
    userId: ID!
    # Define additional properties...
  }

  type User {
    userAccount: UserAccount!
    salesItems: [SalesItem!]!
    orders: [Order!]!
  }

  type Query {
    user(id: ID!): User!
  }
"""
)

USER_ACCOUNT_SERVICE_URL = os.environ.get('USER_ACCOUNT_SERVICE_URL')
SALES_ITEM_SERVICE_URL = os.environ.get('SALES_ITEM_SERVICE_URL')
ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL')


@query.field('user')
async def resolve_user(_, info, id):
    async with AsyncClient() as client:
        [
            user_account_service_response,
            sales_item_service_response,
            order_service_response,
        ] = await gather(
            client.get(f'{USER_ACCOUNT_SERVICE_URL}/user-accounts/{id}'),
            client.get(
                f'{SALES_ITEM_SERVICE_URL}/sales-items?userAccountId={id}'
            ),
            client.get(f'{ORDER_SERVICE_URL}/orders?userAccountId={id}'),
        )

    user_account_service_response.raise_for_status()
    sales_item_service_response.raise_for_status()
    order_service_response.raise_for_status()

    return {
        'userAccount': user_account_service_response.json(),
        'salesItems': sales_item_service_response.json(),
        'orders': order_service_response.json(),
    }


schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
