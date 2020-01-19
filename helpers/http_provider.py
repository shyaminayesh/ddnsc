import requests
from urllib.parse import quote


class HttpProvider:
    def __init__(self, base_url):
        self.base_url = base_url

    @staticmethod
    def get(url):
        """
        :param url: url to HTTP GET
        :returns: Str response. If error, returns None
        """
        try:
            res = requests.get(url)
            '''
            Return the response text if everything goes correctly
            and the server response with 200 HTTP code.
            '''
            if res.status_code == 200:
                return res.text
            if res.status_code != 200:
                print(f"ERROR: Status code is {res.status_code}."
                      f"Response: {res.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed: {e}")
            return None

    def get_q_string(self, query_string):
        """
        :param query_string: query string in dict, where key is LHS, and value
            is RHS for each query string pair
        :returns: Str response. If error, returns None
        """
        q_string = '?'
        for k, v in query_string.items():
            q_string += f"{quote(k)}={quote(v)}&"
        try:
            res = requests.get(f"{self.base_url}{q_string}")
            '''
            Return the response text if everything goes correctly
            and the server response with 200 HTTP code.
            '''
            if res.status_code == 200:
                return res.text
            if res.status_code != 200:
                print(f"ERROR: Status code is {res.status_code}."
                      f"Response: {res.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed: {e}")
            return None
