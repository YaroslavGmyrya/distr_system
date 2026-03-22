# Реализуйте здесь клиент для GraphQL.
import requests

def build_payload(query: str, variables: dict) -> dict:
    """
    Формирует словарь для отправки GraphQL запроса.
    
    :param query: Текст запроса (query или mutation).
    :param variables: Словарь с переменными.
    :return: Словарь с ключами "query" и "variables".
    """
    # Ваш код здесь
    return {"query": query, "variables": variables}

URL = "http://127.0.0.1:8000/graphql"

query = """
query GetOrders {
  orders {
    id
    product
    quantity
  }
}
"""

query2 = """
mutation CreateOrder($product: String!, $quantity: Int!) {
  createOrder(product: $product, quantity: $quantity) {
    id
    product
    quantity
  }
}
"""

request_1 = build_payload(query=query, variables={})
request_2 = build_payload(query=query2, variables={"product":"book", "quantity":200})


response = requests.post(URL, json=request_1)

print("BEFORE REQUEST:\n",response.content)
print("\n\n")


response = requests.post(URL, json=request_2)

print("REQUEST ANSWER:\n",response.content)
print("\n\n")

response = requests.post(URL, json=request_1)

print("AFTER REQUEST:\n",response.content)
print("\n\n")

