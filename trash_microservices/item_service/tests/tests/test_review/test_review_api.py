from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from item_service.models.models import Item, Review, Category
from tests.tests.test_review.manager import ReviewRequestManager
from tests.tests.conftest import headers
from tests.tests.test_review.setup_teardown import setup, teardown

@pytest.mark.asyncio(scope='module')
async def test_add_correct_review(client: AsyncClient, user_id: int, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    item_id, category_id = await setup(client, user_id)

    review_1 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'rot ebal',
        'rating': 4.7
    }

    review_2 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'xyeta',
        'rating': 5.0
    }

    review_3 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'eblo',
        'rating': 1.2
    }

    review_manager = ReviewRequestManager(client, Review)

    await review_manager.add(review_1)
    await review_manager.add(review_2)
    await review_manager.add(review_3)

    all_reviews = await review_manager.get_all_serialized()

    logger.info(all_reviews)

    assert all_reviews[0]['text'] == review_1['text']
    assert all_reviews[1]['text'] == review_2['text']
    assert all_reviews[2]['text'] == review_3['text']

    review_ids = [review['id'] for review in all_reviews]

    await teardown(client, item_id, category_id, review_ids)

@pytest.mark.asyncio(scope='module')
async def test_get_reviews_by_item_and_user_id(client: AsyncClient, user_id: int, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    item_id, category_id = await setup(client, user_id)

    review_1 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'rot ebal',
        'rating': 4.7
    }

    review_2 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'xyeta',
        'rating': 5.0
    }

    review_3 = {
        'reviewer_id': user_id,
        'item_id': item_id,
        'text': 'eblo',
        'rating': 1.2
    }

    review_manager = ReviewRequestManager(client, Review)

    await review_manager.add(review_1)
    await review_manager.add(review_2)
    await review_manager.add(review_3)

    all_reviews = await review_manager.get_all_serialized()
    all_reviews_item = await review_manager.get_by_item_id_serialized(item_id)
    all_reviews_user = await review_manager.get_by_user_id_serialized(user_id)

    assert all_reviews == all_reviews_item == all_reviews_user

    review_ids = [review['id'] for review in all_reviews]

    await teardown(client, item_id, category_id, review_ids)