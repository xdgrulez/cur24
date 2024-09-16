from scrape_products import scrape
from kafi.kafi import *
#
c = Cluster("local")
#
product_dict_list = scrape(["cheese.html", "chocolate.html"])
first_100_product_dict_list = product_dict_list[0:100]
second_100_product_dict_list = product_dict_list[100:200]
second_100_ID_product_dict_list = []
for product_dict in second_100_product_dict_list:
    product_dict["ID"] = product_dict["id"]
    del product_dict["id"]
    second_100_ID_product_dict_list.append(product_dict)
# for product_dict in second_100_ID_product_dict_list:
#     print(product_dict)
remaining_product_dict_list = product_dict_list[200:]
#
# print(len(second_100_product_dict_list))
# print(first_100_product_dict_list[99])
# print(second_100_product_dict_list[0])
# print(len(remaining_product_dict_list))
# print(len(product_dict_list))
#
c.retouch("products")
#
sr = c.schemaRegistry
sr.delete_subject("products-value")
#
cp = c.producer("products")
cp.produce(first_100_product_dict_list)
cp.close()
#
malformed_schema_str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Product",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The name of the product"
    },
    "price": {
      "type": "string",
      "description": "The price of the product"
    },
    "url": {
      "type": "string",
      "description": "The URL of the product"
    },
    "id": {
      "type": "string",
      "description": "The unique identifier of the product"
    },
    "version": {
      "type": "string",
      "description": "The version of the product"
    },
    "price_unit": {
      "type": "string",
      "description": "The unit of the price"
    },
    "weight": {
      "type": "string",
      "description": "The weight of the product"
    }
  },
  "required": ["name", "price", "url"]
}
'''
cp = c.producer("products", value_type="jsonschema", value_schema=malformed_schema_str)
cp.produce(second_100_ID_product_dict_list)
cp.close()
#
well_formed_schema_str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Product",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The name of the product"
    },
    "price": {
      "type": "string",
      "description": "The price of the product"
    },
    "url": {
      "type": "string",
      "description": "The URL of the product"
    },
    "id": {
      "type": "string",
      "description": "The unique identifier of the product"
    },
    "version": {
      "type": "string",
      "description": "The version of the product"
    },
    "price_unit": {
      "type": "string",
      "description": "The unit of the price"
    },
    "weight": {
      "type": "string",
      "description": "The weight of the product"
    }
  },
  "required": ["name", "price", "url", "id"],
  "additionalProperties": false
}
'''
sr = c.schemaRegistry
sr.delete_subject("products-value")
#
cp = c.producer("products", value_type="jsonschema", value_schema=well_formed_schema_str)
cp.produce(remaining_product_dict_list)
cp.close()
