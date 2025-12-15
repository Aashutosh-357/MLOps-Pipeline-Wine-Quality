from locust import HttpUser, task, between

class APIUser(HttpUser):
    # No wait time means we slam the server as fast as possible
    wait_time = between(1, 5) 

    @task
    def predict(self):
        self.client.post("/predict", json={
            "volatile_acidity": 0.7,
            "chlorides": 0.045,
            "density": 0.99,
            "pH": 3.2,
            "alcohol": 10.5
        })