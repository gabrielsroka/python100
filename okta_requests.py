import time
import requests
import datetime
import os

# If you're making multiple API calls, using Session is much faster.
class Session(requests.Session):
    def __init__(self, org_url=os.getenv('OKTA_CLIENT_ORGURL'), token=os.getenv('OKTA_CLIENT_TOKEN')):
        super().__init__()
        self.org_url = org_url
        self.headers['authorization'] = 'SSWS ' + token

    def request(self, method, url, **kwargs):
        if not url.startswith('https:'):
            url = self.org_url + url
        response = super().request(method, url, **kwargs)

        limit = int(response.headers['X-Rate-Limit-Limit'])
        remaining = int(response.headers['X-Rate-Limit-Remaining'])
        # see https://docs.python.org/3/library/datetime.html#datetime.datetime.fromtimestamp
        reset = datetime.datetime.utcfromtimestamp(int(response.headers['X-Rate-Limit-Reset']))
        print(limit, remaining, reset)
        if remaining < 10:
            print('sleeping...')
            while reset > now:
                time.sleep(1) # TODO: calculate sleep time
                now = datetime.utcnow()

        return response

    def post(self, url, json=None):
        return super().post(url, json=json)

    def put(self, url, json=None):
        return super().put(url, json=json)

    def patch(self, url, json=None):
        return super().patch(url, json=json)

    def get_objects(self, url, **params):
        while url:
            response = self.get(url, params=params)
            params = None
            for o in response.json():
                yield o
            url = response.links.get('next', {}).get('url')
