import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .video_url_fetch.video_fetch import get_video_url, get_suggested_episode

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

    hass.services.async_register(
        DOMAIN, SERVICE_PLAY_SUGGESTED, play_suggested, SERVICE_PLAY_SUGGESTED_SCHEMA)

    return True
