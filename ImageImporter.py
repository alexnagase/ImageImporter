#!/usr/bin/env python3

import requests
import hashlib

url = 'https://COMPANY.okta.com'
token = 'TOKEN'

headers = {
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_users(**kwargs):
    # Get Okta users with params, more info: https://developer.okta.com/docs/reference/api/users/#list-users

    return requests.get(url + '/api/v1/users', params=kwargs, headers=headers)


def get_user_pages(**kwargs):
    page = get_users(**kwargs)
    while page:
        yield page
        page = get_next_page(page.links)


def get_next_page(links):
    # Manage Okta response pagination with link headers https://developer.okta.com/docs/reference/api-overview/#pagination
    next = links.get('next')
    if next:
        return requests.get(next['url'], headers=headers)
    else:
        return None


for page in get_user_pages(limit=9, filter=''):
    for user in page.json():

        try:
            # We only want profiles associated with BBHR employee number, KeyError means no BBHR entry and will skip
            x = user['profile']['employeeNumber']

            # Collect values from User's Okta profile
            userId = str(user['id'])
            email = user['profile']['email']
            emailHash = hashlib.md5(email.encode('utf-8')).hexdigest()

            # Build data to POST back to Okta
            data = {}
            profile = {}
            profile["profileImage"] = "https://COMPANY.bamboohr.com/employees/photos/?h=" + emailHash
            data["profile"] = profile

            # POST back to Okta, print response codes

            r = requests.post(url + '/api/v1/users/' + userId, headers=headers, json=data)
            print(email + ' has been updated with response: ' + str(r))
            # print(email + ' has been updated')

        except KeyError:
            #skipped entries
            print("Skipping " + str(user['profile']['email']))
            continue
