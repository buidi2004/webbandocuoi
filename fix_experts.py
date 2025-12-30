import requests

API_BASE = "https://ivie-backend.onrender.com"

def delete_all_experts():
    """Xóa tất cả chuyên gia để fix lỗi database"""
    
    print("Đang lấy danh sách chuyên gia...")
    
    # Thử lấy từng chuyên gia và xóa
    # Vì GET /chuyen_gia bị lỗi, ta thử xóa theo ID
    for expert_id in range(1, 10):  # Thử xóa ID từ 1-10
        try:
            print(f"Đang xóa chuyên gia ID {expert_id}...")
            response = requests.delete(f"{API_BASE}/api/dich_vu/chuyen_gia/{expert_id}", timeout=10)
            
            if response.status_code == 200:
                print(f"  ✅ Đã xóa chuyên gia ID {expert_id}")
            elif response.status_code == 404:
                print(f"  ⏭️  Chuyên gia ID {expert_id} không tồn tại")
            else:
                print(f"  ❌ Lỗi khi xóa ID {expert_id}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception khi xóa ID {expert_id}: {e}")
    
    print("\n✅ Hoàn tất! Thử lại admin panel.")

if __name__ == "__main__":
    delete_all_experts()
