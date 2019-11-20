import pytest
from video_fetch import get_suggested_episode, get_video_url

# The X-Forwarded-For needs to be set so that it isn't set to something else
# since the cdn server rejects requests from known proxies
headers = {'X-Forwarded-For': '127.0.0.1'}


def test_not_started_stream():
    video_asset = get_suggested_episode('nyhetsmorgon')

    assert isinstance(video_asset['id'], int)
    assert isinstance(video_asset['live'], bool)
    assert isinstance(video_asset['startOver'], bool)

    with pytest.raises(Exception, match=r".* stream_not_started.*"):
        get_video_url(video_asset, headers=headers)


def test_started_stream():
    video_asset = get_suggested_episode('nyheterna')

    assert isinstance(video_asset['id'], int)
    assert isinstance(video_asset['live'], bool)
    assert isinstance(video_asset['startOver'], bool)

    url = get_video_url(video_asset, headers=headers)
    assert isinstance(url, str)
    assert url.startswith('http')
