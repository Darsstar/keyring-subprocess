import os
from pathlib import Path

import keyring

keyring_path = Path() / ".nox" / "keyring" / "Scripts"

os.environ["PATH"] = f"{keyring_path.absolute()}{os.pathsep}{os.environ['PATH']}"

bla = keyring.get_keyring()

credential = bla.get_credential(
    "https://pkgs.dev.azure.com/NKI-AVL/_packaging/Mirror/pypi/simple/",
    None,
)

print(f"username={credential.username}")
print(f"password={credential.password}")
