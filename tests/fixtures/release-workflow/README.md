# Static staged-release example

These public example files illustrate the
[Release Package 2.0.0 contract](../../../specs/release-package.md#58-version-2-staged-release-contract).
They do not execute a Skill, product build, upload or announcement.

`package.json` assigns the illustrative release identity `2026.10` independently
of build identities `101` and `102`; this is not a recommended project version
policy. Candidate A has a failed selection check, while candidate B has its own
passed checks and is selected for two targets. The Apple-style target's provider
check remains pending until the required evidence is available. Selection does
not establish delivery, and both target outcomes remain pending.

`a.txt` and `b.txt` are the example artifact bytes. Their SHA-256 identities and
the package's declared fields are checked by
[the static example check](../../../scripts/test-release-package-example.py).
The check neither decides release eligibility nor verifies external evidence.

The former test-owned gate models, local build tool and receipt-journal simulator
were retired during requirement closeout. Their earlier results remain historical
engineering records, not Skill acceptance evidence. Historical consumer checks
remain independent under `scripts/check-stable-consumers.py` and
`scripts/test-stable-consumers.py`.
