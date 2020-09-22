from time import sleep
import requests
import urllib3


# Disable bitchy SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RancherException(Exception):
    pass


class RancherCow():
    ''' Rancher Client API class'''

    def __init__(self, rancher_url, rancher_access_key, rancher_secret_key, rancher_env):
        self.__host = rancher_url + "/v2-beta"
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
            raise RancherException(f"Cannot allocate such env{rancher_env}")
            exit(1)

    def __PUT__(self, url, data):
        ''' POST supressor'''

        responce = self.__session.put(self.__host + url, json=data)

        return responce

    def __POST__(self, url):
        ''' POST supressor'''

        responce = self.__session.post(self.__host + url)

        return responce

    def __POST_DATA__(self, url, data):
        ''' POST supressor'''
        header = {'content-type': 'application/json'}
        responce = self.__session.post(self.__host + url, headers=header, data=data)

        return responce

    def __GET__(self, url):
        ''' GET supressor '''

        responce = self.__session.get(self.__host + url)

        return responce

    def get_env_id(self, env):
        ''' Return name_ID by name given '''

        try:
            r = self.__GET__('/project?name={0}'.format(env)).json()
            environment = r['data'][0]['id']
        except IndexError:
            return False
        return environment

    def get_container_id(self, container_name):
        ''' Return container ID by name given '''

        try:
            r = self.__GET__('/projects/{0}/instances?name={1}'.format(self.___env, container_name)).json()
            container_id = r['data'][0]['id']
        except IndexError:
            raise RancherException
        return container_id


    def start_container(self, container_id):
        ''' Stop container ID '''
        r = self.__POST__('/projects/{0}/containers/{1}/?action=start'.format(self.___env, container_id))

        if r.status_code not in (200, 202):
            return True
        return False

    def restart_container(self, container_id):
        ''' restart container ID '''
        r = self.__POST__('/projects/{0}/containers/{1}/?action=restart'.format(self.___env, container_id))

        if r.status_code not in (200, 202):
            return True
        return False


    def stop_container(self, container_id):
        ''' Start container ID'''

        r = self.__POST__('/projects/{0}/containers/{1}/?action=stop'.format(self.___env, container_id))

        if r.status_code not in (200, 202):
            return True
        return False

    def get_host_property(self, host_name):
        ''' Get memory/CPU info from host, via rancher agent '''

        r = self.__GET__('/projects/{0}/hosts'.format(self.___env)).json()
        for host in r['data']:
            if host['hostname'].startswith(host_name):
                return host['id'], host['info']['memoryInfo']['memTotal'], int(host['info']['cpuInfo']['count']*1000)
        return False

    def get_current_limits(self, host_name):
        ''' Get current limits set in rancher '''

        r = self.__GET__('/projects/{0}/hosts'.format(self.___env)).json()
        for host in r['data']:
            if host['hostname'].startswith(host_name):
                return host['id'], int(host['memory']/1024/1024), host['milliCpu']
        return False

    def update_host_limits(self, host_name, cpu_limit, memory_limit):
        ''' Set host limits, memory/CPU (bytes/milliCPU) '''

        memory_limit = memory_limit * 1024 * 1024
        cpu_limit = cpu_limit * 1000

        r = self.__GET__('/projects/{0}/hosts'.format(self.___env)).json()
        for host in r['data']:
            if host['hostname'].startswith(host_name):
                host_id = host['id']
                break
        else:
            return False

        data = { "memory": memory_limit, "milliCpu": cpu_limit }
        r = self.__PUT__('/projects/{0}/hosts/{1}'.format(self.___env, host_id), data)
        if r.status_code != 200:
            return False
        return True

    def get_status_of_container(self, container_id):
        ''' Get current state of container '''

        r = self.__GET__('/projects/{0}/containers/{1}/'.format(self.___env, container_id))
        if r.status_code not in (200, 201, 202):
            raise RancherException
        return r.json()['state']

    def watch_container(self, desired_state, container_id, check_seconds=30, iterations=3):
        """ Watch for container, untill its desired state"""
        iter_level = 0
        container_state = self.get_status_of_container(container_id)

        while container_state != desired_state:
            container_state = self.get_status_of_container(container_id)
            sleep(check_seconds)
            iter_level += 1
            if iter_level == iterations and container_state != desired_state:
                return False
        return True

    def execute_inside(self, container_id, command_to_execute):
        from websocket import create_connection
        from base64 import b64encode

        if not isinstance(command_to_execute, str):
            raise ValueError

        message = command_to_execute + "\n"
        message = message.encode('ascii')
        base64_bytes = b64encode(message).decode('ascii')

        data = '{"attachStdin":true,"attachStdout":true,"tty":true,"command":["/bin/sh","-c","TERM=xterm-256color; ' \
               'export TERM; [ -x /bin/bash ] && ([ -x /usr/bin/script ] && /usr/bin/script -q -c \\"/bin/bash\\"' \
               ' /dev/null || exec /bin/bash) || exec /bin/sh"]}'

        r = self.__POST_DATA__("/projects/{0}/containers/{1}?action=execute"
                               .format(self.___env, container_id), data)\
                               .json()

        ws_connection = r['url'] + "?token=" + r['token']
        try:
            ws = create_connection(ws_connection)
            ws.send(base64_bytes)
        except Exception:
            return False
        finally: ws.close()

        return True

    def close_connection(self):
        self.__session.close()
