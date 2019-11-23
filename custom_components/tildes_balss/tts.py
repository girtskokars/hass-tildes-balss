"""Support for the Tildes Balss speech service."""
import asyncio
import logging

import aiohttp
from aiohttp.hdrs import REFERER, USER_AGENT
import async_timeout
import voluptuous as vol

from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


SUPPORTED_LANGUAGES = ["lv"]
DEFAULT_LANGUAGE = "lv"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANGUAGE): vol.In(SUPPORTED_LANGUAGES)
    }
)


async def async_get_engine(hass, config, discovery_info=None):
    """Set up Tildes Balss speech component."""
    return TildesBalssProvider(hass, config[CONF_LANG])


class TildesBalssProvider(Provider):
    """The Tildes Balss speech API provider."""

    def __init__(self, hass, lang):
        """Init Tildes Balss TTS service."""
        self.hass = hass
        self._lang = lang
        self.name = "Tildes Balss"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORTED_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS from runa.tilde.lv."""
        websession = async_get_clientsession(self.hass)

        params = {
            "text": message
        }

        headers = {
            REFERER: "https://www.tilde.lv/tildes-balss",
            USER_AGENT: (
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36"
            ),
        }

        try:
            with async_timeout.timeout(10):
                request = await websession.get(
                    "https://runa.tilde.lv/client/say/", params=params, headers=headers
                )

                if request.status != 200:
                    _LOGGER.error(
                        "Error %d on load URL %s", request.status, request.url
                    )
                    return None, None
                data = await request.read()

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for Tildes Balss speech")
            return None, None

        return "mp3", data