from locust import HttpUser, task, between

class DjangoUser(HttpUser):
    wait_time = between(1, 5)
    # host = "localhost:8000/"
    host = "http://localhost:8000"

    @task(3)
    def load_homepage(self):
        self.client.get("/")

    @task(1)
    def load_api(self):
        self.client.get("/shop/")

    @task(1)
    def submit_form(self):
        self.client.post("/submit/", {"field1": "value1", "field2": "value2"})