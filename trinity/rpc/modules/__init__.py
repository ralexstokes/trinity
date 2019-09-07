from typing import (
    Iterable,
)

from lahja import EndpointAPI

from eth_utils import (
    to_tuple,
)

from trinity.chains.base import AsyncChainAPI

from .main import (  # noqa: F401
    BaseRPCModule,
    ChainReplacementEvent,
    Eth1ChainRPCModule,
    ChainBasedRPCModule,
)

from .admin import Admin
from .eth import Eth  # noqa: F401
from .evm import EVM  # noqa: F401
from .net import Net  # noqa: F401
from .web3 import Web3  # noqa: F401


@to_tuple
def initialize_eth1_modules(chain: AsyncChainAPI,
                            event_bus: EndpointAPI) -> Iterable[BaseRPCModule]:
    yield Eth(chain, event_bus)
    yield EVM(chain, event_bus)
    yield Net(event_bus)
    yield Web3()
    yield Admin(event_bus)
