from __future__ import unicode_literals

import json
from builtins import bytes
from pathlib import Path

import plac

from snips_nlu import load_resources, SnipsNLUEngine


@plac.annotations(
    dataset_path=("Path to the training dataset file", "positional", None,
                  str),
    output_path=("Path of the output model", "positional", None, str),
    config_path=("Path to the NLU engine configuration", "option", "c", str))
def train(dataset_path, output_path, config_path):
    """Train an NLU engine on the provided dataset"""
    with Path(dataset_path).open("r", encoding="utf8") as f:
        dataset = json.load(f)

    config = None
    if config_path is not None:
        with Path(config_path).open("r", encoding="utf8") as f:
            config = json.load(f)

    load_resources(dataset["language"])
    engine = SnipsNLUEngine(config).fit(dataset)
    print("Create and train the engine...")

    serialized_engine = bytes(json.dumps(engine.to_dict()), encoding="utf8")
    with Path(output_path).open("w", encoding="utf8") as f:
        f.write(serialized_engine.decode("utf8"))
    print("Saved the trained engine to %s" % output_path)
