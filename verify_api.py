import requests

BASE_URL = "http://localhost:5000"

def test_system():
    print(f"Testing system at {BASE_URL}...")
    
    # 1. Login
    login_data = {
        "email": "admin@hrms.com",
        "password": "Admin@123"
    }
    res = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if res.status_code != 200:
        print(f"Login failed: {res.status_code} {res.text}")
        return
    
    token = res.json().get('access_token')
    print(f"Login successful! Token: {token[:20]}...")
    
    # 2. Check Stats
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers)
    print(f"Stats Response: {res.status_code}")
    print(f"Stats Body: {res.text}")
    if res.status_code == 200:
        print(f"Stats Data: {res.json()}")
        
    # 3. Check Employees
    res = requests.get(f"{BASE_URL}/api/employee/", headers=headers)
    print(f"Employees Response: {res.status_code}")
    if res.status_code == 200:
        employees = res.json()
        print(f"Found {len(employees)} employees.")
    else:
        print(f"Employees Error: {res.text}")

if __name__ == "__main__":
    test_system()
