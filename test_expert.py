import requests
import json

# Test expert creation with minimal fields
API_BASE = "https://ivie-backend.onrender.com"

def test_create_expert():
    """Test creating an expert with minimal required fields"""
    
    expert_data = {
        "name": "Test Expert",
        "title": "Makeup Artist",
        "image_url": "https://i.ibb.co/test.jpg",
        "category": "makeup",
        "level": "senior",
        "location": "Hà Nội",
        "price": 1500000,
        "is_top": False,
        "specialties": ["Cưới", "Sự kiện"]
    }
    
    print("Testing expert creation...")
    print(f"Data: {json.dumps(expert_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{API_BASE}/api/dich_vu/chuyen_gia",
        json=expert_data
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        print("\n✅ Expert created successfully!")
        return response.json()
    else:
        print("\n❌ Failed to create expert")
        return None

def test_get_experts():
    """Get all experts"""
    print("\n\nGetting all experts...")
    response = requests.get(f"{API_BASE}/api/dich_vu/chuyen_gia")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        experts = response.json()
        print(f"Found {len(experts)} experts")
        for expert in experts:
            print(f"  - {expert['name']} ({expert['title']})")
    
    return response.json() if response.status_code == 200 else []

if __name__ == "__main__":
    # Test creation
    new_expert = test_create_expert()
    
    # Test retrieval
    experts = test_get_experts()
    
    # Clean up - delete test expert if created
    if new_expert and 'id' in new_expert:
        print(f"\n\nCleaning up - deleting test expert {new_expert['id']}...")
        delete_response = requests.delete(
            f"{API_BASE}/api/dich_vu/chuyen_gia/{new_expert['id']}"
        )
        print(f"Delete status: {delete_response.status_code}")
