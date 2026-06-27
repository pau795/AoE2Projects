#!/usr/bin/env python
"""Rename one player in an AoE2 DE recorded-game header.

This keeps the recorded-game body byte-for-byte unchanged. Only the compressed
header payload is decompressed, patched, recompressed, and written with an
updated header_length.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from pathlib import Path


RAW_DEFLATE_WBITS = -15
HEADER_PREFIX_SIZE = 8


def _raw_deflate(data: bytes, level: int = 9) -> bytes:
    compressor = zlib.compressobj(level=level, wbits=RAW_DEFLATE_WBITS)
    return compressor.compress(data) + compressor.flush()


def _patch_de_string_at(buf: bytearray, offset: int, old: bytes, new: bytes) -> bool:
    """Patch a DE string whose value starts at offset.

    Format: 60 0a, int16 length, raw bytes.
    """
    if offset < 4:
        return False
    if bytes(buf[offset - 4 : offset - 2]) != b"\x60\x0a":
        return False
    length = struct.unpack_from("<h", buf, offset - 2)[0]
    if length != len(old):
        return False
    struct.pack_into("<h", buf, offset - 2, len(new))
    buf[offset : offset + len(old)] = new
    return True


def _looks_like_de_player_display_name(buf: bytearray, offset: int, name_len: int) -> bool:
    """Return true for the DE player `name` field, false for `censored_name`.

    In the DE player table, censored_name is followed by another DE string
    marker. The actual display name is followed by the player type integer,
    then profile_id.
    """
    next_field = offset + name_len
    return bytes(buf[next_field : next_field + 2]) != b"\x60\x0a"


def _patch_de_profile_id_after_name(
    buf: bytearray,
    offset: int,
    name_len: int,
    profile_id: int,
) -> bool:
    if not _looks_like_de_player_display_name(buf, offset, name_len):
        return False
    profile_offset = offset + name_len + 4
    if profile_offset + 4 > len(buf):
        return False
    struct.pack_into("<I", buf, profile_offset, profile_id)
    return True


def _patch_aoc_string_at(buf: bytearray, offset: int, old: bytes, new: bytes) -> bool:
    """Patch the legacy player-name string whose value starts at offset.

    Format observed in the player block: int16 length including trailing NUL,
    raw bytes, NUL.
    """
    if offset < 2:
        return False
    length = struct.unpack_from("<h", buf, offset - 2)[0]
    if length != len(old) + 1:
        return False
    if offset + len(old) >= len(buf) or buf[offset + len(old)] != 0:
        return False
    struct.pack_into("<h", buf, offset - 2, len(new) + 1)
    buf[offset : offset + len(old) + 1] = new + b"\x00"
    return True


def patch_player_name(
    header: bytes,
    old_name: str,
    new_name: str,
    profile_id: int | None = None,
) -> tuple[bytes, int, int]:
    old = old_name.encode("utf-8")
    new = new_name.encode("utf-8")
    if not old:
        raise ValueError("old player name cannot be empty")
    if len(new) > 32766:
        raise ValueError("new player name is too long for an int16-prefixed header string")

    patched = bytearray(header)
    count = 0
    profile_count = 0
    offset = 0
    while True:
        offset = patched.find(old, offset)
        if offset == -1:
            break
        if _patch_de_string_at(patched, offset, old, new):
            if profile_id is not None and _patch_de_profile_id_after_name(
                patched,
                offset,
                len(new),
                profile_id,
            ):
                profile_count += 1
            count += 1
            offset += len(new)
            continue
        if _patch_aoc_string_at(patched, offset, old, new):
            count += 1
            offset += len(new)
            continue
        offset += len(old)

    return bytes(patched), count, profile_count


def rename_record_player(
    input_path: Path,
    output_path: Path,
    old_name: str,
    new_name: str,
    profile_id: int | None = None,
) -> tuple[int, int]:
    raw = input_path.read_bytes()
    if len(raw) < HEADER_PREFIX_SIZE:
        raise ValueError("input is too small to be an AoE2 recorded game")

    old_header_length, chapter_address = struct.unpack_from("<II", raw, 0)
    if old_header_length <= HEADER_PREFIX_SIZE or old_header_length > len(raw):
        raise ValueError(f"invalid header_length: {old_header_length}")

    compressed_header = raw[HEADER_PREFIX_SIZE:old_header_length]
    decompressed_header = zlib.decompress(compressed_header, wbits=RAW_DEFLATE_WBITS)
    patched_header, patch_count, profile_count = patch_player_name(
        decompressed_header,
        old_name,
        new_name,
        profile_id,
    )
    if patch_count == 0:
        raise ValueError(f"did not find supported header string occurrences for {old_name!r}")

    recompressed_header = _raw_deflate(patched_header)
    new_header_length = HEADER_PREFIX_SIZE + len(recompressed_header)
    output = (
        struct.pack("<II", new_header_length, chapter_address)
        + recompressed_header
        + raw[old_header_length:]
    )
    output_path.write_bytes(output)
    return patch_count, profile_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("old_name")
    parser.add_argument("new_name")
    profile_group = parser.add_mutually_exclusive_group()
    profile_group.add_argument(
        "--profile-id",
        type=lambda value: int(value, 0),
        help="Also replace the renamed DE player's numeric profile id.",
    )
    profile_group.add_argument(
        "--clear-profile-id",
        action="store_true",
        help="Set the renamed DE player's profile id to 0xffffffff.",
    )
    args = parser.parse_args()

    profile_id = 0xFFFFFFFF if args.clear_profile_id else args.profile_id
    try:
        count, profile_count = rename_record_player(
            args.input,
            args.output,
            args.old_name,
            args.new_name,
            profile_id,
        )
    except (OSError, ValueError, zlib.error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"patched {count} header string occurrence(s)")
    if profile_id is not None:
        print(f"patched {profile_count} profile id occurrence(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
