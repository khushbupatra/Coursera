Feature: Product Management
  As a store manager
  I want to manage products
  So that I can keep track of inventory

  Scenario: Get a product
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
    When I request "GET" for product with id "1"
    Then I should see a status code of 200
    And I should see "Smartphone" in the response

  Scenario: Update a product
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
    When I request "PUT" for product with id "1" with body
      """
      {
        "name": "Updated Phone",
        "price": 649.99
      }
      """
    Then I should see a status code of 200
    And I should see "Updated Phone" in the response
    And I should see "649.99" in the response

  Scenario: Delete a product
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
    When I request "DELETE" for product with id "1"
    Then I should see a status code of 204
    When I request "GET" for product with id "1"
    Then I should see a status code of 404

  Scenario: List all products
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
      | Laptop       | High performance  | 999.99| true      | Electronics|
    When I request "GET" for "/products"
    Then I should see a status code of 200
    And I should see "Smartphone" in the response
    And I should see "Laptop" in the response

  Scenario: Search products by name
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
      | Laptop       | High performance  | 999.99| true      | Electronics|
    When I request "GET" for "/products?name=Smartphone"
    Then I should see a status code of 200
    And I should see "Smartphone" in the response
    And I should not see "Laptop" in the response

  Scenario: Search products by category
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
      | T-Shirt      | Cotton shirt     | 19.99 | true      | Clothing   |
    When I request "GET" for "/products?category=Electronics"
    Then I should see a status code of 200
    And I should see "Smartphone" in the response
    And I should not see "T-Shirt" in the response

  Scenario: Search products by availability
    Given the following products exist
      | name         | description       | price | available | category   |
      | Smartphone   | Latest model     | 599.99| true      | Electronics|
      | T-Shirt      | Cotton shirt     | 19.99 | false     | Clothing   |
    When I request "GET" for "/products?available=true"
    Then I should see a status code of 200
    And I should see "Smartphone" in the response
    And I should not see "T-Shirt" in the response