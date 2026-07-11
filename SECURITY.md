# Security

This repository is a **documentation field guide with sanitized code excerpts**. It contains no running service, no credentials, and no personal data: every file has been scrubbed of tokens, keys, hosts, IPs, chat IDs, and private content before publishing.

## If you spot something anyway

If you believe a commit accidentally includes a secret, a real hostname/IP, personal data, or anything else that shouldn't be public:

- Please report it privately via [GitHub's private vulnerability reporting](https://github.com/nickmuchi87/hermes-agents-showcase/security/advisories/new) on this repository,
- or open a plain issue that says only "please check your email" without quoting the sensitive content.

I'll remove it and rotate anything affected. Thank you.

## Scope notes

- The `examples/` scripts are illustrative excerpts. A few run standalone on built-in sample data; none of them talk to real infrastructure from this repo.
- The production system the docs describe runs privately; nothing in this repository grants access to it.
