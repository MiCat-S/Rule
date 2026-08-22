#!/usr/bin/env python3
"""Advance the Yuu518/sing-box-rules rule-set submodule."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_REPOSITORY = "Yuu518/sing-box-rules"
UPSTREAM_URL = f"https://github.com/{UPSTREAM_REPOSITORY}.git"
UPSTREAM_BRANCH = "rule_set"
DESTINATION = ROOT / "upstream" / "Yuu518" / "sing-box-rules"
MANIFEST = ROOT / "upstream" / "Yuu518" / "sing-box-rules.UPSTREAM.json"
RULE_DIRECTORIES = ("rule_set_ip", "rule_set_site")
ALLOWED_SUFFIXES = {".json", ".srs"}


def run_git(arguments: list[str], cwd: Path | None = None) -> str:
    environment = os.environ.copy()
    environment.setdefault("GIT_TERMINAL_PROMPT", "0")
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        env=environment,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def validate_rule_tree(root: Path) -> dict[str, int]:
    json_rules: set[str] = set()
    binary_rules: set[str] = set()
    total_bytes = 0

    for directory_name in RULE_DIRECTORIES:
        directory = root / directory_name
        if not directory.is_dir():
            raise ValueError(f"upstream is missing {directory_name}/")

        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix not in ALLOWED_SUFFIXES:
                raise ValueError(f"unexpected upstream file: {path.relative_to(root)}")
            total_bytes += path.stat().st_size
            key = path.relative_to(root).with_suffix("").as_posix()
            if path.suffix == ".json":
                document = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(document, dict):
                    raise ValueError(f"invalid sing-box rule-set object: {path.relative_to(root)}")
                if not isinstance(document.get("version"), int) or not isinstance(
                    document.get("rules"), list
                ):
                    raise ValueError(f"invalid sing-box rule-set schema: {path.relative_to(root)}")
                json_rules.add(key)
            else:
                if path.stat().st_size == 0:
                    raise ValueError(f"empty binary rule-set: {path.relative_to(root)}")
                binary_rules.add(key)

    missing_binary = sorted(json_rules - binary_rules)
    binary_only = sorted(binary_rules - json_rules)
    if missing_binary:
        raise ValueError(
            "JSON rule sets are missing binary counterparts: "
            f"{missing_binary[:5]}"
        )
    if not binary_rules:
        raise ValueError("upstream contains no rule sets")
    return {
        "rule_sets": len(binary_rules),
        "json_files": len(json_rules),
        "binary_files": len(binary_rules),
        "binary_only": len(binary_only),
        "files": len(json_rules) + len(binary_rules),
        "bytes": total_bytes,
    }


def remote_commit() -> str:
    output = run_git(["ls-remote", UPSTREAM_URL, f"refs/heads/{UPSTREAM_BRANCH}"])
    commit = output.split("\t", 1)[0] if output else ""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"could not resolve {UPSTREAM_BRANCH!r} from {UPSTREAM_URL}")
    return commit


def current_commit() -> str | None:
    if not DESTINATION.is_dir():
        return None
    try:
        value = run_git(["rev-parse", "HEAD"], cwd=DESTINATION)
    except subprocess.CalledProcessError:
        return None
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else None


def sync() -> dict[str, object]:
    if not DESTINATION.is_dir():
        raise ValueError(
            "upstream submodule is missing; run "
            "'git submodule update --init --recursive' first"
        )
    configured_url = run_git(["remote", "get-url", "origin"], cwd=DESTINATION)
    if configured_url.rstrip("/").removesuffix(".git") != UPSTREAM_URL.removesuffix(".git"):
        raise ValueError(f"unexpected submodule origin: {configured_url}")

    run_git(["fetch", "--quiet", "--depth", "1", "origin", UPSTREAM_BRANCH], cwd=DESTINATION)
    commit = run_git(["rev-parse", "FETCH_HEAD"], cwd=DESTINATION)
    run_git(["checkout", "--quiet", "--detach", commit], cwd=DESTINATION)
    stats = validate_rule_tree(DESTINATION)

    manifest: dict[str, object] = {
        "repository": UPSTREAM_REPOSITORY,
        "branch": UPSTREAM_BRANCH,
        "commit": commit,
        "source": f"https://github.com/{UPSTREAM_REPOSITORY}/tree/{commit}",
        **stats,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="only check whether the submodule points to the current upstream commit",
    )
    args = parser.parse_args()

    if args.check:
        remote = remote_commit()
        local = current_commit()
        try:
            manifest_commit = json.loads(MANIFEST.read_text(encoding="utf-8")).get("commit")
        except (json.JSONDecodeError, OSError):
            manifest_commit = None
        if local != remote or manifest_commit != local:
            print(f"upstream submodule is stale: local={local}, remote={remote}")
            return 1
        stats = validate_rule_tree(DESTINATION)
        print(f"upstream submodule is current ({remote[:12]}, {stats['rule_sets']} rule sets)")
        return 0

    manifest = sync()
    print(
        f"synced {manifest['rule_sets']} rule sets ({manifest['files']} files) "
        f"from {manifest['repository']}@{str(manifest['commit'])[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
