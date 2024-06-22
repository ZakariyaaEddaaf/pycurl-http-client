from http_request import HTTPRequest

def main():
    base_url = "https://jsonplaceholder.typicode.com"
    client = HTTPRequest(base_url)
    try:
        users = client.get_request("/users")
        print("GET response:",users)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
