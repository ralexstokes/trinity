import logging
from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
    Union,
)
from ruamel.yaml import (
    YAML,
)

from ssz.tools import (
    from_formatted_dict,
)

from eth2.beacon.types.states import (
    BeaconState,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if TYPE_CHECKING:
    from ruamel.yaml.compat import StreamTextType  # noqa: F401


class KeyFileNotFound(FileNotFoundError):
    pass


def extract_genesis_state_from_stream(stream: Union[Path, "StreamTextType"]) -> BeaconState:
    yaml = YAML(typ="unsafe")
    genesis_json = yaml.load(stream)
    state = from_formatted_dict(genesis_json, BeaconState)
    return state
