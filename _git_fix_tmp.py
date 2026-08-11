# -*- coding: utf-8 -*-
"""Temporary helper: rebuild origin/main tree without the invalid Windows filename,
   and create a child commit via git fast-import (fast-import bypasses path validation)."""
import subprocess
import time

REPO = r"d:/文档/cyc-note"
ORIGIN_SHA = "5c09843d1edcf0e87ca2ec53e85c6edc1a3037bb"
BAD_MARK = "caffeine?"


def git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=REPO, text=True,
                                   encoding="utf-8", errors="replace").strip()


# committer identity
name = git("config", "user.name")
email = git("config", "user.email")
if not name or not email:
    author = git("--no-pager", "log", "-1", "--format=%an <%ae>")
    name, email = author.replace("<", " <").split(" <")
    email = email.rstrip(">")

# list tree entries (-z gives raw, unquoted paths)
raw = subprocess.check_output(["git", "ls-tree", "-r", "-z", ORIGIN_SHA], cwd=REPO)
entries = []
bad_path = None
for line in raw.decode("utf-8").split("\0"):
    if not line:
        continue
    meta, path = line.split("\t", 1)
    if BAD_MARK in path:
        bad_path = path
        print("BAD_PATH:", repr(path))
        continue
    mode, typ, sha = meta.split(" ")
    if typ != "blob":
        print("WARN non-blob:", line)
        continue
    entries.append((mode, sha, path))


def c_quote(path):
    out = ['"']
    for ch in path:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o < 0x20 or o == 0x7F:
            out.append("\\%03o" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


msg = "chore: remove file with invalid Windows filename (? in name)"
lines = [
    "commit refs/heads/_fix",
    "mark :1",
    "committer %s <%s> %d +0800" % (name, email, int(time.time())),
    "data %d" % len(msg.encode("utf-8")),
    msg,
    "from %s" % ORIGIN_SHA,
    "deleteall",
]
for mode, sha, path in entries:
    lines.append("M %s %s %s" % (mode, sha, c_quote(path)))
lines.append("")
stream = "\n".join(lines)

p = subprocess.run(["git", "fast-import", "--quiet"], cwd=REPO,
                   input=stream.encode("utf-8"), capture_output=True)
if p.returncode != 0:
    print("STDERR:", p.stderr.decode("utf-8", "replace"))
    raise SystemExit(1)

fix_sha = git("rev-parse", "refs/heads/_fix")
print("FIX_SHA:", fix_sha)
print("ENTRIES:", len(entries), "(excluded 1 bad path)")
