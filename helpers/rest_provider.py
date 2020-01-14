import json
import requests


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
                print(f"ERROR: Status code is {res.status_code}." f"Response: {res.text}")
                return None


        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed: {e}")
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
            print(f"ERROR: Invalid response to request at endpoint {endpoint}")
        return json_resp

    def put(self, endpoint, data):
        """
        :param endpoint: REST API endpoint to GET
        :param data: dict of data to send (as json)
        :returns: True if succesful, else False
        """
        try:
            res = requests.put(f"{self.base_url}/{endpoint}", headers=self.headers, auth=self.auth, data=json.dumps(data))
            if res.status_code != 200:
                print(f"ERROR: Status code is {res.status_code}. "
                      f"Response: {res.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed: {e}")
            return False
        return True
