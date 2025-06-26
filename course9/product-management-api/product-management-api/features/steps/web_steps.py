from behave import given, when, then
import json

@given('the following products exist')
def step_impl(context):
    for row in context.table:
        product_data = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].lower() == "true",
            "category": row["category"]
        }
        context.client.post("/products", json=product_data)

@when('I request "{method}" for product with id "{id}"')
def step_impl(context, method, id):
    context.response = context.client.request(
        method,
        f"/products/{id}",
        headers={"Content-Type": "application/json"}
    )

@when('I request "{method}" for "{path}"')
def step_impl(context, method, path):
    context.response = context.client.request(
        method,
        path,
        headers={"Content-Type": "application/json"}
    )

@when('I request "{method}" for product with id "{id}" with body')
def step_impl(context, method, id):
    data = json.loads(context.text)
    context.response = context.client.request(
        method,
        f"/products/{id}",
        json=data,
        headers={"Content-Type": "application/json"}
    )

@then('I should see a status code of {code}')
def step_impl(context, code):
    assert context.response.status_code == int(code)

@then('I should see "{text}" in the response')
def step_impl(context, text):
    assert text in context.response.get_data(as_text=True)

@then('I should not see "{text}" in the response')
def step_impl(context, text):
    assert text not in context.response.get_data(as_text=True)