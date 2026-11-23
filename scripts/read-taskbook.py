#!/usr/bin/env python3
"""Write the single root-level taskbook.md from a ZIP or TAR to stdout."""

import argparse
from pathlib import Path
import stat
import sys
import tarfile
import zipfile


ROOT_NAMES = {"taskbook.md", "./taskbook.md"}


def root_member(members, get_name):
    matches = [member for member in members if get_name(member) in ROOT_NAMES]
    if len(matches) != 1:
        raise ValueError("expected exactly one root-level taskbook.md")
    return matches[0]


def read_taskbook(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            entry = root_member(archive.infolist(), lambda member: member.filename)
            file_type = stat.S_IFMT(entry.external_attr >> 16)
            dos_directory = entry.external_attr & 0x10
            if entry.is_dir() or dos_directory or file_type not in (0, stat.S_IFREG):
                raise ValueError("taskbook.md must be a regular file")
            return archive.read(entry)

    with tarfile.open(path, "r:*") as archive:
        entry = root_member(archive, lambda member: member.name)
        if not entry.isfile():
            raise ValueError("taskbook.md must be a regular file")
        with archive.extractfile(entry) as source:
            return source.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        taskbook = read_taskbook(args.archive)
    except (EOFError, OSError, ValueError, RuntimeError, tarfile.TarError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Cannot read taskbook: {error}\n")
    sys.stdout.buffer.write(taskbook)


if __name__ == "__main__":
    main()
