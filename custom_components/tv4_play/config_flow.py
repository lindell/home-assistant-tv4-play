from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
)
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from typing import Any, Dict, Optional
from collections.abc import Mapping

from custom_components.tv4_play.video_url_fetch.video_fetch import fetch_access_token

from .const import CONF_ENTRY_NAME, DOMAIN, CONF_REFRESH_TOKEN

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTRY_NAME, default="TV4 Play"): cv.string,
        vol.Required(CONF_REFRESH_TOKEN): cv.string,
    }
)

REAUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_REFRESH_TOKEN): cv.string,
    }
)


class TV4PlayConfigFlow(ConfigFlow, domain=DOMAIN):
    """TV4 Play config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                refresh_token = user_input[CONF_REFRESH_TOKEN]
                await fetch_access_token(refresh_token)
                return self.async_create_entry(
                    title=user_input[CONF_ENTRY_NAME],
                    data={
                        "refresh_token": refresh_token,
                    },
                )
            except Exception:
                errors["base"] = "auth"

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Dialog that informs the user that reauth is required."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=REAUTH_SCHEMA,
            )

        try:
            refresh_token = user_input[CONF_REFRESH_TOKEN]
            await fetch_access_token(refresh_token)
        except Exception:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=REAUTH_SCHEMA,
                errors={"base": "auth"},
            )

        return self.async_update_reload_and_abort(
            self._get_reconfigure_entry(),
            data_updates={
                "refresh_token": refresh_token,
            },
        )
