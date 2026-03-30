import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"

def log_test(name, success, info=""):
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {name} {info}")

def final_verification():
    print("=== FINAL SYSTEM VERIFICATION ===")
    
    # 1. Admin Login
    admin_creds = {"email": "admin@hrms.com", "password": "Admin@123"}
    res = requests.post(f"{BASE_URL}/api/auth/login", json=admin_creds)
    if res.status_code != 200:
        log_test("Admin Login", False, res.text)
        return
    admin_token = res.json()['access_token']
    log_test("Admin Login", True)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 2. Add New Employee
    timestamp = datetime.now().strftime("%H%M%S")
    emp_id = f"TEST{timestamp}"
    emp_data = {
        "emp_id": emp_id,
        "email": f"tester{timestamp}@hrms.com",
        "password": "Welcome@123",
        "first_name": "Test",
        "last_name": "Employee",
        "department": "QA",
        "designation": "Engineer",
        "salary_base": 60000
    }
    res = requests.post(f"{BASE_URL}/api/employee/", json=emp_data, headers=headers)
    log_test("Add Employee", res.status_code == 201, res.text)
    
    # 3. Employee Login
    emp_creds = {"email": f"tester{timestamp}@hrms.com", "password": "Welcome@123"}
    res = requests.post(f"{BASE_URL}/api/auth/login", json=emp_creds)
    if res.status_code != 200:
        log_test("Employee Login", False, res.text)
        return
    emp_token = res.json()['access_token']
    emp_headers = {"Authorization": f"Bearer {emp_token}"}
    log_test("Employee Login", True)
    
    # 4. Clock In
    res = requests.post(f"{BASE_URL}/api/attendance/clock-in", json={"location": "Office"}, headers=emp_headers)
    log_test("Clock In", res.status_code in [200, 201], res.text)
    
    # 5. Apply for Leave
    leave_data = {
        "leave_type": "Casual Leave",
        "start_date": "2026-04-01",
        "end_date": "2026-04-02",
        "reason": "Family function"
    }
    res = requests.post(f"{BASE_URL}/api/leave/apply", json=leave_data, headers=emp_headers)
    log_test("Apply Leave", res.status_code == 201, res.text)
    
    # 6. Admin Approve Leave
    res = requests.get(f"{BASE_URL}/api/leave/pending", headers=headers)
    if res.status_code == 200:
        pending = res.json()
        if len(pending) > 0:
            leave_id = pending[0]['id']
            res = requests.post(f"{BASE_URL}/api/leave/action/{leave_id}", json={"status": "Approved"}, headers=headers)
            log_test("Approve Leave", res.status_code == 200, res.text)
        else:
            log_test("Approve Leave", False, "No pending leaves found")
    else:
        log_test("Fetch Pending Leaves", False, res.text)
    
    # 7. Generate Payroll (Admin)
    payroll_data = {"month": 3, "year": 2026}
    res = requests.post(f"{BASE_URL}/api/payroll/generate", json=payroll_data, headers=headers)
    log_test("Generate Payroll", res.status_code == 201, res.text)
    
    # 8. Dashboard Statistics
    res = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers)
    log_test("Dashboard Stats", res.status_code == 200, str(res.json()))

if __name__ == "__main__":
    final_verification()
