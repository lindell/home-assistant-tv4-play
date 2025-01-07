import datetime
from homeassistant import config_entries, core
from homeassistant.helpers.entity import Entity
import jwt
from stringcase import snakecase

from .const import DOMAIN, CONF_REFRESH_TOKEN


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    # Update our config to include new repos and remove those that have been removed.
    if config_entry.options:
        config.update(config_entry.options)

    sensor = TV4PlayToken(config_entry.title, config.get(CONF_REFRESH_TOKEN))
    async_add_entities([sensor], update_before_add=True)


class TV4PlayToken(Entity):
    """Representation of a GitHub Repo sensor."""

    def __init__(self, entry_name: str, encoded_jwt: str):
        super().__init__()
        data = jwt.decode(encoded_jwt, options={"verify_signature": False})
        expiry = datetime.datetime.fromtimestamp(data["exp"])
        self._state = expiry
        self._available = True
        self._unique_id = f"{snakecase(entry_name)}_token_expiry"
        self.entry_name = entry_name

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return f"{self.entry_name} Token Expiry"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    @property
    def state(self) -> datetime.datetime | None:
        return self._state
