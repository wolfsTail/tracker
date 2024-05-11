import string, random
from dataclasses import dataclass

from schemas import UserLoginSchema
from repository import UserRepository


@dataclass
class UserService:
    user_repo = UserRepository

    async def create_user(
            self, username: str, password: str,
            ) -> UserLoginSchema:
        access_token = self._dummy_generate_access_token()
        user = await self.user_repo.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)
    
    @staticmethod
    def _dummy_generate_access_token(n=19) -> str:
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
