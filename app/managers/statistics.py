from sqlalchemy import func, select

from app.managers.base import BaseAdapter
from app.orm.models import Request, Subscription

LABEL_IDX = 0
COUNT_IDX = 1


class StatisticsManager(BaseAdapter):
    MIN_REQUEST_COUNT_FOR_REGULAR_USER = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get(self) -> str:
        requests = select([
            func.concat(
                func.text('Requests - '),
                func.count(Request.id)
            ),
            func.concat(
                func.text('Unique users - '),
                func.count(func.distinct(Request.user_id))
            )
        ]).select_from(
            Request
        )
        requests_regular = select([
            func.concat(
                func.text('Regular users - '),
                func.count(func.text('*')),
                func.text(
                    ' (more than ' + str(self.MIN_REQUEST_COUNT_FOR_REGULAR_USER) + ' requests)'
                )
            ),
            func.text('')
        ]).select_from(
            select([
                Request.user_id
            ]).select_from(
                Request
            ).group_by(
                Request.user_id
            ).having(
                func.count(func.text('*')) > self.MIN_REQUEST_COUNT_FOR_REGULAR_USER
            ).alias('tmp')
        )
        subscriptions = select([
            func.concat(
                func.text('Subscriptions - '),
                func.count(Subscription.id),
            ),
            func.concat(
                func.text('Unique users - '),
                func.count(func.distinct(Subscription.user_id)),
            )
        ]).select_from(
            Subscription
        )
        data = await subscriptions.union_all(requests.union_all(requests_regular)).gino.all()
        return '\n'.join([record[LABEL_IDX] + '. ' + record[COUNT_IDX] for record in data])
