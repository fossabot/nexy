import json

import certifi
import urllib3


class NexusService:

    def __init__(self, url, username, password):
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        self.url = url
        self.headers = urllib3.util.make_headers(
            basic_auth='{0}:{1}'.format(username, password),
            accept_encoding='application/json'
        )

    def find_repositories(self):
        """Find all repositories"""
        # Generate uri to call
        uri = "{}/service/rest/v1/repositories".format(self.url)
        response = self.http.request(
            'GET',
            uri,
            headers=self.headers,
            retries=False
        )

        # Check response status
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))
        else:
            self.__handle_error(response)

    def find_components(self, repository):
        """Find all components"""
        # Iterate over each result
        next_token = None
        components = []
        while True:
            # Generate uri to call
            if next_token is None:
                uri = "{0}/service/rest/v1/components?repository={1}".format(self.url, repository)
            else:
                uri = "{0}/service/rest/v1/components?repository={1}&continuationToken={2}".format(
                    self.url,
                    repository,
                    next_token
                )

            # Send request and get response
            response = self.http.request(
                'GET',
                uri,
                headers=self.headers,
                retries=False
            )

            # Check response status
            if response.status == 200:
                doc = json.loads(response.data.decode('utf-8'))
                components += doc['items']

                if doc['continuationToken'] is not None:
                    next_token = doc['continuationToken']
                else:
                    break
            elif response.status == 404:
                raise ValueError('Repository not found')
            else:
                self.__handle_error(response)

        return components

    def delete_component(self, id):
        """Delete a component"""
        response = self.http.request(
            'DELETE',
            "{0}/service/rest/v1/components/{1}".format(self.url, id),
            headers=self.headers,
            retries=False
        )
        # Check response status
        if response.status != 204:
            raise ValueError("Can't delete component: {}".format(id))

    def find_tasks(self):
        """Find all tasks"""
        response = self.http.request(
            'GET',
            "{0}/service/rest/v1/tasks".format(self.url),
            headers=self.headers,
            retries=False
        )
        # Check response status
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))['items']
        else:
            self.__handle_error(response)

    def start_task(self, id):
        """Start a task"""
        response = self.http.request(
            'POST',
            "{0}/service/rest/v1/tasks/{1}/run".format(self.url, id),
            headers=self.headers,
            retries=False
        )
        if response.status == 204:
            pass
        elif response.status == 404:
            raise ValueError('Task not found')
        else:
            self.__handle_error(response)

    def stop_task(self, id):
        """Stop a task"""
        response = self.http.request(
            'POST',
            "{0}/service/rest/v1/tasks/{1}/stop".format(self.url, id),
            headers=self.headers,
            retries=False
        )
        if response.status == 404:
            raise ValueError('Task not found')
        elif response.status == 409:
            raise ValueError('Unable to stop task')
        else:
            self.__handle_error(response)

    @staticmethod
    def __handle_error(response):
        if response.status == 401:
            raise ValueError('Invalid credentials')
        else:
            raise ValueError('Unhandle error')
