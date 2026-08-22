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

SYNC_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_upstream.py"
SYNC_SPEC = importlib.util.spec_from_file_location("sync_upstream", SYNC_SCRIPT)
sync_upstream = importlib.util.module_from_spec(SYNC_SPEC)
assert SYNC_SPEC.loader is not None
sys.modules[SYNC_SPEC.name] = sync_upstream
SYNC_SPEC.loader.exec_module(sync_upstream)

UPSTREAM_CONVERTER = Path(__file__).resolve().parents[1] / "scripts" / "convert_upstream_rules.py"
UPSTREAM_SPEC = importlib.util.spec_from_file_location(
    "convert_upstream_rules", UPSTREAM_CONVERTER
)
convert_upstream_rules = importlib.util.module_from_spec(UPSTREAM_SPEC)
assert UPSTREAM_SPEC.loader is not None
sys.modules[UPSTREAM_SPEC.name] = convert_upstream_rules
UPSTREAM_SPEC.loader.exec_module(convert_upstream_rules)


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

    def test_upstream_validator_requires_matching_json_and_srs_pairs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory_name in sync_upstream.RULE_DIRECTORIES:
                directory = root / directory_name
                directory.mkdir()
                (directory / "sample.json").write_text(
                    '{"version": 3, "rules": []}\n', encoding="utf-8"
                )
                (directory / "sample.srs").write_bytes(b"srs")

            stats = sync_upstream.validate_rule_tree(root)

        self.assertEqual(stats["rule_sets"], 2)
        self.assertEqual(stats["files"], 4)

    def test_upstream_sing_box_rules_are_converted_to_all_text_targets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "source"
            for directory_name in ("rule_set_site", "rule_set_ip"):
                (source_root / directory_name).mkdir(parents=True)
            (source_root / "rule_set_site/sample.json").write_text(
                json.dumps(
                    {
                        "version": 2,
                        "rules": [
                            {
                                "domain": "exact.example",
                                "domain_suffix": [".suffix.example"],
                                "domain_keyword": ["keyword"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (source_root / "rule_set_ip/sample.json").write_text(
                json.dumps(
                    {"version": 2, "rules": [{"ip_cidr": ["192.0.2.0/24", "2001:db8::/32"]}]}
                ),
                encoding="utf-8",
            )
            output = root / "output"

            manifest = convert_upstream_rules.build(output, source_root, "abc123")

            self.assertEqual(manifest["rules"], 5)
            surge = (output / "surge/rule_set_ip/sample.list").read_text()
            self.assertIn("IP-CIDR,192.0.2.0/24", surge)
            self.assertIn("IP-CIDR6,2001:db8::/32", surge)
            quantumult_x = (output / "quantumult-x/rule_set_site/sample.list").read_text()
            self.assertIn("host-suffix,suffix.example,proxy", quantumult_x)
            self.assertTrue((output / "mihomo/rule_set_site/sample.yaml").is_file())


if __name__ == "__main__":
    unittest.main()
