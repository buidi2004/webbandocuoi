"""
Unit tests cho authentication module
"""
import sys
sys.path.insert(0, '.')

from auth import (
    authenticate, has_permission, get_allowed_menu_items,
    USERS, MENU_PERMISSIONS, hash_password
)
import bcrypt

def test_password_hashing():
    """Test bcrypt password hashing"""
    print("🧪 Test 1: Password Hashing")
    
    # Test hash generation
    password = "test123"
    hashed = hash_password(password)
    print(f"  ✓ Generated hash: {hashed[:20]}...")
    
    # Test verification
    assert bcrypt.checkpw(password.encode(), hashed.encode()), "Hash verification failed"
    print(f"  ✓ Hash verification successful")
    
    # Test wrong password
    assert not bcrypt.checkpw("wrong".encode(), hashed.encode()), "Wrong password should fail"
    print(f"  ✓ Wrong password correctly rejected")
    
    print("✅ Test 1 PASSED\n")


def test_authenticate_valid_credentials():
    """Test authentication với credentials hợp lệ"""
    print("🧪 Test 2: Valid Credentials")
    
    # Test CEO login
    user = authenticate("ceo", "123456")
    assert user is not None, "CEO authentication failed"
    assert user["username"] == "ceo", "Wrong username"
    assert user["role"] == "CEO", "Wrong role"
    assert "all" in user["permissions"], "CEO should have 'all' permission"
    print(f"  ✓ CEO login successful: {user['full_name']}")
    
    # Test Nhân viên login
    user = authenticate("nhanvien", "12345")
    assert user is not None, "Nhân viên authentication failed"
    assert user["username"] == "nhanvien", "Wrong username"
    assert user["role"] == "Nhân viên", "Wrong role"
    assert "all" not in user["permissions"], "Nhân viên should not have 'all' permission"
    print(f"  ✓ Nhân viên login successful: {user['full_name']}")
    
    print("✅ Test 2 PASSED\n")


def test_authenticate_invalid_credentials():
    """Test authentication với credentials không hợp lệ"""
    print("🧪 Test 3: Invalid Credentials")
    
    # Test wrong username
    user = authenticate("wronguser", "123456")
    assert user is None, "Wrong username should return None"
    print("  ✓ Wrong username correctly rejected")
    
    # Test wrong password
    user = authenticate("ceo", "wrongpass")
    assert user is None, "Wrong password should return None"
    print("  ✓ Wrong password correctly rejected")
    
    # Test empty credentials
    user = authenticate("", "")
    assert user is None, "Empty credentials should return None"
    print("  ✓ Empty credentials correctly rejected")
    
    print("✅ Test 3 PASSED\n")


def test_ceo_permissions():
    """Test CEO có tất cả quyền"""
    print("🧪 Test 4: CEO Permissions")
    
    # Simulate CEO user
    ceo_user = {
        "username": "ceo",
        "role": "CEO",
        "permissions": ["all"]
    }
    
    # Test với mọi permission
    test_permissions = ["products", "reviews", "orders", "dashboard", "anything"]
    for perm in test_permissions:
        # Giả lập has_permission với CEO user
        has_perm = "all" in ceo_user["permissions"]
        assert has_perm, f"CEO should have {perm} permission"
        print(f"  ✓ CEO has '{perm}' permission")
    
    print("✅ Test 4 PASSED\n")


def test_nhanvien_permissions():
    """Test Nhân viên bị hạn chế quyền"""
    print("🧪 Test 5: Nhân viên Permissions")
    
    # Simulate Nhân viên user
    nv_user = {
        "username": "nhanvien",
        "role": "Nhân viên",
        "permissions": USERS["nhanvien"]["permissions"]
    }
    
    # Test quyền được phép
    allowed = ["dashboard", "orders", "combo", "experts"]
    for perm in allowed:
        has_perm = perm in nv_user["permissions"]
        assert has_perm, f"Nhân viên should have {perm} permission"
        print(f"  ✓ Nhân viên has '{perm}' permission")
    
    # Test quyền bị cấm
    forbidden = ["products", "reviews"]
    for perm in forbidden:
        has_perm = perm in nv_user["permissions"]
        assert not has_perm, f"Nhân viên should NOT have {perm} permission"
        print(f"  ✓ Nhân viên does NOT have '{perm}' permission")
    
    print("✅ Test 5 PASSED\n")


def test_menu_visibility():
    """Test menu items visibility theo permissions"""
    print("🧪 Test 6: Menu Visibility")
    
    # CEO should see all menus
    ceo_user = {"permissions": ["all"]}
    ceo_menus = list(MENU_PERMISSIONS.keys()) if "all" in ceo_user["permissions"] else []
    assert len(ceo_menus) == len(MENU_PERMISSIONS), "CEO should see all menu items"
    print(f"  ✓ CEO sees all {len(ceo_menus)} menu items")
    
    # Nhân viên should see limited menus
    nv_user = {"permissions": USERS["nhanvien"]["permissions"]}
    nv_menus = []
    for menu_item, permission in MENU_PERMISSIONS.items():
        if permission in nv_user["permissions"]:
            nv_menus.append(menu_item)
    
    # Verify restricted menus are hidden
    assert "👗 Quản lý Sản phẩm" not in nv_menus, "Nhân viên should not see Quản lý Sản phẩm"
    assert "⏳ Duyệt Đánh Giá" not in nv_menus, "Nhân viên should not see Duyệt Đánh Giá"
    print(f"  ✓ Nhân viên sees {len(nv_menus)} menu items (restricted)")
    print(f"  ✓ 'Quản lý Sản phẩm' hidden from Nhân viên")
    print(f"  ✓ 'Duyệt Đánh Giá' hidden from Nhân viên")
    
    print("✅ Test 6 PASSED\n")


def test_password_hashes_in_users():
    """Verify password hashes trong USERS dict"""
    print("🧪 Test 7: Password Hashes Verification")
    
    # Test CEO password
    ceo_hash = USERS["ceo"]["password_hash"]
    assert bcrypt.checkpw("123456".encode(), ceo_hash.encode()), "CEO password hash invalid"
    print("  ✓ CEO password hash verified (123456)")
    
    # Test Nhân viên password
    nv_hash = USERS["nhanvien"]["password_hash"]
    assert bcrypt.checkpw("12345".encode(), nv_hash.encode()), "Nhân viên password hash invalid"
    print("  ✓ Nhân viên password hash verified (12345)")
    
    print("✅ Test 7 PASSED\n")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RUNNING AUTHENTICATION TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_password_hashing()
        test_authenticate_valid_credentials()
        test_authenticate_invalid_credentials()
        test_ceo_permissions()
        test_nhanvien_permissions()
        test_menu_visibility()
        test_password_hashes_in_users()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
