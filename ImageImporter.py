#!/usr/bin/env python3

import requests
import hashlib
import json

okta_url = 'https://[COMPANY].okta.com'
api_token = 'TOKEN'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'SSWS ' + api_token
}

# pull user data from Okta
userData = requests.get(okta_url + '/api/v1/users/', headers=headers).json()

for item in userData:
    try:
        # check if entry has Bamboo HR employee number, KeyError means no entry and will skip
        x = item['profile']['employeeNumber']

        # collect profile values
        userId = str(item['id'])
        email = item['profile']['email']
        emailHash = hashlib.md5(email.encode('utf-8')).hexdigest()

        # build data to POST back to Okta
        data = {}
        profile = {}
        profile["profileImage"] = "https://COMPANY.bamboohr.com/employees/photos/?h=" + emailHash
        data["profile"] = profile

        # post

        r = requests.post(okta_url + '/api/v1/users/' + userId, headers=headers, json=data)
        print(r)
        # print(email + ' has been updated')

    except KeyError:
        continue
