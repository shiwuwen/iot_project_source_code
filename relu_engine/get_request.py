import requests as re


def get_val(post_url):
    response = re.get(post_url)
    data = response.json()
    print(data)


if __name__ == '__main__':
    url = 'http://localhost:5000/air_conditioning_start'
    url2 = 'http://localhost:5000/air_conditioning_run'
    get_val(url)
    index = 10
    while index:
        get_val(url2)
