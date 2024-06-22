import pycurl
from io import BytesIO
import json

class HTTPRequest:
    
    def __init__(self, base_url):
        self.base_url = base_url

    def _perform_request(self, url, custom_request=None, headers=None, data=None, timeout=None):
        buffer = BytesIO()
        c = pycurl.Curl()

        try:
            c.setopt(c.URL, url)
            if custom_request:
                c.setopt(c.CUSTOMREQUEST, custom_request)
            if headers:
                c.setopt(c.HTTPHEADER, headers)
            if data:
                c.setopt(c.POSTFIELDS, json.dumps(data))
            if timeout:
                c.setopt(c.TIMEOUT, timeout)
            c.setopt(c.WRITEDATA, buffer)

            c.perform()
            status_code = c.getinfo(c.RESPONSE_CODE)
            c.close()

            body = buffer.getvalue().decode('utf-8') if buffer.getvalue() else None
            return status_code, body
        
        except pycurl.error as e:
            c.close()
            raise Exception(f"An error occurred: {e}")
        
        finally:
            buffer.close()

    def get_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = ['Accept: application/json']

        status_code, body = self._perform_request(url, headers=headers)

        if status_code == 200:
            return json.loads(body)
        else:
            raise Exception(f"GET request failed with status code: {status_code}")

    def put_request(self, endpoint, data, timeout=10):
        url = f"{self.base_url}{endpoint}"
        headers = ['Accept: application/json', 'Content-Type: application/json']

        status_code, body = self._perform_request(url, custom_request='PUT', headers=headers, data=data, timeout=timeout)

        if status_code in [200, 201]:
            return json.loads(body)
        else:
            raise Exception(f"PUT request failed with status code: {status_code}")

    def delete_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = ['Accept: application/json']

        status_code, _ = self._perform_request(url, custom_request='DELETE', headers=headers)

        if status_code == 204:
            return {"message": "Resource deleted successfully"}
        else:
            raise Exception(f"DELETE request failed with status code: {status_code}")
