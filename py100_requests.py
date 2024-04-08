import requests
import os

# Set these:
org_url = os.getenv('OKTA_CLIENT_ORGURL')
token = os.getenv('OKTA_CLIENT_TOKEN')

headers = {
    'authorization': 'SSWS ' + token
}

response = requests.get(org_url + '/api/v1/users/me', headers=headers)
me = response.json()
if response.ok:
    print(me['profile']['login'])
else:
    print('error', me)

# Paginate
url = org_url + '/api/v1/users?limit=2&filter=profile.lastName eq "Doe"'
while url:
    response = requests.get(url, headers=headers)
    users = response.json()

    if response.ok:
        for user in users:
            print(user['profile']['login'])
        url = response.links.get('next', {}).get('url')
        print(url)
    else:
        print('error', users)
