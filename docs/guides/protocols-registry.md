---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# Protocol registry and remote loading

An agent should discover and load a protocol through the **protocol registry**, rather than relying on a local file.

---

## The idea

An agent **must not** assume any local file exists. Instead:

```text
Agent workflow:
  1. Know where the registry is — the only thing it knows in advance
  2. Query the registry for protocol information, including the remote URL
  3. Load a protocol remotely as needed
  4. Optionally cache it locally, without depending on the cache
```

---

## 1. The discovery entry point

### A single source of truth

```text
🔗 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md
    ↓
    carries the registry information for every protocol
```

This URL is all an agent needs at startup.

### How a protocol is defined in the manifest

```json
{
  "project": "AI Cortex",
  "version": "2.0.0",

  "registry": {
    "protocols_catalog": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/INDEX.md"
  },

  "protocols": [
    {
      "id": "UNIVERSAL_NOTIFICATION_SPEC_V2",
      "name": "Universal Notification Protocol",
      "version": "1.0.0",
      "domain": "notifications",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",
      "repository": "https://github.com/nesnilnehc/ai-cortex",
      "path": "protocols/unp.md",
      "scope": "Applicable whenever designing or reviewing notification systems"
    },
    {
      "id": "INP_SPEC_V1",
      "name": "IM Notification Protocol",
      "version": "1.0.0",
      "domain": "notifications",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/inp.md",
      "repository": "https://github.com/nesnilnehc/ai-cortex",
      "path": "protocols/inp.md",
      "scope": "Applicable when implementing notification rendering and routing for instant messaging channels"
    }
  ]
}
```

**The fields that matter**:
- `canonical_url` — the protocol's authoritative URL, which is where an agent loads it from
- `domain` — the problem domain the protocol applies to
- `version` — the semantic version
- `repository` — the source repository

---

## 2. The agent's discovery flow

### Step 1: fetch the protocol catalogue

```python
# agent code
manifest_url = "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md"
manifest = fetch_json(manifest_url)

# every available protocol
protocols = manifest["protocols"]
```

### Step 2: query for the protocols relevant to the task's domain

```python
def find_relevant_protocols(task_description, protocols):
    """Find the protocols relevant to a task"""

    relevant = []

    # approach 1: match on keywords
    keywords = {
        "notification": ["UNIVERSAL_NOTIFICATION_SPEC_V2", "INP_SPEC_V1"],
        "logging": ["LOG_SPEC_V1"],  # a future protocol
        "error": ["ERR_SPEC_V1"],    # a future protocol
    }

    for keyword, protocol_ids in keywords.items():
        if keyword in task_description.lower():
            for pid in protocol_ids:
                relevant.append(find_by_id(protocols, pid))

    # approach 2: match on the domain tag
    for protocol in protocols:
        if any(domain in task_description for domain in protocol["domains"]):
            relevant.append(protocol)

    return relevant

# usage
task = "I need to design a notification system"
protocols = find_relevant_protocols(task, manifest["protocols"])
# result: [UNIVERSAL_NOTIFICATION_SPEC_V2, INP_SPEC_V1]
```

### Step 3: load the protocol remotely

```python
def load_protocol(protocol_metadata):
    """Load a protocol from its remote URL"""

    url = protocol_metadata["canonical_url"]
    content = fetch_text(url)

    return {
        "id": protocol_metadata["id"],
        "version": protocol_metadata["version"],
        "content": content,
        "url": url
    }

# usage
for protocol_meta in protocols:
    protocol = load_protocol(protocol_meta)
    inject_into_context(protocol)
```

---

## 3. Version management

### The versioning strategy

```text
Major (breaking changes):
  UNP v1.0.0  ->  UNP v2.0.0 (incompatible)
  URL: .../v1/unp.md  ->  .../v2/unp.md

Minor (new capability):
  UNP v1.0.0  ->  UNP v1.1.0 (compatible)
  URL: .../unp.md is unchanged, always pointing at the newest minor

Patch (bug fix):
  UNP v1.0.0  ->  UNP v1.0.1
  URL unchanged; the fix arrives automatically
```

### Pinning a specific version

```json
// skills/INDEX.md
{
  "protocols": [
    {
      "id": "UNIVERSAL_NOTIFICATION_SPEC_V2",
      "version": "1.0.0",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",

      // optional: URLs for specific versions
      "version_urls": {
        "1.0.0": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.0.0/protocols/unp.md",
        "1.0.1": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.0.1/protocols/unp.md",
        "1.1.0": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.1.0/protocols/unp.md"
      }
    }
  ]
}
```

### How an agent picks a version

```python
def load_protocol_version(protocol_id, version="latest", manifest=None):
    """Load a specific version of a protocol"""

    protocol = find_by_id(manifest["protocols"], protocol_id)

    if version == "latest":
        url = protocol["canonical_url"]
    else:
        url = protocol["version_urls"][version]

    return fetch_text(url)
```

---

## 4. The registry entry format

### A complete registry entry

```yaml
# one element of the protocols array in skills/INDEX.md
{
  "id": "UNIVERSAL_NOTIFICATION_SPEC_V2",                    # globally unique id
  "name": "Universal Notification Protocol",
  "description": "Channel-agnostic semantic layer for notifications",

  # URL information
  "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",
  "repository": "https://github.com/nesnilnehc/ai-cortex",
  "repository_path": "protocols/unp.md",

  # version information
  "version": "1.0.0",
  "status": "active",                    # active | deprecated | experimental
  "lifecycle": "living",                 # whether it is still maintained

  # discovery and loading
  "domain": "notifications",             # the problem domain
  "scope": "Applicable whenever designing or reviewing notification systems",
  "applies_to": ["design", "code-review", "implementation"],

  # relationships
  "related": ["INP_SPEC_V1"],            # related protocols

  # metadata
  "author": "AI Cortex Team",
  "license": "MIT",
  "tags": ["semantic", "channel-agnostic", "notifications"]
}
```

---

## 5. Scenarios

### Scenario 1: an agent's first run in a new project

```text
Agent initialisation:
  1. It knows the registry URL
  2. It fetches skills/INDEX.md
  3. It parses the protocol list
  4. It loads the protocols the task needs
  5. It is ready at once, with nothing configured in advance

From the user's side:
  Agent: "I have loaded the UNP v1.0.0 and INP v1.0.0 protocols"
  User:  "Generate a notification system"
  Agent: ✅ done, using the remotely loaded protocols
```

### Scenario 2: an agent across different organisations

```text
Agent A works at company X:
  manifest_url = "https://company-x.internal/ai-cortex/skills/INDEX.md"
  -> loads company X's protocols

Agent B works at company Y:
  manifest_url = "https://company-y.internal/ai-cortex/skills/INDEX.md"
  -> loads company Y's protocols

Agent C uses AI Cortex:
  manifest_url = "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md"
  -> loads the official AI Cortex protocols
```

### Scenario 3: upgrading an agent's protocol version

```text
The user's code runs on UNP v1.0.0:
  The agent detects that the code uses "UNP v1.0.0"
  The manifest says the newest version is UNP v2.0.0

What the agent may then do:
  1. Ask the user: "a newer UNP exists, upgrade?"
  2. If they agree, load v2.0.0 and produce migration suggestions
  3. Stay backward compatible unless the upgrade is explicitly chosen
```

---

## 6. Implementation notes

### For an agent framework

```python
class ProtocolRegistry:
    def __init__(self, manifest_url: str):
        self.manifest_url = manifest_url
        self.manifest = None
        self._cache = {}  # optional local cache

    def discover(self, domain: str = None) -> List[Protocol]:
        """Discover protocols"""
        if not self.manifest:
            self.manifest = fetch_json(self.manifest_url)

        protocols = self.manifest["protocols"]

        if domain:
            protocols = [p for p in protocols if p.get("domain") == domain]

        return protocols

    def load(self, protocol_id: str, version: str = "latest") -> str:
        """Load a protocol's content"""
        protocol = self._find_by_id(protocol_id)

        # check the cache
        cache_key = f"{protocol_id}:{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # load it remotely
        if version == "latest":
            url = protocol["canonical_url"]
        else:
            url = protocol["version_urls"][version]

        content = fetch_text(url)
        self._cache[cache_key] = content  # optional cache

        return content

    def get_relevant_protocols(self, task_description: str):
        """Get the protocols relevant to a task description"""
        # keyword matching, or semantic similarity
        ...
```

### For a project

```yaml
# .claude/config.yaml
protocols:
  registry_url: https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md

  # optional: pin specific versions
  pinned_versions:
    UNIVERSAL_NOTIFICATION_SPEC_V2: "1.0.0"
    INP_SPEC_V1: "1.0.0"

  # optional: local cache
  cache:
    enabled: true
    directory: ./.claude/protocol-cache
```

---

## 7. Three ways to discover a protocol

### 1. Named explicitly

```python
# the agent loads the protocol by name
registry = ProtocolRegistry("https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md")
unp = registry.load("UNIVERSAL_NOTIFICATION_SPEC_V2")
```

### 2. Inferred from the task

```python
# the agent discovers them from the task
task = "generate a notification system"
protocols = registry.get_relevant_protocols(task)
# discovered -> [UNIVERSAL_NOTIFICATION_SPEC_V2, INP_SPEC_V1]
```

### 3. Declared by the skill

```yaml
# skill frontmatter
---
name: review-notifications
protocols:
  - id: UNIVERSAL_NOTIFICATION_SPEC_V2
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---

# at skill runtime the agent loads the declared protocols
```

---

## 8. Compared with a local clone

| Aspect | Remote loading (recommended) | A local clone (not recommended) |
|:---|:---|:---|
| **Setup** | ✅ 0 steps, just a URL | ❌ requires a clone or download |
| **Statelessness** | ✅ the agent works anywhere | ❌ depends on a local file |
| **Versioning** | ✅ the newest comes from the manifest automatically | ❌ has to be updated by hand |
| **Across projects** | ✅ can load protocols from different sources | ❌ only the local version |
| **Disk** | ✅ stores nothing, caching optional | ❌ takes local space |
| **Network** | ⚠️ needs the network | ✅ works offline, if cached |

---

## 9. The minimum an agent has to integrate

An agent only has to know **this one URL**:

```text
https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md
```

From it, an agent can:
- ✅ discover every available protocol
- ✅ get a protocol's canonical URL
- ✅ load any version of any protocol
- ✅ learn a protocol's domain and scope
- ✅ find the related protocols

---

**Design principles**:

- An agent should be **stateless and unconfigured**
- A protocol should be **discoverable and loadable remotely**
- A version should be **explicit and traceable**
- The only prior knowledge should be **one registry URL**

**Last updated**: 2026-03-25
