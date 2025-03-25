import requests
import json
from bs4 import BeautifulSoup

def crawl_cnfanssheets_com(product_id):
    all_products = []
    item_types = [
        'shoes',
        'hoodies-sweaters',
        't-shirts',
        'jackets',
        'pants-shorts',
        'headwear',
        'accessories',
        'other-stuff'
    ]

    for _type in item_types:
        page = 0
        while True:
            try:
                # Create URL
                url = 'https://www.cnfanssheets.com/item-type/' + _type + '?2dd7d2d8_page=' + str(page)
                
                # Fetch the webpage content
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find items
                products = soup.find_all(class_='products w-dyn-item w-col w-col-3')
                if products:
                    for product in products:
                        product_data = {}

                        # Add product origin
                        product_data["origin"] = 'cnfanssheets'

                        # Add product ID
                        product_data["id"] = product_id

                        # Extract product title
                        product_title = product.find(class_='productsinfo_title')
                        if product_title:
                            product_data["name"] = product_title.text.strip()
                        else:
                            continue

                        # Extract product image
                        product_image = product.find('img')
                        if product_image:
                            product_data["image"] = product_image.get('src')
                        else:
                            continue

                        # Extract price
                        product_price = product.find(class_='pricesnow')
                        if product_price:
                            product_data["price"] = float(product_price.text[1:])
                        else:
                            continue

                        # Extract product link
                        product_page = product.find(class_='links-block w-inline-block')
                        if not(product_page):
                            continue
                        product_page_url = 'https://www.cnfanssheets.com' + product_page.get('href')
                        print(product_page_url)
                        itempage = requests.get(product_page_url)
                        itempage.raise_for_status()
                        itempage_soup = BeautifulSoup(itempage.text, 'html.parser')
                        product_link = itempage_soup.find(class_='pandabuy-button w-button')
                        if not(product_link):
                            continue
                        product_data["link"] = product_link.get('href')

                        # Add currency
                        product_data["currency"] = 'usd'

                        # Add category
                        product_data["category"] = _type

                        # Add the product data to the list
                        if product_data:
                            all_products.append(product_data)

                        product_id += 1
                            
                else:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching the URL: {e}")

    return all_products

def crawl_cnfanssheet_com(product_id):
    all_products = []
    item_types = {
        "shoes": 10,
        "t-shirts": 12,
        "hoodies": 15,
        "jackets": 16,
        "pants": 17,
    }
    category_map = {
        "shoes": "shoes",
        "t-shirts": "t-shirts",
        "hoodies": "hoodies-sweaters",
        "jackets": "jackets",
        "pants": "pants-shorts",
    }

    for _type in item_types:
        page = 0
        while True:
            try:
                # Create URL
                url = 'https://www.cnfanssheet.com/?category=' + str(item_types[_type]) + '&page=' + str(page) + '&brand=-1'
                
                # Fetch the webpage content
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find items
                products = soup.find_all(class_='item')
                if len(products) > 3:
                    for product in products:
                        product_data = {}

                        # Add product origin
                        product_data["origin"] = "cnfanssheet"

                        # Add product ID
                        product_data["id"] = product_id

                        # Extract product title
                        product_title_container = product.find(class_='name')
                        if not(product_title_container):
                            continue
                        product_title = product_title_container.find('a')
                        if not(product_title):
                            continue
                        product_data["name"] = product_title.text.strip()

                        # Extract product image
                        product_image_container = product.find(class_='thumbnail')
                        if not(product_image_container):
                            continue
                        product_image = product_image_container.find('img')
                        if not(product_image):
                            continue
                        product_data["image"] = product_image.get('src')

                        # Extract product price
                        product_price_container = product.find(class_='price')
                        if not(product_price_container):
                            continue
                        product_price = product_price_container.find('a')
                        if not(product_price):
                            continue
                        product_data["price"] = float(product_price.text[1:])

                        # Add currency
                        product_data["currency"] = 'usd'

                        # Add category
                        product_data["category"] = category_map[_type]

                        # Add the product data to the list
                        if product_data:
                            all_products.append(product_data)

                        product_id += 1
                            
                else:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching the URL: {e}")

    return all_products

def download_and_extract():
    all_products = []
    product_id = 1
    
    print('Crawling cnfanssheets.com')
    all_products.extend(crawl_cnfanssheets_com(product_id))

    print('Crawling cnfanssheet.com')
    all_products.extend(crawl_cnfanssheet_com(product_id))

    # Write the products list to a JSON file
    if all_products:
        with open('products-data.json', 'w') as json_file:
            json.dump(all_products, json_file, indent=4)

        print(f"Data has been written to 'products-data.json'")

if __name__ == "__main__":
    download_and_extract()
