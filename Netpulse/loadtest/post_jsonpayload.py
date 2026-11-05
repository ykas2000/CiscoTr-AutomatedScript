from locust import HttpUser, task, between

class LoginUser(HttpUser):
    # Users wait 2 to 5 seconds before attempting another action
    wait_time = between(2, 5)

    @task
    def login_user(self):
        """Simulates a user posting login credentials[cite: 3]."""
        payload = {
            "username": "network_admin",
            "password": "secure_password_123"
        }
        
        print("\n--- Task: User Login (POST) ---")
        print(f"📤 Sending Payload: {payload}")
        
        # Send HTTP POST request with JSON data
        response = self.client.post("/login", json=payload)
        
        print(f"📥 Received Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful! Token or session established.")
        else:
            print(f"⚠️ Login failed or rejected. Code: {response.status_code}")