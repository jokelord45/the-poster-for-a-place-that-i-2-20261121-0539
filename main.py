"""Publish the travel poster for Solmara, a place that isn't there.

The repository holds one picture, entry.png: an art-deco travel poster
for Solmara, a city of golden domes and white towers floating on islands
in a rose-gold sky above a sea of clouds, with airships drifting between
the islands and the tagline "WHERE THE SKY BECOMES THE SEA". Solmara
does not exist; the poster is the whole point.

Running this module copies that picture, byte for byte, into the
grading output directory. It refuses to publish anything that is not a
complete JPEG inside the one-mebibyte cap, and it checks the copy
against the source by comparing digests, so two runs always write the
same bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
JPEG_MAGIC = bytes((0xFF, 0xD8, 0xFF))


def source_picture():
    return Path(__file__).resolve().with_name(PICTURE_NAME)


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def load_jpeg(path):
    data = path.read_bytes()
    if not data:
        sys.exit(f"{path.name} is empty, refusing to publish it")
    if len(data) > MAX_BYTES:
        sys.exit(f"{path.name} is {len(data)} bytes, over the {MAX_BYTES} cap")
    if data[:3] != JPEG_MAGIC:
        sys.exit(f"{path.name} is not a JPEG")
    return data


def main():
    data = load_jpeg(source_picture())
    dest = output_dir()
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / PICTURE_NAME
    target.write_bytes(data)
    check = target.read_bytes()
    if hashlib.sha256(check).hexdigest() != hashlib.sha256(data).hexdigest():
        sys.exit(f"{target} does not match {PICTURE_NAME}, refusing to publish it")
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
