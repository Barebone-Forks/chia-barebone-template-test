from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "<FORK-TECHNICAL-NAME>_harvester <FORK-TECHNICAL-NAME>_timelord_launcher <FORK-TECHNICAL-NAME>_timelord <FORK-TECHNICAL-NAME>_farmer <FORK-TECHNICAL-NAME>_full_node <FORK-TECHNICAL-NAME>_wallet".split(),
    "node": "<FORK-TECHNICAL-NAME>_full_node".split(),
    "harvester": "<FORK-TECHNICAL-NAME>_harvester".split(),
    "farmer": "<FORK-TECHNICAL-NAME>_harvester <FORK-TECHNICAL-NAME>_farmer <FORK-TECHNICAL-NAME>_full_node <FORK-TECHNICAL-NAME>_wallet".split(),
    "farmer-no-wallet": "<FORK-TECHNICAL-NAME>_harvester <FORK-TECHNICAL-NAME>_farmer <FORK-TECHNICAL-NAME>_full_node".split(),
    "farmer-only": "<FORK-TECHNICAL-NAME>_farmer".split(),
    "timelord": "<FORK-TECHNICAL-NAME>_timelord_launcher <FORK-TECHNICAL-NAME>_timelord <FORK-TECHNICAL-NAME>_full_node".split(),
    "timelord-only": "<FORK-TECHNICAL-NAME>_timelord".split(),
    "timelord-launcher-only": "<FORK-TECHNICAL-NAME>_timelord_launcher".split(),
    "wallet": "<FORK-TECHNICAL-NAME>_wallet".split(),
    "introducer": "<FORK-TECHNICAL-NAME>_introducer".split(),
    "simulator": "<FORK-TECHNICAL-NAME>_full_node_simulator".split(),
    "crawler": "<FORK-TECHNICAL-NAME>_crawler".split(),
    "seeder": "<FORK-TECHNICAL-NAME>_crawler <FORK-TECHNICAL-NAME>_seeder".split(),
    "seeder-only": "<FORK-TECHNICAL-NAME>_seeder".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
