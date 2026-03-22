import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# define type
@strawberry.type
class Order:
    id: int
    product: str
    quantity: int
    
orders_db = [
    Order(id=1, product="book", quantity=10),
    Order(id=2, product="food", quantity=14)
]

@strawberry.type
class Query:
    @strawberry.field
    # get all orders
    def orders(self) -> list[Order]:
        return orders_db

    @strawberry.field
    # get order by ID
    def order(self, id: int) -> Order | None:
        for order in orders_db:
            if order.id == id:
                return order
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createOrder(self, product: str, quantity: int) -> Order:
        new_order = Order(
            id=len(orders_db) + 1,
            product=product,
            quantity=quantity
        )

        orders_db.append(new_order)
        return new_order


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

app.include_router(GraphQLRouter(schema), prefix="/graphql")