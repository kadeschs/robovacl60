"""Tests for the L60 DPS payload decoders."""

import base64

import pytest

from custom_components.robovacl60.vacuum import (
    decode_l60_error_codes,
    decode_mode_string,
    decode_status_string,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("BgoAEAUyAA==", "cleaning"),
        ("BgoAEAVSAA==", "cleaning"),
        ("CAoAEAUyAggB", "paused"),
        ("BBAHQgA=", "returning"),
        ("BBADGgA=", "docked"),
        ("BhADGgIIAQ==", "docked"),
        ("AA==", "docked"),
        ("AhAB", "docked"),
    ],
)
def test_decode_status_string(raw, expected):
    assert decode_status_string(raw) == expected


def test_decode_status_string_unknown():
    assert decode_status_string("zzzz") == "unknown (zzzz)"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("BBoCCAE=", "auto"), ("AggN", "pause"), ("AggG", "home"), ("AggB", "room")],
)
def test_decode_mode_string(raw, expected):
    assert decode_mode_string(raw) == expected


def _varint(n: int) -> bytes:
    out = b""
    while True:
        byte, n = n & 0x7F, n >> 7
        if n:
            out += bytes([byte | 0x80])
        else:
            return out + bytes([byte])


def _error_code(body: bytes) -> str:
    """Build a length-prefixed, base64 ErrorCode payload like DPS 177."""
    stamp = b"\x08" + _varint(116474227125683100)  # field 1: uptime stamp
    payload = stamp + body
    return base64.b64encode(_varint(len(payload)) + payload).decode()


@pytest.mark.parametrize(
    "raw",
    [
        # Real L60 payloads from Nov 7 2026: uptime stamp + empty new_code = no error
        "DAich8KqlJbzzgFSAA==",
        "DAjovL6SlZbzzgFSAA==",
        "CONNECTION_FAILED",
        "",
        None,
        0,
        "!!!not-base64",
    ],
)
def test_decode_error_codes_none(raw):
    assert decode_l60_error_codes(raw) == set()


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        (b"\x10" + _varint(2), {2}),  # field 2 error, varint
        (b"\x12\x02" + _varint(7) + _varint(19), {7, 19}),  # field 2 packed
        (b"\x18" + _varint(4), {4}),  # field 3 warning
        (b"\x52\x02\x08\x05", {5}),  # field 10 new_code.error
        (b"\x10\x00", set()),  # code 0 means none
    ],
)
def test_decode_error_codes_present(body, expected):
    assert decode_l60_error_codes(_error_code(body)) == expected


def test_decode_error_codes_int():
    assert decode_l60_error_codes(3) == {3}
