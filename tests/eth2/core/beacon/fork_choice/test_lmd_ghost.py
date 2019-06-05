import itertools
import random

import pytest

from eth_utils.toolz import (
    first,
    mapcat,
    merge_with,
    second,
)

from eth2.configs import CommitteeConfig
from eth2.beacon.constants import ZERO_HASH32
from eth2.beacon.committee_helpers import (
    get_current_epoch_committee_count,
    get_crosslink_committees_at_slot,
    get_previous_epoch_committee_count,
)
from eth2.beacon.helpers import get_epoch_start_slot
from eth2.beacon.fork_choice.lmd_ghost import lmd_ghost_scoring, Store
from eth2.beacon.types.attestation_data import AttestationData
from eth2.beacon.types.blocks import BeaconBlock
from eth2.beacon.types.pending_attestations import PendingAttestation
from eth2.beacon.types.states import BeaconState

# genesis_chain_db
# empty attestation pool
# some tests where there are atts in pool but doesn't change the fork choice
# some tests where there are atts in the pool and it _does_ change the fork choice
# state w/ attesting balances


# test cases
# - one block from justified head
# - two blocks from justified head, score them all properly
# - two forks from justified head, score the right fork higher
# - three blocks from justified head, score them all properly
# - three forks from justified head, pick the right fork

def _mk_expected_number_of_attestations(state, valid_slot_range, number_of_attestations, config):
    """
    Create ``number_of_attestations`` sampled uniformly across the ``valid_slot_range``.
    Use the ``state`` to know which validators should participate.

    Returns a collection of (Slot, AttestationData)
    """
    all_committees = []
    for slot in valid_slot_range:
        committees = get_crosslink_committees_at_slot(
            state,
            slot,
            CommitteeConfig(config),
        )
        for committee, _ in committees:
            all_committees.append((slot, committee))

    result = {}
    for slot, committee in random.sample(all_committees,
                                         number_of_attestations):
        for index in committee:
            result[index] = (slot, AttestationData(slot=slot,
                                                   beacon_block_root=ZERO_HASH32,
                                                   source_epoch=0,
                                                   source_root=ZERO_HASH32,
                                                   target_root=ZERO_HASH32,
                                                   shard=0,
                                                   previous_crosslink=None,
                                                   crosslink_data_root=ZERO_HASH32))
    return result


def _mk_pending_attestation(data):
    return PendingAttestation(
        aggregation_bitfield=bytes(),
        data=data,
        custody_bitfield=bytes(),
        inclusion_slot=0,
    )


def _distinct_attestation_filter(state,
                                 config,
                                 attestation_distribution,
                                 previous_epoch_attestations,
                                 current_epoch_attestations,
                                 pool_attestations):
    pass


def _not_distinct_attestation_filter(state,
                                     config,
                                     attestation_distribution,
                                     previous_epoch_attestations_by_index,
                                     current_epoch_attestations_by_index,
                                     pool_attestations_by_index):
    """
    Do not try to ensure that attestations are distinct across sources.
    """
    previous_epoch_attestations = tuple(
        _mk_pending_attestation(data) for _, data in previous_epoch_attestations_by_index.values()
    )
    current_epoch_attestations = tuple(
        _mk_pending_attestation(data) for _, data in current_epoch_attestations_by_index.values()
    )
    pool_attestations = tuple(
        _mk_pending_attestation(data) for _, data in pool_attestations_by_index.values()
    )

    # given how we generate our test cases, may have duplicates in ``pool_attestations``
    # fix this here:
    pool_attestations = tuple(
        filter(
            lambda data:
            data not in previous_epoch_attestations or
            data not in current_epoch_attestations, pool_attestations
        )
    )

    return (
        previous_epoch_attestations,
        current_epoch_attestations,
        pool_attestations,
    )


def _keep_latest_slot(inputs):
    return second(max(inputs, key=first))


@pytest.mark.parametrize(
    (
        "n",
    ),
    [
        (8,),
        (1024,),
    ]
)
@pytest.mark.parametrize(
    (
        "attestation_distribution",
    ),
    [
        (
            {"previous": i,
             "current": j,
             "pool": k},
        ) for i, j, k in itertools.product(range(2), repeat=3)
    ]
)
@pytest.mark.parametrize(
    (
        "distribution_filter",
    ),
    [
        # (_distinct_attestation_filter,),
        (_not_distinct_attestation_filter,),
    ],
)
def test_store_get_latest_attestation(n,
                                      n_validators_state,
                                      sample_beacon_state_params,
                                      empty_attestation_pool,
                                      config,
                                      attestation_distribution,
                                      distribution_filter):
    """
    Given some attestations across the various sources, can we
    find the latest ones for each validator?

    Cases:
    - attestations in just previous_epoch
    - attestations in just current_epoch
    - attestations in just pool
    - combinations of all of the above, where attestations are distinct in each category
    - combinations of all of the above, where attestations are not distinct

    Note: the current parameterization generates some test cases that are effectively duplicates of
    others. Unless performance becomes an issue, don't worry about it for now.
    """
    # create some attestations based on the active validators and the input distribution
    state = n_validators_state

    previous_epoch = state.previous_epoch(config.SLOTS_PER_EPOCH)
    previous_committee_count = get_previous_epoch_committee_count(
        state,
        config.SHARD_COUNT,
        config.SLOTS_PER_EPOCH,
        config.TARGET_COMMITTEE_SIZE,
    )
    current_epoch = state.current_epoch(config.SLOTS_PER_EPOCH)
    current_committee_count = get_current_epoch_committee_count(
        state,
        config.SHARD_COUNT,
        config.SLOTS_PER_EPOCH,
        config.TARGET_COMMITTEE_SIZE,
    )
    next_epoch = state.next_epoch(config.SLOTS_PER_EPOCH)

    previous_epoch_range = range(
        get_epoch_start_slot(previous_epoch, config.SLOTS_PER_EPOCH),
        get_epoch_start_slot(current_epoch, config.SLOTS_PER_EPOCH)
    )

    current_epoch_range = range(
        get_epoch_start_slot(current_epoch, config.SLOTS_PER_EPOCH),
        get_epoch_start_slot(next_epoch, config.SLOTS_PER_EPOCH)
    )

    pool_range = range(
        get_epoch_start_slot(previous_epoch, config.SLOTS_PER_EPOCH),
        get_epoch_start_slot(next_epoch, config.SLOTS_PER_EPOCH) + config.SLOTS_PER_EPOCH,
    )

    previous_epoch_attestations_by_index = _mk_expected_number_of_attestations(
        state,
        previous_epoch_range,
        previous_committee_count * attestation_distribution["previous"],
        config,
    )
    current_epoch_attestations_by_index = _mk_expected_number_of_attestations(
        state,
        current_epoch_range,
        current_committee_count * attestation_distribution["current"],
        config,
    )
    pool_attestations_by_index = _mk_expected_number_of_attestations(
        state,
        pool_range,
        (previous_committee_count + current_committee_count) * attestation_distribution["pool"],
        config,
    )

    expected_index = merge_with(
        _keep_latest_slot,
        previous_epoch_attestations_by_index,
        current_epoch_attestations_by_index,
        pool_attestations_by_index,
    )

    # filter according to our uniqueness requirements
    (
        previous_epoch_attestations,
        current_epoch_attestations,
        pool_attestations
    ) = distribution_filter(
        state,
        config,
        attestation_distribution,
        previous_epoch_attestations_by_index,
        current_epoch_attestations_by_index,
        pool_attestations_by_index,
    )

    # ensure we get the expected results
    state = state.copy(
        previous_epoch_attestations=previous_epoch_attestations,
        current_epoch_attestations=current_epoch_attestations,
    )

    pool = empty_attestation_pool
    for attestation in pool_attestations:
        pool.add(attestation)

    chain_db = None  # not relevant for this test
    store = Store(chain_db, state, pool, BeaconBlock, config)

    for validator_index in range(len(state.validator_registry)):
        expected_attestation_data = expected_index.get(validator_index, None)
        stored_attestation_data = store._get_latest_attestation(validator_index)
        assert expected_attestation_data == stored_attestation_data


def test_lmd_ghost_fork_choice_scoring(sample_beacon_block_params):
    """
    Given some blocks and some attestations, can we score them correctly?
    """
    # slot = 22
    # block = BeaconBlock(**sample_beacon_block_params).copy(
    #     slot=slot,
    # )

    # expected_score = slot

    # score = higher_slot_scoring(block)

    # assert score == expected_score
