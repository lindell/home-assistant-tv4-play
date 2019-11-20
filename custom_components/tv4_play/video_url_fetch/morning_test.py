import pytest
from video_fetch import get_suggested_episode, get_video_url


def test_not_started_stream():
    video_asset = get_suggested_episode('efter-fem')

    assert isinstance(video_asset['id'], int)
    assert isinstance(video_asset['live'], bool)
    assert isinstance(video_asset['startOver'], bool)

    with pytest.raises(Exception, match=r".* stream_not_started.*"):
        get_video_url(video_asset)


def test_started_stream():
    video_asset = get_suggested_episode('nyhetsmorgon')

    assert isinstance(video_asset['id'], int)
    assert isinstance(video_asset['live'], bool)
    assert isinstance(video_asset['startOver'], bool)

    url = get_video_url(video_asset)
    assert isinstance(url, str)
    assert url.startswith('http')
