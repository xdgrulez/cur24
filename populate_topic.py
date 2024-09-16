import os
import pickle
from scrape_products import scrape
from kafi.kafi import *
#
c = Cluster("local")
#
print("Scraping...")
if os.path.exists("products.pickle"):
  p = open("products.pickle", "rb")
  product_dict_list = pickle.load(p)
  p.close()
else:   
  product_dict_list = scrape(["cheese.html", "chocolate.html"])
  p = open("products.pickle", "wb")
  pickle.dump(product_dict_list, p)
  p.close()
print("...done.")
#
first_100_product_dict_list = product_dict_list[0:100]
first_100_pryce_product_dict_list = []
for product_dict in first_100_product_dict_list:
    product_dict["pryce"] = product_dict["price"]
    del product_dict["price"]
    first_100_pryce_product_dict_list.append(product_dict)
#
remaining_product_dict_list = product_dict_list[100:]
#
c.retouch("products")
#
sr = c.schemaRegistry
if "products-value" in sr.get_subjects():
  sr.delete_subject("products-value", permanent=True)
#
cp = c.producer("products")
print("Producing the first 100 messages...")
cp.produce(first_100_pryce_product_dict_list)
print("...done.")
cp.close()
#
schema_str = '''
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
cp = c.producer("products", value_type="jsonschema", value_schema=schema_str)
print("Producing the remaining messages...")
cp.produce(remaining_product_dict_list)
print("...done.")
cp.close()
