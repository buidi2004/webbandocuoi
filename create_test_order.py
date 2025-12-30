import requests
import json

# Create a test order
url = "https://ivie-backend.onrender.com/api/don_hang/"

order_data = {
    "customer_name": "Nguyễn Văn A",
    "customer_email": "test@example.com",
    "customer_phone": "0123456789",
    "shipping_address": "123 Đường ABC, Quận 1, TP.HCM",
    "total_amount": 1500000,
    "items": [
        {
            "product_id": 1,
            "quantity": 1,
            "price": 1500000,
            "loai": "mua",
            "rental_days": 0
        }
    ],
    "payment_method": "cod",
    "delivery_type": "delivery",
    "note": "Đơn hàng test"
}

print("Creating test order...")
try:
    response = requests.post(url, json=order_data, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        order = response.json()
        print(f"Order created: {json.dumps(order, indent=2, ensure_ascii=False)}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
