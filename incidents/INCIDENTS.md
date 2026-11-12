# Incidents

Appended by hooks. Admin reviews and changes `open` to `resolved: <note>`.

- 2026-11-10T18:47:03+00:00 | open | secret | role=founder | session=73123174 | Write: Blocked (R12): content contains a AWS key. Never store secrets in the repo, logs or memory.
- 2026-11-10T19:31:57+00:00 | open | exfiltration | role=founder | session=73123174 | Edit: Blocked (R16): writing company data outside the repo.
- 2026-11-12T04:19:29+00:00 | open | pii | role=founder | session=t | Write: Blocked (R15): content contains a VN phone number. Customer personal data may live only in data/<role>/private/ (gitignored). Use aggregates or a pseudonym like KH-0012.
