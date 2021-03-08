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

(process:tracing:contacts)=
# Finding Potential Contact Persons

## Overview

```{panels}
Participants
^^^
* {term}`Traced Guest`s
* {term}`Luca Server`
* {term}`Health Department`
* {term}`Health Department Frontend`
* {term}`Venue Owner`
* {term}`Venue Owner Frontend`

---

Assets
^^^
* {term}`Contact Data`
* {term}`Check-In`
* {term}`Check-In History` (acquired in the {ref}`previous part<process:tracing>`)

---

Preconditions
^^^
* the {term}`Health Department` has the {term}`Check-In History` of the {term}`Infected Guest`
---

Postconditions
^^^
* the {term}`Health Department` has access to the {term}`Contact Data` of all {term}`Traced Guest`s
```


## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: tracing_contacts_secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`data secret`
  - The {term}`data secret`s of all {term}`Traced Guest`s are made accessible to the {term}`Health Department` in the process in order to decrypt the {term}`encrypted guest data`.
  - * doubly encrypted in each {term}`Check-In`
    * encrypted with the {term}`daily keypair`, then decrypted, in the {term}`Health Department Frontend`
* - {term}`venue keypair`
  - The keypair's private key is used in the {term}`Venue Owner Frontend` to decrypt the outer layer of encryption on the {term}`contact data reference` and the Additional Data in each {term}`Traced Guest`'s {term}`Check-In`.
  - * {term}`Venue Owner Frontend`
* - {term}`daily keypair`
  - The keypair's private key is used in the {term}`Health Department Frontend` to decrypt the inner layer of encryption on the {term}`contact data reference` in each {term}`Traced Guest`'s {term}`Check-In`.
  - * {term}`Health Department Frontend`
``````

## Process

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml
hide footbox
skinparam responseMessageBelowArrow true

actor       "Venue Owner"          as VO
participant "Venue Owner Frontend" as VOF
participant "Luca Server"          as LS
participant "Health Department"    as HD
participant "HD Employee"          as HE

== Continues from Part 1 ==

activate LS
LS --> VO: ask to assist in contact tracing
VO --> VOF: activate tracing\n(agree to assist)
activate VOF
VOF -> LS: fetch double-encrypted\ncontact data references
VOF -> VOF: decrypt outer\nencryption layer\n(using venue keypair)
VOF --> LS: encrypted contact\ndata references
deactivate VOF
deactivate LS

...The Health Department Employee can request the tracing results at any time in the process.\nluca will return those results that have already been made available by the Venue Owner....
HE --> HD: request tracing results
activate HD
HD -> LS: fetch encrypted\ncontact data references
activate LS
LS --> HD: encrypted contact\ndata references
HD -> HD: decrypt contact\ndata references\n(using daily keypair):\nuser IDs, data secrets
HD -> LS: fetch encrypted\nguest data (user IDs)
LS --> HD: encrypted guest data
deactivate LS
HD -> HD: decrypt guest data\n(using data secret):\nContact Data for\neach Traced Guest
return display Contact Data of\npotential contact persons

@enduml
```

Given the {term}`Infected Guest`'s {term}`Check-In History` (obtained in {ref}`part 1 above<process:tracing>` the {term}`Luca Server` determines all {term}`Venue Owner`s whose venues have been visited by this Guest.
Each of them is contacted using the {term}`Venue Information` provided during {ref}`process:venue_registration` and asked to reveal the encrypted {term}`contact data reference`s of potential contact persons ({term}`Traced Guest`s).

When a {term}`Venue Owner` has been contacted to assist in contact tracing they use the respective functionality in the {term}`Venue Owner Frontend`.
The {term}`Venue Owner Frontend` proceeds to download all {term}`Check-In`s registered for this venue that coincide with the visit of the {term}`Infected Guest` from the {term}`Luca Server`.
For each of these {term}`Check-In`s both the outer encryption layer on the {term}`contact data reference` and the Additional Data are decrypted using the private key of this venue's {term}`venue keypair`.
Note that, after the decryption, the {term}`contact data reference` is still encrypted with they {term}`daily keypair` and thus only accessible to the {term}`Health Department` (see {ref}`process:guest_checkin`).

The data is uploaded back to the {term}`Luca Server` in order to be shared with the {term}`Health Department` that initiated the tracing.

After decrypting the {term}`contact data reference`s the Health Department possesses each {term}`Traced Guest`'s {term}`user ID` and {term}`data secret`.
It fetches the Guests' {term}`encrypted guest data` from the {term}`Luca Server` using the {term}`user ID` and decrypts it using the {term}`data encryption key` (derived from the {term}`data secret`) to obtain the {term}`Contact Data` and the {term}`data authentication key`.
The latter is used to verify the authenticity of both the {term}`Check-In` and the {term}`contact data reference`.
The {term}`Contact Data` can now be used to contact the {term}`Traced Guest` and inform them that they are at risk of being infected.

## Security Considerations

### Authentication of Contact Data and Check-Ins

The {term}`data authentication key` is used to authenticate both the {term}`contact data reference` in the {term}`Check-In` (using the {term}`verification tag`) and the {term}`Contact Data`.
However, the {term}`data authentication key` has to be retrieved by deriving the {term}`data secret` contained in the {term}`contact data reference`.

This is unusual (cf. Encrypt-then-MAC), but we consider it sound.
Please refer to {ref}`the Security Considerations regarding Guest Check-In<process:guest_checkin:security:verification_tag>` for further details.

### Possible Abuse of Traced Guests' Data Secrets

In the process described above the {term}`Health Department` obtains each {term}`Traced Guest`'s {term}`data secret` and derives the symmetric {term}`data authentication key` from it.
It uses this key to validate the authenticity of the {term}`Check-In`s, verifying that the {term}`Check-In`s it received from the {term}`Luca Server` have in fact been created by the owner of the {term}`data secret` (the {term}`Traced Guest`).

However, having learned the {term}`data secret`, the {term}`Health Department` can now itself create apparently valid {term}`Check-In`s for that {term}`Traced Guest`.
Neither the {term}`Luca Server` nor another {term}`Health Department` can distinguish these forged {term}`Check-In`s from authentic ones.

Note that the {term}`Health Department` does not know {term}`Traced Guest`s' {term}`tracing secret`s here.
Hence, the forged {term}`Check-In`s would not appear in the Guest's {term}`Check-In History`.
They would, however, appear whenever the forged {term}`Check-In` coincides in time and place with another {term}`Traced Guest`'s {term}`Check-In`.
