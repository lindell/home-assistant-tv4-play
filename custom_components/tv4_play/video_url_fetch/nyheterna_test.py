import os
from weakref import ref

import pytest
from video_fetch import fetch_access_token, get_suggested_episode, get_video_url

# The X-Forwarded-For needs to be set so that it isn't set to something else
# since the cdn server rejects requests from known proxies
headers = {"X-Forwarded-For": "195.198.201.208"}


@pytest.mark.asyncio
async def test_nyheterna():
    refresh_token = os.environ.get("TV4_REFRESH_TOKEN")
    if refresh_token is None:
        raise Exception(
            "No refresh token found in environment variable TV4_REFRESH_TOKEN"
        )

    access_token = await fetch_access_token(refresh_token)

    episode = await get_suggested_episode(access_token, "2f9d93c74848c53db133")
    assert episode.image_url.startswith("http")

    url = await get_video_url(access_token, episode.id, headers=headers)
    assert isinstance(url, str)
    assert url.startswith("http")
