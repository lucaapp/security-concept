---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

import os
import sys
sys.path.insert(0, os.path.abspath('../../lib'))

import plantumlmagic
```

(process:daily_key)=
# Daily Keypair Rotation

## Overview

```{panels}
Participants
^^^
* {term}`Health Department`
* {term}`Health Department Frontend`
* {term}`Luca Server`

---

Assets
^^^
* None

---

Preconditions
^^^
* the {term}`Health Department` is {ref}`registered with the Luca system <process:health_department_registration>`
* the current {term}`daily keypair` is older than its rotation threshold

---

Postconditions
^^^
* a fresh {term}`daily keypair` is generated and published to the {term}`Luca Server`
  * {term}`Guest App`s use the new public key for {term}`Check-In`s
  * all {term}`Health Department`s have access to the new private key for {ref}`contact tracing <process:tracing>`
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: Daily Keypair Rotation Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`daily keypair`
  - {term}`Guest App`s use the {term}`daily keypair`'s public key to encrypt their {term}`contact data reference` for every {term}`Check-In`.
    The {term}`daily keypair` is rotated frequently to minimize potential misuse.
  - Private key is accessible to all {term}`Health Department`s
* - {term}`HDSKP`
  - New {term}`daily keypair` public keys are signed by the {term}`Health Department`'s private key so that {term}`Guest App`s can validate the public key's authenticity.
  - Every {term}`Health Department` maintains their own {term}`HDSKP` locally. Public keys are distributed via the {term}`Luca Server` [^hdeskp_certificate].
* - {term}`HDEKP`
  - New {term}`daily keypair` private keys are encrypted for each {term}`Health Department` via their associated {term}`HDEKP`.
  - Every {term}`Health Department` maintains their own {term}`HDEKP` locally. Public keys are distributed via the {term}`Luca Server` [^hdeskp_certificate].
``````

[^hdeskp_certificate]: Currently, the {term}`Health Department`s provide verbatim public keys as HDSKP/HDEKP, only. A future version of _luca_ will also provide means to verify the authenticity of those public keys against a trusted third party.

(process:daily_key_rotation)=
## Daily Public Key Rotation

For every {term}`Check-In` the {term}`Guest App` encrypts a {term}`contact data reference` with the {term}`daily keypair`.
To mitigate the impact of any single compromised key _luca_ rotates the {term}`daily keypair` frequently.

The rotation will be performed by any {term}`Health Department` that logs in after the last {term}`daily keypair` expired.
The private key is encrypted and shared by all participating {term}`Health Department`s using their associated {term}`HDEKP`s (Health Department Encryption Key Pair) via the {term}`Luca Server`.
The public key (and its creation date) are signed with the {term}`HDSKP` (Health Department Signing Key Pair) and distributed to all {term}`Guest App`s via the {term}`Luca Server`.
This effectively replaces the old {term}`daily keypair`.
All described cryptographic actions are performed in the {term}`Health Department Frontend`, the {term}`Luca Server` never learns the {term}`daily keypair` private key in plaintext form.

Measures are taken to solve race conditions if multiple {term}`Health Department`s try to perform the key rotation simultaneously.
Eventually, all {term}`Health Department`s share the knowledge of the new {term}`daily keypair` and are ready to decipher {term}`Contact Data` of {term}`Check-In`s performed on that day.

### Rotation Process

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml

actor       "Health Department Employee" as E
participant "Health Department Frontend" as HD
participant "Luca Server"                as LS
collections "Other Health Departments"   as HDs
actor       "Other HD Employee"          as Es

E   --> HD: Logs into the HD Frontend

activate HD
HD  ->  LS: Daily Keypair still valid?
LS  --> HD: Expired!

activate HD
HD  ->  LS: Get HDEKP of all HDs
LS  --> HD: [ HDEKPs, ... ]
HD  ->  HD: Generate new daily keypair
HD  ->  HD: Encrypt private key for all HDEKPs
HD  ->  HD: Sign public key with HDSKP
HD  ->  LS: Register new daily keypair

deactivate HD

Es  --> HDs: Logs into th HD Frontend
activate HDs
HDs ->  LS: Daily Keypair still valid?
LS  --> HDs: New encrypted private key
deactivate HDs

@enduml
```

### Key Destruction

Private keys of {term}`daily keypair`s that are older than the epidemiologically relevant time span (specifically, four weeks) can be destroyed.
The {term}`Luca Server` removes all such encrypted private keys for all {term}`Health Department`s.
Furthermore, the {term}`Health Department Frontend` removes all locally stored copies of such private keys.

### Security Considerations

(process:daily_key_rotation:considerations)=
#### Authenticity of HDSKP and HDEKP

Each {term}`Health Department` owns a pair of keypairs, namely {term}`HDSKP` and {term}`HDEKP`.
Those keypairs are used to authenticate and distribute newly generated {term}`daily keypair`s.
Both {term}`HDSKP` and {term}`HDEKP` are generated in the {term}`Health Department Frontend` during {ref}`the registration process <process:health_department_registration>` and remain known exclusively to the respective {term}`Health Department`.
In a {ref}`future version of _luca_<appendix:planned:hdekp_hdskp>`, we plan to certify the public keys of {term}`HDSKP` and {term}`HDEKP` by an independent trusted certificate authority to further strengthen their authenticity guarantees.
