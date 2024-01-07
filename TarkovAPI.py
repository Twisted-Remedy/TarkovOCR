import requests

def getItemInfo(name: str):
    query = f"""
    {{
        items(name: "{name}") {{
            name
            shortName
            avg24hPrice
            sellFor{{
                vendor{{
                    name
                }}
                price
                currency
            }}
        }}
    }}
    """

    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    try:
        if response.status_code == 200:
            return response.json()['data']['items'][0]
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
    except IndexError:
        print(f"Failed to get item! ({name})")
        return 0

def getBestTrader(vendorData):
    price = 0
    for i, x in enumerate(vendorData['sellFor']):
        if x['vendor']['name'] == "Flea Market":
            continue
        if x['price'] > price:
            price = x['price']
            vendor = x
    return vendor