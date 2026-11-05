from locust import HttpUser, task, between

class MixedWorkflowUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def view_items(self):
        """High-frequency task: Browsing items (Weight: 3)[cite: 3]."""
        print("\n--- Executing Task: View Items (Weight: 3) ---")
        response = self.client.get("/items")
        print(f"📦 /items Status: {response.status_code}")

    @task(1)
    def view_orders(self):
        """Low-frequency task: Checking orders (Weight: 1)[cite: 3]."""
        print("\n--- Executing Task: View Orders (Weight: 1) ---")
        response = self.client.get("/orders")
        print(f"📋 /orders Status: {response.status_code}")