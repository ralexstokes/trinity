from dataclasses import dataclass

from eth_utils import decode_hex

from eth2.constants import GWEI_PER_ETH
from eth2.typing import Epoch, Gwei, Second, Slot


@dataclass
class Eth2Config:
    MAX_COMMITTEES_PER_SLOT: int
    TARGET_COMMITTEE_SIZE: int
    MAX_VALIDATORS_PER_COMMITTEE: int
    MIN_PER_EPOCH_CHURN_LIMIT: int
    CHURN_LIMIT_QUOTIENT: int
    SHUFFLE_ROUND_COUNT: int
    # Genesis
    MIN_GENESIS_ACTIVE_VALIDATOR_COUNT: int
    MIN_GENESIS_TIME: int
    # Gwei values,
    MIN_DEPOSIT_AMOUNT: Gwei
    MAX_EFFECTIVE_BALANCE: Gwei
    EJECTION_BALANCE: Gwei
    EFFECTIVE_BALANCE_INCREMENT: Gwei
    # Initial values
    GENESIS_SLOT: Slot
    GENESIS_EPOCH: Epoch
    BLS_WITHDRAWAL_PREFIX: int
    # Time parameters
    SECONDS_PER_SLOT: Second
    MIN_ATTESTATION_INCLUSION_DELAY: int
    SLOTS_PER_EPOCH: int
    MIN_SEED_LOOKAHEAD: int
    MAX_SEED_LOOKAHEAD: int
    SLOTS_PER_ETH1_VOTING_PERIOD: int
    SLOTS_PER_HISTORICAL_ROOT: int
    MIN_VALIDATOR_WITHDRAWABILITY_DELAY: int
    PERSISTENT_COMMITTEE_PERIOD: int
    MIN_EPOCHS_TO_INACTIVITY_PENALTY: int
    # State list lengths
    EPOCHS_PER_HISTORICAL_VECTOR: int
    EPOCHS_PER_SLASHINGS_VECTOR: int
    HISTORICAL_ROOTS_LIMIT: int
    VALIDATOR_REGISTRY_LIMIT: int
    # Rewards and penalties
    BASE_REWARD_FACTOR: int
    WHISTLEBLOWER_REWARD_QUOTIENT: int
    PROPOSER_REWARD_QUOTIENT: int
    INACTIVITY_PENALTY_QUOTIENT: int
    MIN_SLASHING_PENALTY_QUOTIENT: int
    # Max operations per block
    MAX_PROPOSER_SLASHINGS: int
    MAX_ATTESTER_SLASHINGS: int
    MAX_ATTESTATIONS: int
    MAX_DEPOSITS: int
    MAX_VOLUNTARY_EXITS: int
    # Fork choice
    SAFE_SLOTS_TO_UPDATE_JUSTIFIED: int
    # Deposit contract
    DEPOSIT_CONTRACT_ADDRESS: bytes


class CommitteeConfig:
    def __init__(self, config: Eth2Config):
        # Basic
        self.GENESIS_SLOT = config.GENESIS_SLOT
        self.GENESIS_EPOCH = config.GENESIS_EPOCH
        self.MAX_COMMITTEES_PER_SLOT = config.MAX_COMMITTEES_PER_SLOT
        self.SLOTS_PER_EPOCH = config.SLOTS_PER_EPOCH
        self.TARGET_COMMITTEE_SIZE = config.TARGET_COMMITTEE_SIZE
        self.SHUFFLE_ROUND_COUNT = config.SHUFFLE_ROUND_COUNT

        # For seed
        self.MIN_SEED_LOOKAHEAD = config.MIN_SEED_LOOKAHEAD
        self.MAX_SEED_LOOKAHEAD = config.MAX_SEED_LOOKAHEAD
        self.EPOCHS_PER_HISTORICAL_VECTOR = config.EPOCHS_PER_HISTORICAL_VECTOR
        self.EPOCHS_PER_HISTORICAL_VECTOR = config.EPOCHS_PER_HISTORICAL_VECTOR

        self.MAX_EFFECTIVE_BALANCE = config.MAX_EFFECTIVE_BALANCE
        self.EFFECTIVE_BALANCE_INCREMENT = config.EFFECTIVE_BALANCE_INCREMENT


class Eth2GenesisConfig:
    """
    Genesis parameters that might lives in
    a state or a state machine config
    but is assumed unlikely to change between forks.
    Pass this to the chains, chain_db, or other objects that need them.
    """

    def __init__(self, config: Eth2Config) -> None:
        self.GENESIS_SLOT = config.GENESIS_SLOT
        self.GENESIS_EPOCH = config.GENESIS_EPOCH
        self.SECONDS_PER_SLOT = config.SECONDS_PER_SLOT
        self.SLOTS_PER_EPOCH = config.SLOTS_PER_EPOCH


MINIMAL_SERENITY_CONFIG = Eth2Config(
    # Misc
    MAX_COMMITTEES_PER_SLOT=4,
    TARGET_COMMITTEE_SIZE=4,
    MAX_VALIDATORS_PER_COMMITTEE=2048,
    MIN_PER_EPOCH_CHURN_LIMIT=4,
    CHURN_LIMIT_QUOTIENT=65536,
    SHUFFLE_ROUND_COUNT=10,
    # Genesis
    MIN_GENESIS_ACTIVE_VALIDATOR_COUNT=64,
    MIN_GENESIS_TIME=1578009600,  # (= Jan 3, 2020)
    # Gwei values
    MIN_DEPOSIT_AMOUNT=Gwei(2 ** 0 * GWEI_PER_ETH),  # (= 1,000,000,000) Gwei
    MAX_EFFECTIVE_BALANCE=Gwei(2 ** 5 * GWEI_PER_ETH),  # (= 32,000,000,00) Gwei
    EJECTION_BALANCE=Gwei(2 ** 4 * GWEI_PER_ETH),  # (= 16,000,000,000) Gwei
    EFFECTIVE_BALANCE_INCREMENT=Gwei(2 ** 0 * GWEI_PER_ETH),  # (= 1,000,000,000) Gwei
    # Initial values
    GENESIS_SLOT=Slot(0),
    GENESIS_EPOCH=Epoch(0),
    BLS_WITHDRAWAL_PREFIX=0,
    # Time parameters
    SECONDS_PER_SLOT=Second(6),  # seconds
    MIN_ATTESTATION_INCLUSION_DELAY=2 ** 0,  # (= 1) slots
    SLOTS_PER_EPOCH=8,
    MIN_SEED_LOOKAHEAD=2 ** 0,  # (= 1) epochs
    MAX_SEED_LOOKAHEAD=2 ** 2,  # (= 4) epochs
    SLOTS_PER_ETH1_VOTING_PERIOD=16,
    SLOTS_PER_HISTORICAL_ROOT=64,
    MIN_VALIDATOR_WITHDRAWABILITY_DELAY=256,
    PERSISTENT_COMMITTEE_PERIOD=2 ** 7,  # (= 128) epochs
    MIN_EPOCHS_TO_INACTIVITY_PENALTY=4,
    # State list lengths
    EPOCHS_PER_HISTORICAL_VECTOR=64,
    EPOCHS_PER_SLASHINGS_VECTOR=64,
    HISTORICAL_ROOTS_LIMIT=2 ** 24,
    VALIDATOR_REGISTRY_LIMIT=2 ** 40,
    # Reward and penalty quotients
    BASE_REWARD_FACTOR=2 ** 6,  # (= 64)
    WHISTLEBLOWER_REWARD_QUOTIENT=2 ** 9,  # (= 512)
    PROPOSER_REWARD_QUOTIENT=2 ** 3,
    INACTIVITY_PENALTY_QUOTIENT=2 ** 25,  # (= 33,554,432)
    MIN_SLASHING_PENALTY_QUOTIENT=2 ** 5,
    # Max operations per block
    MAX_PROPOSER_SLASHINGS=2 ** 4,  # (= 16)
    MAX_ATTESTER_SLASHINGS=2 ** 0,  # (= 1)
    MAX_ATTESTATIONS=2 ** 7,  # (= 128)
    MAX_DEPOSITS=2 ** 4,  # (= 16)
    MAX_VOLUNTARY_EXITS=2 ** 4,  # (= 16)
    # Fork choice
    SAFE_SLOTS_TO_UPDATE_JUSTIFIED=2,
    # Deposit contract
    DEPOSIT_CONTRACT_ADDRESS=decode_hex(
        "0x1234567890123456789012345678901234567890"
    ),  # TBD
)

SERENITY_CONFIG = Eth2Config(
    # Misc
    MAX_COMMITTEES_PER_SLOT=2 ** 6,  # (= 64) committees
    TARGET_COMMITTEE_SIZE=2 ** 7,  # (= 128) validators
    MAX_VALIDATORS_PER_COMMITTEE=2 ** 11,  # (= 2,048) validators
    MIN_PER_EPOCH_CHURN_LIMIT=2 ** 2,
    CHURN_LIMIT_QUOTIENT=2 ** 16,
    SHUFFLE_ROUND_COUNT=90,
    # Genesis
    MIN_GENESIS_ACTIVE_VALIDATOR_COUNT=2 ** 14,
    MIN_GENESIS_TIME=1578009600,  # (= Jan 3, 2020)
    # Gwei values
    MIN_DEPOSIT_AMOUNT=Gwei(2 ** 0 * GWEI_PER_ETH),  # (= 1,000,000,000) Gwei
    MAX_EFFECTIVE_BALANCE=Gwei(2 ** 5 * GWEI_PER_ETH),  # (= 32,000,000,00) Gwei
    EJECTION_BALANCE=Gwei(2 ** 4 * GWEI_PER_ETH),  # (= 16,000,000,000) Gwei
    EFFECTIVE_BALANCE_INCREMENT=Gwei(2 ** 0 * GWEI_PER_ETH),  # (= 1,000,000,000) Gwei
    # Initial values
    GENESIS_SLOT=Slot(0),
    GENESIS_EPOCH=Epoch(0),
    BLS_WITHDRAWAL_PREFIX=0,
    # Time parameters
    SECONDS_PER_SLOT=Second(12),  # seconds
    MIN_ATTESTATION_INCLUSION_DELAY=2 ** 0,  # (= 1) slots
    SLOTS_PER_EPOCH=2 ** 5,  # (= 32) slots
    MIN_SEED_LOOKAHEAD=2 ** 0,  # (= 1) epochs
    MAX_SEED_LOOKAHEAD=2 ** 2,  # (= 4) epochs
    SLOTS_PER_ETH1_VOTING_PERIOD=2 ** 10,  # (= 16) epochs
    SLOTS_PER_HISTORICAL_ROOT=2 ** 13,  # (= 8,192) slots
    MIN_VALIDATOR_WITHDRAWABILITY_DELAY=2 ** 8,  # (= 256) epochs
    PERSISTENT_COMMITTEE_PERIOD=2 ** 11,  # (= 2,048) epochs
    MIN_EPOCHS_TO_INACTIVITY_PENALTY=2 ** 2,
    # State list lengths
    EPOCHS_PER_HISTORICAL_VECTOR=2 ** 16,
    EPOCHS_PER_SLASHINGS_VECTOR=2 ** 13,
    HISTORICAL_ROOTS_LIMIT=2 ** 24,
    VALIDATOR_REGISTRY_LIMIT=2 ** 40,
    # Reward and penalty quotients
    BASE_REWARD_FACTOR=2 ** 6,  # (= 64)
    WHISTLEBLOWER_REWARD_QUOTIENT=2 ** 9,  # (= 512)
    PROPOSER_REWARD_QUOTIENT=2 ** 3,
    INACTIVITY_PENALTY_QUOTIENT=2 ** 25,  # (= 33,554,432)
    MIN_SLASHING_PENALTY_QUOTIENT=2 ** 5,
    # Max operations per block
    MAX_PROPOSER_SLASHINGS=2 ** 4,  # (= 16)
    MAX_ATTESTER_SLASHINGS=2 ** 0,  # (= 1)
    MAX_ATTESTATIONS=2 ** 7,  # (= 128)
    MAX_DEPOSITS=2 ** 4,  # (= 16)
    MAX_VOLUNTARY_EXITS=2 ** 4,  # (= 16)
    # Fork choice
    SAFE_SLOTS_TO_UPDATE_JUSTIFIED=8,
    # Deposit contract
    DEPOSIT_CONTRACT_ADDRESS=decode_hex(
        "0x1234567890123456789012345678901234567890"
    ),  # TBD
)

# NOTE: change this variable to change the package-wide configuration
CURRENT_CONFIG: Eth2Config = SERENITY_CONFIG

_config_profile_mapping = {
    "mainnet": SERENITY_CONFIG,
    "minimal": MINIMAL_SERENITY_CONFIG,
}


def set_config_profile(config_profile: str) -> Eth2Config:
    """
    There are a number of package-wide parameters we can infer from the
    ``config_profile`` which determines if one of the above hard-coded
    configurations is applicable to our application.

    If we can resolve the caller's request, update the global configuration
    ``CURRENT_CONFIG`` in this module.
    """
    config = _config_profile_mapping.get(config_profile)
    if config:
        global CURRENT_CONFIG
        CURRENT_CONFIG = config
    return CURRENT_CONFIG
