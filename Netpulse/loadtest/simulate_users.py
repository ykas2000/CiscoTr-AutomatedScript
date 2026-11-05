from locust import HttpUser, task, between

class BrowseItemsUser(HttpUser):
    # Simulated users wait 1 to 3 seconds between tasks to mimic realistic behavior
    wait_time = between(1, 3)

    @task
    def get_items(self):
        """Simulates a user requesting the /items endpoint."""
        print("\n--- Task: Fetching Items (GET) ---")
        
        # Send HTTP GET request
        response = self.client.get("/items")
        
        print(f"📥 Received Status Code: {response.status_code}")
        
        # Add conditional checks and prints for debugging during test runs
        if response.status_code == 200:
            print(f"✅ Success! Response data: {response.text[:100]}...") # Print first 100 chars
        else:
            print(f"❌ Failed with status code: {response.status_code}")