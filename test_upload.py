import requests

# Test upload endpoint
url = "https://ivie-backend.onrender.com/api/tap_tin/upload"

# Create a simple test image (1x1 pixel PNG)
test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

files = {"file": ("test.png", test_image, "image/png")}

print("Testing upload endpoint...")
try:
    response = requests.post(url, files=files, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
