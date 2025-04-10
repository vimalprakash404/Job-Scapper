import requests



def get_fastest_proxy():
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        proxies = data.get("proxies", [])

        # Filter only alive proxies with a valid average_timeout
        alive_proxies = [
            proxy for proxy in proxies
            if proxy.get("alive") and proxy.get("average_timeout") is not None
        ]

        if not alive_proxies:
            print("No alive proxies with average_timeout found.")
            return None

        # Find the proxy with the lowest average_timeout
        fastest_proxy = min(alive_proxies, key=lambda p: p["average_timeout"])

        print("Fastest proxy found:")
        print(f"Proxy: {fastest_proxy['ip']}")
        print(f"Port: {fastest_proxy['port']}")
        print(f"Average Timeout: {fastest_proxy['average_timeout']} ms")
        return fastest_proxy

    except requests.RequestException as e:
        print("Failed to fetch proxy data:", e)
        return None

# Run the function
get_fastest_proxy()
