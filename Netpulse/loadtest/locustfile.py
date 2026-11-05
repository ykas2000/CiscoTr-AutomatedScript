from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_items(self):
        self.client.get(
        "/devices",
        headers={"Authorization": "Bearer test-token-123"}
    )
