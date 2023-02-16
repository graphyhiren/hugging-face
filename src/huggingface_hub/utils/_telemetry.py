from typing import Dict, Optional, Union
from urllib.parse import quote

import requests

from .. import constants
from . import build_hf_headers, hf_raise_for_status
from .. import logging

logger = logging.get_logger(__name__)


def send_telemetry(
    topic: str,
    *,
    library_name: Optional[str] = None,
    library_version: Optional[str] = None,
    user_agent: Union[Dict, str, None] = None,
) -> None:
    """
    Sends telemetry that helps tracking usage of different HF libraries.

    This usage data helps us debug issues and prioritize new features. However, we understand that not everyone wants
    to share additional information, and we respect your privacy. You can disable telemetry collection by setting the
    `HF_HUB_DISABLE_TELEMETRY=1` as environment variable. Telemetry is also disabled in offline mode (i.e. when setting
    `HF_HUB_OFFLINE=1`).

    Args:
        topic (`str`):
            Name of the topic that is monitored. The topic is directly used to build the URL. If you want to monitor
            subtopics, just use "/" separation. Examples: "gradio", "transformers/examples",...
        library_name (`str`, *optional*):
            The name of the library that is making the HTTP request. Will be added to the user-agent header.
        library_version (`str`, *optional*):
            The version of the library that is making the HTTP request. Will be added to the user-agent header.
        user_agent (`str`, `dict`, *optional*):
            The user agent info in the form of a dictionary or a single string. It will be completed with information about the installed packages.

    Example:
    ```py
    >>> from huggingface_hub.utils import send_telemetry

    # Send telemetry without library information
    >>> send_telemetry("ping")

    # Send telemetry to subtopic with library information
    >>> send_telemetry("gradio/local_link", library_name="gradio", library_version="3.22.1")

    # Send telemetry with additional data
    >>> send_telemetry(
    ...     topic="examples",
    ...     library_name="transformers",
    ...     library_version="4.26.0",
    ...     user_agent={"pipeline": "text_classification", "framework": "flax"},
    ... )
    ```
    """
    if constants.HF_HUB_OFFLINE or constants.HF_HUB_DISABLE_TELEMETRY:
        return

    path = "/".join(quote(part) for part in topic.split("/") if len(part) > 0)
    try:
        r = requests.head(
            f"{constants.ENDPOINT}/api/telemetry/{path}",
            headers=build_hf_headers(
                token=False,  # no need to send a token for telemetry
                library_name=library_name,
                library_version=library_version,
                user_agent=user_agent,
            ),
        )
        hf_raise_for_status(r)
    except Exception as e:
        # We don't want to error in case of connection errors of any kind.
        logger.debug(f"Error while sending telemetry: {e}")
