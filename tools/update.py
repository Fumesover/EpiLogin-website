#!/usr/bin/python

import requests
import sys

API_EPILOGIN = "https://epilogin.fr/api"
# API_EPILOGIN = "http://127.0.0.1:8000/api"
API_CRI = "https://cri.epita.fr/api"

def get_headers(header, token):
    return {'Authorization': header + ' ' + token}

def fetch_paginate(next, token, header):
    output = []

    while next:
        print(next)
        r = requests.get(next, headers=get_headers(header, token))

        if r.status_code != 200:
            print('Request failed,', next, r.status_code)
            return None

        data = r.json()

        output += data['results']
        next = data['next']
    
    return output

def add_group(email, group, token):
    r = requests.post(API_EPILOGIN + "/groups/", {
        'email': email,
        'group': group
        }, headers=get_headers("Token", token))
    
    if r.status_code != 201:
        print('Request failed:', "add_group:", email, group, r.status_code)

    r = requests.post(API_EPILOGIN + "/updates/", {
            'type': 'addgroup',
            'ban_type': 'group',
            'email': email,
            'value': group,
            'author': 0
        }, headers=get_headers("Token", token))

    if r.status_code != 201:
        print('Request failed:', "add_group_update:", email, group, r.status_code)

def del_group(email, group, token):
    groups = fetch_paginate(
            API_EPILOGIN + "/groups/?email={}&group={}".format(email, group),
            token, "Token")

    for group in groups:
        r = requests.delete(API_EPILOGIN + "/groups/{}/".format(group['id']),
            headers=get_headers("Token", token))

        if r.status_code != 204:
            print('Request failed:', "del_group:", email, group['id'], r.status_code)

        r = requests.post(API_EPILOGIN + "/updates/", {
                'type': 'delgroup',
                'ban_type': 'group',
                'email': email,
                'value': group['group'],
                'author': 0
            }, headers=get_headers("Token", token))

        if r.status_code != 201:
            print('Request failed:', "del_group_update:", email, group, r.status_code)

def main(TOKEN_API, TOKEN_CRI):
    el_data = fetch_paginate(API_EPILOGIN + "/groups/", TOKEN_API, "Token")

    el_users = {}
    for group in el_data:
        if not group['email'] in el_users:
            el_users[group['email']] = []
        el_users[group['email']].append(group['group'])

    cri_data = fetch_paginate(API_CRI + "/users/", TOKEN_CRI, "Basic")

    for user in cri_data:
        if not user['mail']:
            continue

        if user['mail'] == "paul.hervot@epita.fr":
            print(user)
            print(el_users[user['mail']])
            print(user['class_groups'] + [user['promo']])

        if user['mail'] in el_users:
            el_user = el_users[user['mail']]
            user_groups = user['class_groups'] + [user['promo']]
            for rank in user_groups:
                if not rank in el_user:
                    add_group(user['mail'], rank, TOKEN_API)
                    print("Go add", rank, "for", user['mail'])

            for rank in el_user:
                if rank[0] != '@' and not rank in user_groups:
                    del_group(user['mail'], rank, TOKEN_API)
                    print("Go rem", rank, "for", user['mail'])
        else:
            for rank in user['class_groups'] + [user['promo']]:
                print("Go add", rank, "for", user['mail'])
                add_group(user['mail'], rank, TOKEN_API)

    return cri_data

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("\t", sys.argv[0], "[token_api]", "[token_cri]")
        exit(1)

    main(sys.argv[1], sys.argv[2])

