from dataclasses import dataclass

import pytest


@dataclass
class FakeUserRepo:

    def __init__(self):
        self.users = []

    def add(self, user):
        self.users.append(user)

    def get(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_all(self):
        return self.users
    
    def delete(self, user_id):
        for user in self.users:
            if user.id == user_id:
                self.users.remove(user)
                return user
        return None


@pytest.fixtures
def user_repository():
    return FakeUserRepo()
