from typing import Optional

from pydantic import BaseModel


class RequestCreate(BaseModel):
    user_id: int
    team_id: Optional[int]
