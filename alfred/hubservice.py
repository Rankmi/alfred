import json

import requests

__base_url = "https://rankmi.myjetbrains.com/hub/api/rest/"
__headers = {'Authorization': 'Bearer perm:ZWRnYXJkby5mcmVkeg==.YWxmcmVk.4cwY2Pw8qm7Z6oMh0Qm2fjqwqiNULF'}


def get_all_users():
    users = requests.get(__base_url + "users", headers=__headers)
    print(json.dumps(users.json(), indent=4))


