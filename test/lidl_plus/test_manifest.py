import json
from pathlib import Path

from custom_components.lidl_plus.const import DOMAIN


def test_manifest():
    root_dir = Path(__file__).parent.parent.parent
    with open(f"{root_dir}/custom_components/lidl_plus/manifest.json") as f:
        manifest = json.load(f)
    assert manifest["domain"] == DOMAIN
    assert manifest["name"] == "Lidl Plus"
    assert manifest["documentation"] == "https://github.com/t0bst4r/hacs-lidl_plus"
