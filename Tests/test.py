api_key = "ud4J9RTtncJIFktrHWfpN59y3VLVVfhb"
location = str(input("Enter location: "))

url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

def print_dict(data, indent=0):
    for key, value in data.items():
        print("  " * indent + f"{key}:")
        if isinstance(value, dict):
            print_dict(value, indent + 1)
        else:
            print("  " * (indent + 1) + f"{value}")

if response.status_code == 200:
    data = response.json()
    print_dict(data)
else:
    print("Error:", response.status_code)
