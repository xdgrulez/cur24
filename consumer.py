from kafi.kafi import *
#
c = Cluster("local")
#
result_dict_list = c.map("products", type="jsonschema", map_function=lambda x: {"name": x["value"]["name"], "price": x["value"]["price"]})
#
for result_dict in result_dict_list:
    print(result_dict)
