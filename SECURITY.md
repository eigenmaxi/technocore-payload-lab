# Security

This lab publishes a **public** Technocore DID, signed room records, and a
DID note. It does **not** publish the private key or passphrase.

## Never commit

- `identity.pem`
- any `*.pem` or `*.key` file
- the identity passphrase
- `mailbox-name.txt` if you want the mailbox to stay unlisted
- `.venv/`
- `.env` files

`.gitignore` already excludes those patterns. Before every commit:

```bash
git ls-files "*.pem" "*.key"
```

That command must print nothing.

## Public vs private

| Publish | Keep private |
|---|---|
| `did:key:z6Mk...` | `identity.pem` |
| Technocore room and sequence | passphrase |
| contribution URLs | local backup paths |
| DID note URL | Keychain / passphrase file |

A DID is only yours if you control the matching encrypted key. Do not copy a
DID from this repository and treat it as yours.

## Recovery

There is no central recovery service. Back up `identity.pem` and its passphrase
**separately**, outside Git.

The passphrase for this machine is stored in the macOS Keychain service
`technocore-payload-lab` and as a `0600` file under
`~/.local/share/technocore-payload-lab/`.
