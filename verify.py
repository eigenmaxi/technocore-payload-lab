#!/usr/bin/env python3
"""Verify a Technocore signed payload without holding the private key.

Technocore signs the UTF-8 bytes of:

    room|nonce|normalized-text

The DID is the public key. If verification succeeds, that DID produced the
text. It does not prove the writer is honest — only that they hold the key.

Usage:
  python verify.py --did DID --room ROOM --nonce NONCE --text TEXT --sig SIG
  python verify.py --example examples/signed-payload.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from technocore_agent import (
    IdentityError,
    ProtocolError,
    message_payload,
    verify_bytes,
)


def verify_message(did: str, room: str, nonce: str, text: str, signature: str) -> str:
    """Return the normalized text if the signature matches the DID."""
    normalized, payload = message_payload(room, nonce, text)
    verify_bytes(did, signature, payload)
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--did")
    parser.add_argument("--room")
    parser.add_argument("--nonce")
    parser.add_argument("--text")
    parser.add_argument("--sig")
    parser.add_argument("--example", type=Path)
    args = parser.parse_args()

    if args.example is not None:
        data = json.loads(args.example.read_text(encoding="utf-8"))
        did = data["did"]
        room = data["room"]
        nonce = str(data["nonce"])
        text = data["text"]
        signature = data["sig"]
    else:
        missing = [
            name
            for name in ("did", "room", "nonce", "text", "sig")
            if getattr(args, name) in {None, ""}
        ]
        if missing:
            parser.error("provide --example or all of --did --room --nonce --text --sig")
        did = args.did
        room = args.room
        nonce = args.nonce
        text = args.text
        signature = args.sig

    try:
        normalized = verify_message(did, room, nonce, text, signature)
    except (IdentityError, ProtocolError) as error:
        print(f"invalid: {error}", file=sys.stderr)
        return 1

    print("valid")
    print(f"did: {did}")
    print(f"room: {room}")
    print(f"nonce: {nonce}")
    print(f"payload: {room}|{nonce}|{normalized}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
