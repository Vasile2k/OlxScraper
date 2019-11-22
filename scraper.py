__author__ = "Vasile2k"

import requests
from html.parser import HTMLParser

queries = [
    "Corsair K95",
    "Gigabyte Aorus Z390 Pro"
]

url = "https://www.olx.ro/oferte/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/35.0.1916.47 Safari/537.36"
headers = {"User-Agent": user_agent}

products = {}
last_product = []


def clean_string(input):
    # clean the data from tabs, spaces, slashes and/or newlines
    #          because as I see, the parser gives a lot of them
    #                              and '\n', because fuck python
    return str(input).replace("\n", "").replace("\\n", "").replace("\t", "").replace(" ", "").replace("\\", "")


def clean_shitty_decoding(input):
    # clean the unescaped string
    # encode all symbols to unicode, escape them, keep only ascii, decode
    # now you have a clean string
    # fuck python
    return str(input).encode("utf-8").decode("unicode_escape").encode("ascii", errors="ignore").decode()


def add_product(product):
    if not last_product == []:
        raise Exception("Add the price of the previous product before adding a new one!")
    if not isinstance(product, str):
        raise TypeError("\'product\' should be a string!")
    last_product.append(product)


def add_price(price):
    if last_product == []:
        raise Exception("Add a product before adding a price!")
    if not isinstance(price, str):
        raise TypeError("\'price\' should be a string!")
    products[last_product[0]] = price
    last_product.clear()


def list_all_products():
    max_len = max(len(p) for p in products)
    for k in products:
        print(k.ljust(max_len + 4), " -> ", products[k])


class OlxResponseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.__inside_table_count = 0
        self.__has_data = False
        self.__has_price_data = False

    def handle_starttag(self, tag, attrs):
        # convert attrs to dict
        attrs = dict(attrs)
        # clean the tag attribute because the parser seem so add a lot of shit
        tag = clean_string(tag)
        if tag == "table" and "id" in attrs and attrs["id"] == "offers_table":
            # start the table with listings
            self.__inside_table_count = 1
        if self.__inside_table_count:
            if tag == "table":
                # incremet table counte because there are tables inside the table with listings
                self.__inside_table_count += 1
            elif tag == "a" and "data-cy" in attrs and attrs["data-cy"] == "listing-ad-title":
                self.__has_data = True
            elif tag == "p" and "class" in attrs and attrs["class"] == "price":
                self.__has_price_data = True

    def handle_endtag(self, tag):
        if tag == "table" and self.__inside_table_count:
            self.__inside_table_count -= 1

    def handle_data(self, data):
        if not clean_string(data) == "":
            if self.__has_data:
                add_product(clean_shitty_decoding(data))
                self.__has_data = False
            elif self.__has_price_data:
                add_price(clean_shitty_decoding(data))
                self.__has_price_data = False


def create_query_url(query_text):
    return url + "q-" + query_text.replace(" ", "-") + "/"

if __name__ == "__main__":
    for query in queries:
        response = requests.get(create_query_url(query), headers=headers)
        parser = OlxResponseParser()
        parser.feed(str(response.content))
        parser.close()

    list_all_products()
