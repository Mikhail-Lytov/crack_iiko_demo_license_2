import api_iiko_back.reguest_iiko_backend as api_iiko
from datetime import datetime, timedelta

TEST_ITEM = "Test beer"


def get_product_id(response_json, product_name):
    for product in response_json:
        if product.get('name') == product_name:
            return product.get('id'), product.get("defaultSalePrice")
    return None

def create_new_document():
    today = datetime.now() + timedelta(days=1)
    date_now = today.strftime("%Y-%m-%d")

    date_to = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    token = api_iiko.get_auth()
    items = api_iiko.get_all_items(token)

    product_id, price = get_product_id(items, TEST_ITEM)

    api_iiko.create_new_document(token, date_now, date_to, product_id, price)

    api_iiko.log_out(token)



if __name__ == '__main__':
    create_new_document()