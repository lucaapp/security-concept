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

(process:tracing)=
# Tracing the Check-In History of an Infected Guest

The goal of this process is to identify {term}`Guest`s that are at a risk of being infected, as a result of having been in contact with an {term}`Infected Guest`.
The process consists of two major parts: {ref}`process:tracing` and {ref}`process:tracing:contacts`.
This chapter describes the first part.

## Overview

```{panels}
Participants
^^^
* {term}`Infected Guest`
* {term}`Guest App`
* {term}`Health Department`
* {term}`Health Department Frontend`
* {term}`Luca Server`

---

Assets
^^^
* {term}`Contact Data`
* {term}`Check-In`
* {term}`Check-In History`

---

Preconditions
^^^
* the {term}`Infected Guest` {ref}`is registered<process:guest_registration>`
* the {term}`Infected Guest` has created at least one {term}`Check-In` (see {ref}`process:guest_checkin`) [^no_checkins]
* the {term}`Infected Guest`'s {term}`Guest App` has retrieved and validated the public key of the current {term}`daily keypair`
* the {term}`Health Department` is onboarded to the Luca system and has access to the {term}`daily keypair`s (see {ref}`process:daily_key`)
* the {term}`Health Department` is in contact with an {term}`Infected Guest`

---

Postconditions
^^^
* the {term}`Health Department` has access to the {term}`Check-In History` of the {term}`Infected Guest`
```

[^no_checkins]: The process can also be trivially performed if the Guest has not created any {term}`Check-In`s but the {term}`Check-In History` will be empty.

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: tracing_history_secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`tracing secret`s
  - Given the consent of the {term}`Infected Guest` the relevant {term}`tracing secret`s are made available to the {term}`Health Department` and the {term}`Luca Server` to reconstruct the {term}`Check-In History`.
  - * {term}`Guest App`
    * {term}`Health Department Frontend`
    * {term}`Luca Server`
* - {term}`data secret`
  - During the process, the {term}`Health Department Frontend` fetches the {term}`Infected Guest`'s {term}`encrypted guest data`, decrypts it using the {term}`data secret`, and displays it.
  - * {term}`Guest App`
    * {term}`Health Department Frontend`
* - {term}`daily keypair`
  - The {term}`Guest App` encrypts the {term}`guest data transfer object` with the public key. The {term}`Health Department` uses the private key for decryption of the same.
  - * {term}`Health Department Frontend`
    * {term}`Guest App` (public key only)
* - {term}`tracing TAN`
  - The TAN is created on the {term}`Luca Server` as an identifier for the encrypted {term}`guest data transfer object` by request of the {term}`Guest App`, which displays it to the Guest. The Guest then communicates it to the {term}`Health Department`.
  - * {term}`Luca Server`
    * {term}`Guest App`
    * {term}`Health Department Frontend`
``````

## Process

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml
hide footbox
skinparam responseMessageBelowArrow true

actor       "Infected Guest"             as G
participant "Guest App"                  as GA
participant "Luca Server"                as LS
participant "Health Department Frontend" as HD
participant "HD Employee"                as HE

G -> GA: activate\nHistory Sharing
activate GA
GA -> LS: guest data\ntransfer object
LS --> GA: tracing TAN
return display tracing TAN

G --> HE: tracing TAN (via telephone)
HE --> HD: enter TAN and start tracing
activate HD
HD -> LS: fetch guest data transfer\nobject for tracing TAN
LS --> HD: guest data transfer object
HD -> HD: decrypt transfer object\nusing daily keypair
HD -> LS: start tracing for\nuser ID and tracing secrets
deactivate HD
activate LS
LS -> LS: generate possible trace IDs
LS -> LS: find Check-Ins for trace IDs

== Continue in Part 2 ==

@enduml
```

The first part of the contact tracing is for the {term}`Health Department` to reconstruct the {term}`Check-In History` of the {term}`Infected Guest`.
Each {term}`Check-In` stored in _luca_ is associated with an unique {term}`trace ID`.
These IDs are derived from the {term}`tracing secret` stored in the {term}`Guest App` (as well as from the Guest's {term}`user ID` and a timestamp).
Hence, given the {term}`Infected Guest`'s {term}`tracing secret`s the {term}`Health Department` can reconstruct the {term}`Infected Guest`'s {term}`trace ID`s and find all relevant {term}`Check-In`s.

### Accessing the Infected Guest's Tracing Secrets

In the first step the {term}`Health Department` needs to acquire the {term}`Infected Guest`'s {term}`tracing secret`s for the epidemiologically relevant timespan.
Each {term}`tracing secret` will allow the {term}`Health Department` to find all {term}`Check-In`s whose {term}`trace ID` is based on this secret.

In the beginning of the process, an {term}`Infected Guest` is directly contacted by a local {term}`Health Department`.
In order to retrieve the Guest's {term}`tracing secret`s the Health Department asks the Guest to reveal their {term}`Contact Data` and {term}`Check-In History` via a functionality in the {term}`Guest App`.

When this functionality is activated, the App creates a {term}`guest data transfer object` that holds all information required for the Health Department's tracing process:

| Asset | Use |
| ----- | --- |
| {term}`tracing secret`s | Needed to reconstruct the Guest's {term}`trace ID`s |
| {term}`user ID`         | Needed to reconstruct the Guest's {term}`trace ID`s |
| {term}`data secret`     | Used to validate and display the {term}`Infected Guest`'s identity in the {term}`Health Department Frontend` |

The data is encrypted using the current {term}`daily keypair`'s public key [^daily_key] and uploaded to the {term}`Luca Server`.
The Luca Server returns a {term}`tracing TAN`, which is a short alpha-numeric identifier for the {term}`guest data transfer object` on the Luca Server and does not carry any further security relevance.

[^daily_key]: Whenever making use of the {term}`daily keypair` the {term}`Guest App` verifies the key's validity and authenticity as described in {ref}`process:daily_key`.

The {term}`Infected Guest` can now pick up their communication with the {term}`Health Department` and spell out the {term}`tracing TAN`.
This allows the Health Department to retrieve the encrypted {term}`guest data transfer object` from the Luca Server.
The transfer object is decrypted using the {term}`daily keypair`'s private key.
Usage of the {term}`daily keypair` within the {term}`Health Department` is detailed in Chapter {ref}`process:daily_key`.

After a short timespan of a few hours the encrypted {term}`guest data transfer object`s are deleted from the {term}`Luca Server`.

### Reconstructing the Infected Guest's Check-In History

The second step is for the {term}`Health Department` to find all venues where the {term}`Infected Guest` has created {term}`Check-In`s within the recent, epidemiologically relevant timespan (e.g. 14 days).

To start the tracing process, the {term}`Health Department` sends the {term}`Infected Guest`'s {term}`tracing secret`s to the {term}`Luca Server`.
Based on the secrets and the affected {term}`user ID`, the Luca Server generates all possible {term}`trace ID`s for the relevant time frame.
Given these {term}`trace ID`s _luca_ can find all {term}`Check-In`s created by that Guest during that time frame---the {term}`Infected Guest`'s {term}`Check-In History`.

The {term}`Luca Server` can use the recovered {term}`Check-In History` to contact all venues the {term}`Infected Guest` has visited.
The process of contacting {term}`Venue Owner`s for lifting the outer layer of encryption in each affected {term}`Check-In` is described in the {ref}`next part <process:tracing:contacts>`.

## Security Considerations

### Correlation of Guest Data Transfer Objects and Encrypted Guest Data

After receiving a {term}`Infected Guest`'s {term}`guest data transfer object` the {term}`Health Department Frontend` uses the contained {term}`user ID` to obtain that Guest's {term}`encrypted guest data` from the {term}`Luca Server`.
This is done in order to display the {term}`Infected Guest`'s {term}`Contact Data` to the {term}`Health Department`.

The {term}`Luca Server` can (indirectly) use this circumstance in order to associate a {term}`guest data transfer object` with the {term}`encrypted guest data` of the same Guest by observing the {term}`Health Department Frontend`'s requests.

### Accidental Upload of Guest Data Transfer Object

Guests could trigger the {term}`Guest App`'s functionality to upload the {term}`guest data transfer object` and request a TAN accidentally or out of curiosity.
This would needlessly upload their encrypted secrets, but they still would not be accessible to the {term}`Luca Server` (as they are encrypted for the {term}`daily keypair`) nor the {term}`Health Department` (as they do not know the TAN).

We believe this risk is acceptable and can further be mitigated by an informative warning message in the {term}`Guest App` when activating the functionality.

