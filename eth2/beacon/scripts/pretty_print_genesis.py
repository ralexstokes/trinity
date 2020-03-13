#!/usr/bin/env python

import argparse
import sys

from ruamel.yaml import YAML
import ssz
from ssz.tools import to_formatted_dict

from eth2.beacon.types.states import BeaconState
from eth2.configs import set_config_profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ssz", type=str, required=True)
    parser.add_argument("--config-profile", type=str, required=True)
    args = parser.parse_args()

    assert args.config_profile in {"mainnet", "minimal"}
    set_config_profile(args.config_profile)

    with open(args.ssz, "rb") as f:
        encoded = f.read()
    state = ssz.decode(encoded, sedes=BeaconState)

    yaml = YAML(typ="unsafe")
    yaml.dump(to_formatted_dict(state), sys.stdout)


if __name__ == "__main__":
    main()
