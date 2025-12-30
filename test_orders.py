import requests
import json

# Test get orders
url = "https://ivie-backend.onrender.com/api/don_hang/"

print("Testing orders endpoint...")
try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        orders = response.json()
        print(f"Number of orders: {len(orders)}")
        if orders:
            print(f"First order: {json.dumps(orders[0], indent=2, ensure_ascii=False)}")
        else:
            print("No orders found in database")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
