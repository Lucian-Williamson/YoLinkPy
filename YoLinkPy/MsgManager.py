from typing import Any

from yolink.device import YoLinkDevice
from yolink.message_listener import MessageListener


# Example implementation of MessageListener
class MsgListener(MessageListener):
    """Custom message listener implementation."""

    def on_message(self, device: YoLinkDevice, msg_data: dict[str, Any]) -> None:
        """Handle received message from device."""
        print(f"Received message from {device}: {msg_data}")
        # Perform actions based on the received message ...
