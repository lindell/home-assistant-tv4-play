import logging
from homeassistant.helpers import config_validation as cv, selector
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.const import Platform


from .video_url_fetch.video_fetch import (
    fetch_access_token,
    get_video_url,
    get_suggested_episode,
)
from .const import DOMAIN

DEPENDENCIES = ["media_player"]

CONF_ENTITY_ID = "entity_id"
CONF_PROGRAM_NAME = "program_name"
CONF_CONFIG_ENTRY = "config_entry"

SERVICE_PLAY_SUGGESTED = "play_suggested"
SERVICE_PLAY_SUGGESTED_SCHEMA = vol.Schema(
    {
        CONF_ENTITY_ID: cv.entity_ids,
        CONF_CONFIG_ENTRY: selector.ConfigEntrySelector(
            {
                "integration": DOMAIN,
            }
        ),
        CONF_PROGRAM_NAME: str,
    }
)

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})

    async def play_suggested(service):
        """Play a tv4 play video"""

        entity_id = service.data.get(CONF_ENTITY_ID)
        program_name = service.data.get(CONF_PROGRAM_NAME)
        config_entry_id = service.data.get(CONF_CONFIG_ENTRY)

        config_entry = hass.data[DOMAIN][config_entry_id]
        refresh_token: str = config_entry["refresh_token"]

        access_token = await fetch_access_token(refresh_token)

        episode = await get_suggested_episode(access_token, program_name)

        _LOGGER.debug("Suggested episode: %s", episode.id)

        video_url = await get_video_url(access_token, episode.id)

        service_data = {
            "entity_id": entity_id,
            "media_content_id": video_url,
            "media_content_type": "video",
            "extra": {
                "title": episode.title,
                "thumb": episode.image_url,
            },
        }

        await hass.services.async_call("media_player", "play_media", service_data)

    hass.services.async_register(
        DOMAIN, SERVICE_PLAY_SUGGESTED, play_suggested, SERVICE_PLAY_SUGGESTED_SCHEMA
    )

    return True


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass_data = dict(entry.data)
    hass.data[DOMAIN][entry.entry_id] = hass_data

    # Forward the setup to the sensor platform.
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True
