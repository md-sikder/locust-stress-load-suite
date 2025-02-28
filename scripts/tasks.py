# tasks.py
from locust import TaskSet, task

class UserBehavior(TaskSet):
    @task(1)
    def post_user(self):
        response = self.client.post("/api/users", json={"name": "morpheus", "job": "leader"})
        print(response.text)

    @task(1)
    def put_user(self):
        response = self.client.put("/api/users/2", json={"name": "morpheus", "job": "zion resident"})
        print(response.text)

    @task(1)
    def delete_user(self):
        response = self.client.delete("/api/users/2")
        print(response.text)
