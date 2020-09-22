import requests
import urllib3

# Disable bitchy SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JwtGenException(Exception):
    pass


class RancherAuthToken():
    ''' Rancher api key creation class '''

    def __init__(self, rancher_url, rancher_login, rancher_password):
        self.__host = 'http://' + rancher_url + "/v2-beta"
        self.__session = requests.Session()
        self.__session.verify = True
        self.__rancher_pass = rancher_password
        self.__rancher_login = rancher_login
        self.__jwt = (lambda: self.__session. \
                               post(self.__host + '/token', \
                               data={'code': f'{self.__rancher_login}:{self.__rancher_pass}'}) \
                               .json()['jwt'])()
        self.__env = (lambda: self.__session \
                               .get(self.__host + '/projects', \
                               headers={'Cookie': f'token={self.__jwt}'}) \
                               .json()['data'][0]['id'])()

        if self.__env and self.__jwt == None:
            raise JwtGenException("Cannot generate ENV or JWT token, terminating")

    def generate_api_token(self, name="python_app", description="Python created token"):

        payload = {"name":f"{name}","description":f"{description}"}
        r = self.__session.post(self.__host + '/apikey', \
                                headers={'Cookie': f'token={self.__jwt}'}, \
                                data=payload).json()
        return r['secretValue'], r['publicValue'], r['id']

    def deactivate_api_token(self, id):

        r = self.__session.post(self.__host + f"/apikeys/{id}/?action=deactivate",
                                headers={'Cookie': f'token={self.__jwt}'})

        assert r.status_code != 422, f"Failed to deactivate token id: {id}"
        assert r.json()['state'] == "deactivating", f"Status is not deactivating token id: {id}"

        return True

    def delete_api_token(self, id):

        r = self.__session.delete(self.__host + f'/apikeys/{id}',
                                  headers={'Cookie': f'token={self.__jwt}'})

        assert r.status_code != 422, f"Failed to delete token id: {id}"
        assert r.json()['state'] == "removing", f"Status is not removing token id: {id}"

    def close_connection(self):

        self.__session.close()

        return True
