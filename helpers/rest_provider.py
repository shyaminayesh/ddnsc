import json
import requests
from helpers.logger import Logger


class RestProvider:
    def __init__(self, base_url, auth, headers):
        self.base_url = base_url
        self.headers = headers
        self.auth = auth

    def get(self, endpoint):
        """
        :param endpoint: REST API endpoint to GET
        :returns: Str response. If error, returns None
        """
        try:

            res = requests.get(f"{self.base_url}/{endpoint}", auth=self.auth, headers=self.headers)


            '''
            Return the response text if everything goes correctly
            and the server response with 200 HTTP code.
            '''
            if res.status_code == 200:
                return res.text


            if res.status_code != 200:
                Logger.error("ERROR: Status code is {res.status_code}."
                             f"Response: {res.text}")
                return None


        except requests.exceptions.RequestException as e:
            Logger.error(f"Request failed: {e}")
            return None

    def get_json(self, endpoint):
        """
        :param endpoint: REST API endpoint to GET
        :returns: dict representing json response. If error, returns None
        """
        resp = self.get(endpoint)
        json_resp = None

        try:
            json_resp = json.loads(resp)
        except json.JSONDecodeError:
            Logger.error(f"Invalid response to request at endpoint {endpoint}")
        return json_resp



    '''
    Some API need POST request instead of PUT. This
    method will implement POST interface for the
    REST Provider
    '''
    def post(self, endpoint, data):
        try:

            Response = requests.post(f"{self.base_url}/{endpoint}", headers=self.headers, auth=self.auth, data=json.dumps(data))

            '''
            If something goes wrong we'll get status code that
            not eq to 200
            '''
            if Response.status_code != 200:
                Logger.error(f"Response code {Response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            Logger.error(f"Request failed : {e}")
            return False
        finally:
            return True



    def put(self, endpoint, data):
        """
        :param endpoint: REST API endpoint to GET
        :param data: dict of data to send (as json)
        :returns: True if succesful, else False
        """
        try:
            res = requests.put(f"{self.base_url}/{endpoint}", headers=self.headers, auth=self.auth, data=json.dumps(data))
            if res.status_code != 200:
                Logger.error(f"Status code is {res.status_code}. "
                             f"Response: {res.text}")
                return False
        except requests.exceptions.RequestException as e:
            Logger.error(f"Request failed: {e}")
            return False
        return True
