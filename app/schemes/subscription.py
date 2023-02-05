from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    team_name: str
    user_id: int
