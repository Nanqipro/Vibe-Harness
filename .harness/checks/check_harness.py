#!/usr/bin/env python3
"""Read-only consistency checks for the portable harness."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
README = HARNESS / "README.md"
PLACEHOLDER = re.compile(r"[<>{}]")
INLINE = re.compile(r"`([^`\n]+)`")
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DEFAULT_PROMPT = re.compile(r"default_prompt:\s*[\"']?.*?\$([a-z0-9-]+)", re.I)
failures: list[str] = []


def fail(message: str, location: str) -> None:
    failures.append(f"✗ {message} [{location}]")


def check_internal_links() -> None:
    for path in sorted(HARNESS.rglob("*.md")):
        if path.is_symlink():
            fail("Harness 文档不能是符号链接", str(path.relative_to(HARNESS.parent)))
            continue
        for token in INLINE.findall(path.read_text(encoding="utf-8")):
            token = token.strip().rstrip(".,:;")
            if not token.startswith(".harness/") or PLACEHOLDER.search(token):
                continue
            target = (HARNESS.parent / token).resolve()
            try:
                target.relative_to(HARNESS)
            except ValueError:
                fail(f"引用路径越出 Harness: {token}", str(path.relative_to(HARNESS.parent)))
                continue
            if not target.exists():
                fail(f"引用路径不存在: {token}", str(path.relative_to(HARNESS.parent)))


def check_skills() -> None:
    readme = README.read_text(encoding="utf-8")
    for directory in sorted(path for path in (HARNESS / "skills").iterdir() if path.is_dir()):
        expected = directory.name
        skill_md = directory / "SKILL.md"
        adapter = directory / "agents" / "openai.yaml"
        location = str(directory.relative_to(HARNESS.parent))
        if directory.is_symlink():
            fail("技能目录不能是符号链接", location)
            continue
        if not skill_md.exists() or not adapter.exists():
            fail("技能文件不完整", location)
            continue
        name = NAME.search(skill_md.read_text(encoding="utf-8"))
        prompt = DEFAULT_PROMPT.search(adapter.read_text(encoding="utf-8"))
        if not name or name.group(1) != expected:
            fail("目录名与 SKILL.md name 不一致", location)
        if not prompt or prompt.group(1) != expected:
            fail("目录名与适配层 default_prompt 不一致", location)
        if f"skills/{expected}/SKILL.md" not in readme:
            fail("技能未被任务路由引用", location)


def main() -> int:
    check_internal_links()
    check_skills()
    if failures:
        print(f"[check-harness] 发现 {len(failures)} 个问题:")
        print("\n".join(failures))
        return 1
    print("[check-harness] 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
