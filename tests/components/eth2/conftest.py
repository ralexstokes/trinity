import pytest

from eth2.configs import set_config_profile

# SSZ
@pytest.fixture(scope="function", autouse=True)
def override_ssz_lengths():
    set_config_profile("minimal")
