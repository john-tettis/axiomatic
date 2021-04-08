import requests

url = "https://zenquotes.io/api/"

response = requests.request("GET", f'{url}/today')


def retrieve_quotes(filter):
    '''Retreive quotes from api or database depending on filter'''

    if filter == 'famous':
        return get_famous_quotes(50)




def get_famous_quotes(limit):
    """Send request to api for 50 random quotes"""
    response = requests.request("GET", f'{url}/quotes')
    quotes = []

    for obj in response.json():

        quotes.append({
            'content': obj['q'],
            'author': obj['a']
        })
    return quotes