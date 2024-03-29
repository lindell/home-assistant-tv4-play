from requests import get
from requests import post


def get_video_url(video_asset, headers=None):
    "Get the CDN video url"

    config = get("https://html-player-v2.b17g.net/config?service=tv4", headers=headers).json()
    playback_endpoint = config["PLAYBACK_ENDPOINT"]

    url = '{}/play/{}?service=tv4&device=browser&protocol=hls%2Cdash&drm=widevine&is_live={}&has_startover={}'.format(
        playback_endpoint,
        video_asset['id'],
        video_asset['live'],
        video_asset['startOver'],
    )

    data = get(url, headers=headers).json()
    if 'errorCode' in data:
        raise Exception(
            "Could not fetch the CDN data: {}".format(data['errorCode'])
        )
    video_url = data['playbackItem']['manifestUrl']

    return video_url


def get_suggested_episode(program_id):
    "Get information about the suggested episode based on the program name"
    query = """
        query($name: String) {
            program(nid: $name) {
                suggestedEpisode {
                    videoAsset {
                        id
                        live
                        startOver
                        title
                        image2 {
                            url
                        }
                    }
                }
            }
        }
    """

    query_data = {
        'query': query,
        'variables': {
            'name': program_id,
        },
    }

    data = post('https://graphql.tv4play.se/graphql',
                json=query_data).json()
    video_asset = data['data']['program']['suggestedEpisode']['videoAsset']

    return video_asset
