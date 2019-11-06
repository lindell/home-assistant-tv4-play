import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from requests import get
from requests import post

DOMAIN = "tv4_play"

DEPENDENCIES = ['media_player']

CONF_ENTITY_ID = 'entity_id'
CONF_PROGRAM_NAME = 'program_name'

SERVICE_PLAY_SUGGESTED = 'play_suggested'
SERVICE_PLAY_SUGGESTED_SCHEMA = vol.Schema({
    CONF_ENTITY_ID: cv.entity_ids,
    CONF_PROGRAM_NAME: str,
})

_LOGGER = logging.getLogger(__name__)

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

async def async_setup(hass, config):

    async def play_suggested(service):
        """Play a tv4 play video"""

        entity_id = service.data.get(CONF_ENTITY_ID)
        program_name = service.data.get(CONF_PROGRAM_NAME)

        video_url = get_video_url(get_suggested_episode(program_name))

        service_data = {
            'entity_id': entity_id,
            'media_content_id': video_url,
            'media_content_type': 'video'
        }

        await hass.services.async_call('media_player', 'play_media', service_data)

    hass.services.async_register(DOMAIN, SERVICE_PLAY_SUGGESTED, play_suggested, SERVICE_PLAY_SUGGESTED_SCHEMA)

    return True
