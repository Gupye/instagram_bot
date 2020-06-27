import requests
def get_html(url):
    r = requests.get(url)
    q = r.text
    return (q)