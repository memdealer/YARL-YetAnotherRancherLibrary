import requests
import urllib3

# Disable bitchy SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class RancherCow():
    ''' Rancher Client API class'''

    def __init__(self, rancher_url, rancher_access_key, rancher_secret_key, rancher_env):
        self.__host = rancher_url
        self.__session = requests.Session()
        self.__session.auth = (rancher_access_key, rancher_secret_key)
        self.__session.headers = {'Content-Type': 'application/json'}
        self.__session.verify = False
        self.__access_key = rancher_access_key
        self.__secret_key = rancher_secret_key
        self.___env = (lambda: self.__session
                       .get(self.__host + '/project?name={0}' \
                       .format(rancher_env)) \
                       .json()['data'][0]['id'])()
        if self.___env in (None, ''):
            exit(1)

    def POST_(self, url):
        ''' POST supressor'''

        responce = self.__session.post(self.__host + url)

        return responce

    def GET_(self, url):
        ''' GET supressor '''

        responce = self.__session.get(self.__host + url)

        return responce

    def get_env_id(self, env):
        ''' Return name_ID by name given '''

        r = self.GET_('/project?name={0}'.format(env)).json()

        return r['data'][0]['id']


    def get_container_id(self, container_name):
        ''' Return container ID by name given '''

        r = self.GET_('/projects/{0}/instances?name={1}'.format(self.___env, container_name)) \
            .json()

        return r['data'][0]['id']


    def start_container(self, container_id):
        ''' Stop container ID '''
        r = self.POST_('/projects/{0}/containers/{1}/?action=start'.format(self.___env, container_id))

        if r.status_code not in (200, 202):
            return True
        return False

    def stop_container(self, container_id):
        ''' Start container ID'''

        r = self.POST_('/projects/{0}/containers/{1}/?action=stop'.format(self.___env, container_id))

        if r.status_code not in (200, 202):
            return True
        return False
