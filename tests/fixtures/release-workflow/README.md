# Offline staged-release fixtures

These fixtures support the [AIC-REQ-06 coverage assessment](../../../experiments/release-workflow/acceptance-review.md).
They are synthetic public examples. No product repository, credential, network
service, Apple toolchain, upload endpoint or announcement channel is used.

`package.json` uses the actual [Release Package 2.0.0 field names](../../../specs/release-package.md#58-version-2-staged-release-contract).
Its explicit example policy assigns release `2026.10` independently of builds
`101` and `102`; neither numbering scheme is a recommendation for a consumer.
Candidate A fails selection; candidate B passes. Both identities and observations
remain in the package. Desktop and Apple-style targets are independently selected.
The Apple-style provider check is pending until after upload.

`a.txt` and `b.txt` are the candidate bytes with SHA-256 identities in the package.
`build_tool.py` is a harmless fixture project tool that writes a ZIP containing a
client, plugin and configuration in a temporary working directory. The harness
invokes this existing tool for both standalone and combined scenarios; it does not
run commands discovered in a real product checkout. A combined build creates a
new candidate and its own output check, preserving the previous candidates.

`local_workflow.py` is test-owned reference execution, **not the Markdown Skill
runtime**. A JSONL receipt journal replaces the provider. Each write has persisted
intent and an exclusive file lock. Tests lose the reply only after a real local
journal append, reload package state, reconcile the journal and verify that the
write count does not increase. Announcement recovery also checks product bytes
and the action journal. Candidate changes and modified delivered bytes block reuse.

`release_contract_v2.py` is a bounded offline reader, not a universal validator.
The fixture stages (`select`, `upload`, `complete`), origin values and supplied
policy dictionaries are test parameters, not a new required project format.
Nonempty evidence references are structurally checked; their external truth and
human authority are not attested. Additional consumer stages or policy mechanisms
need their own verified mapping before use. The tests do not prove the Skills will
follow their instructions in an independent Agent host.

The legacy import example preserves known version/source facts, leaves unknown
build identities and artifacts unknown, and keeps delivery pending. It neither
upgrades a real package nor converts a historical publication claim into new
candidate verification. The historical source bytes remain unchanged.
