from requests import get
from requests import post

# Get the CDN video url
def get_video_url(video_asset):
    url = 'https://playback-api.b17g.net/media/{}?service=tv4&device=browser&protocol=hls%2Cdash&drm=widevine&is_live={}&has_startover={}'.format(
        video_asset['id'],
        video_asset['live'],
        video_asset['startOver'],
    )

    data = get(url).json()
    if 'errorCode' in data:
        raise Exception("Could not fetch the CDN data: {}".format(data['errorCode']))
    video_url = data['playbackItem']['manifestUrl']

    return video_url

# Get information about the sugested episode based on the program name
def get_suggested_episode(program_id):
    query = """
        query($name: String) {
            program(nid: $name) {
                suggestedEpisode {
                    videoAsset {
                        id
                        live
                        startOver
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

    data = post('https://tv4-graphql-web.b17g.net/graphql', json=query_data).json()
    video_asset = data['data']['program']['suggestedEpisode']['videoAsset']

    return video_asset
