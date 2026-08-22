import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "convert_rules.py"
SPEC = importlib.util.spec_from_file_location("convert_rules", SCRIPT)
convert_rules = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = convert_rules
SPEC.loader.exec_module(convert_rules)


class ConvertRulesTests(unittest.TestCase):
    def test_embedded_policy_is_removed_and_options_are_kept(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "sample.Conf"
            source.write_text(
                "DOMAIN-SUFFIX,example.com,DIRECT,extended-matching\n"
                "IP-CIDR,192.0.2.1/24,PROXY,no-resolve\n",
                encoding="utf-8",
            )
            rules = convert_rules.parse_rules(source)

        self.assertEqual(rules[0].canonical, "DOMAIN-SUFFIX,example.com,extended-matching")
        self.assertEqual(rules[1].canonical, "IP-CIDR,192.0.2.1/24,no-resolve")

    def test_build_writes_all_formats_and_reports_ip_asn(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "nested" / "sample.list"
            source.parent.mkdir()
            source.write_text(
                "DOMAIN,example.com\nIP-CIDR6,2001:db8::/32,no-resolve\nIP-ASN,64500\n",
                encoding="utf-8",
            )
            output = root / "generated"
            manifest = convert_rules.build(output, root)

            self.assertEqual(len(manifest["targets"]), 6)
            self.assertTrue((output / "surge/nested/sample.list").is_file())
            self.assertTrue((output / "mihomo/nested/sample.yaml").is_file())
            self.assertTrue((output / "quantumult-x/nested/sample.list").is_file())
            sing_box = json.loads((output / "sing-box/nested/sample.json").read_text())
            self.assertEqual(sing_box["rules"][0]["domain"], ["example.com"])
            self.assertEqual(sing_box["rules"][0]["ip_cidr"], ["2001:db8::/32"])
            unsupported = json.loads((output / "unsupported.json").read_text())
            self.assertEqual(unsupported[0]["rule"], "IP-ASN,64500")


if __name__ == "__main__":
    unittest.main()
