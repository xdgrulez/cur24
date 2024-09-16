from bs4 import BeautifulSoup

# Extractors

def get_article(tag):
    return tag.name == "article"
    

def get_name(tag):
    return tag.name == "span" and tag.has_attr("class") and "ng-star-inserted" in tag.get("class") and tag.has_attr("data-cy") and "product-name" in tag.get("data-cy")


def get_price(tag):
    return tag.name == "span" and tag.has_attr("class") and "actual" in tag.get("class")


def get_price_unit(tag):
    return tag.name == "span" and tag.has_attr("class") and "ng-star-inserted" in tag.get("class") and tag.has_attr("id") and "price-unit" in tag.get("id")


def get_version(tag):
    return tag.name == "span" and tag.has_attr("class") and "ng-star-inserted" in tag.get("class") and tag.has_attr("data-cy") and "product-versioning" in tag.get("data-cy")


def get_weight(tag):
    return tag.name == "span" and tag.has_attr("class") and "weight-priceUnit" in tag.get("class")


def get_detail(tag):
    return tag.name == "div" and tag.has_attr("class") and "show-product-detail" in tag.get("class")


def get_url(tag):
    return tag.name == "a" and tag.has_attr("class") and "show-product-image" in tag.get("class")

# Extract products

def scrape(file_str_list):
    product_dict_list = []
    for file_str in file_str_list:
        with open(file_str, "r") as f:
            content = f.read()
            #
            soup = BeautifulSoup(content, 'html.parser')
            #
            for product_tag in soup.find_all(get_article):
                name_str_list = [tag.contents[0] for tag in product_tag.find_all(get_name)]
                price_str_list = [tag.contents[0] for tag in product_tag.find_all(get_price)]
                if len(name_str_list) == 1 and len(price_str_list) == 1:
                    name_str = name_str_list[0].strip()
                    #
                    price_str = price_str_list[0].strip()
                    #
                    url_str = [url_tag["href"] for detail_tag in product_tag.find_all(get_detail) for url_tag in detail_tag.find_all(get_url)][0]
                    #
                    id_str = url_str.split("/")[-1]
                    ###
                    product_dict = {"name": name_str, "price": price_str, "url": url_str, "id": id_str}
                    ###
                    version_str_list = [tag.contents[0] for tag in product_tag.find_all(get_version)]
                    if len(version_str_list) == 1:
                        product_dict["version"] = version_str_list[0].strip()
                    #
                    price_unit_str_list = [tag.contents[0] for tag in product_tag.find_all(get_price_unit)]
                    if len(price_unit_str_list) == 1:
                        product_dict["price_unit"] = price_unit_str_list[0].strip()
                    #
                    weight_str_list = [tag.contents[1] for tag in product_tag.find_all(get_weight)]
                    if len(weight_str_list) == 1:
                        product_dict["weight"] = weight_str_list[0].strip()
                    #
                    product_dict_list.append(product_dict)
    #
    return product_dict_list


# product_dict_list = scrape(["cur24/cheese.html", "cur24/chocolate.html"])
# for product_dict in product_dict_list:
#     print(product_dict)
# print(len(product_dict_list))
