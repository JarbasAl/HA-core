"""OpenVoiceOS notification platform."""
from __future__ import annotations

import logging
from ovos_bus_client import MessageBusClient, Message  # pylint: disable=import-error

from homeassistant.components.notify import BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)


def get_service(
        hass: HomeAssistant,
        config: ConfigType,
        discovery_info: DiscoveryInfoType | None = None,
) -> OVOSNotificationService:
    """Get the OVOS notification service."""
    return OVOSNotificationService(hass.data["ovos"])


class OVOSNotificationService(BaseNotificationService):
    """The OVOS Notification Service."""

    def __init__(self, mycroft_ip, mycroft_port=8181):
        """Initialize the service."""
        self.mycroft_ip = mycroft_ip
        self.mycroft_port = mycroft_port

    def send_message(self, message="", **kwargs):
        """Send a message to speak on ovos instance."""
        try:
            client = MessageBusClient(host=self.mycroft_ip, port=self.mycroft_port)
            client.run_in_thread()
            client.connected_event.wait()
            client.emit(Message("speak", {"utterance": message}))
            client.close()
        except:
            _LOGGER.log("Could not reach this instance of OpenVoiceOS")
