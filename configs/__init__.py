# __init__.py

import pathlib
import toml

path=pathlib.Path(__file__).parent/"base.all.toml"

with path.open(mode='r') as fp:
    cnf = toml.load(fp)
