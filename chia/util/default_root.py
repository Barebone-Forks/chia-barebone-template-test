import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("<FORK-UPCASE-TECHNICAL-NAME>_ROOT", "~/.<FORK-TECHNICAL-NAME>/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("<FORK-UPCASE-TECHNICAL-NAME>_KEYS_ROOT", "~/.<FORK-TECHNICAL-NAME>_keys"))).resolve()
