---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
(process:guest_registration)=
# Guest Registration

In this process a new {term}`Guest` registers to the Luca system.
This process is required for Guests using the {term}`Guest App`.
During this process, local secrets are created, the Guest enters their {term}`Contact Data` and identifiers and encrypted data are sent to the {term}`Luca Server`.

## Overview

```{panels}
Participants
^^^
* {term}`Guest`
* {term}`Guest App`
* {term}`Luca Server`

---

Assets
^^^
* {term}`Contact Data`

---

Preconditions
^^^
* the Guest is not registered
* the Guest App is installed

---

Postconditions
^^^
* the Guest has a {term}`user ID` and a {term}`guest keypair`
* the {term}`Guest App` has stored the private key material and secrets
* the {term}`Luca Server` has stored the encrypted {term}`Contact Data`
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: Guest Registration Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`data secret`
  - A secret "seed"[^secret_seed] which is used to derive both the {term}`data encryption key` and the {term}`data authentication key`.
    This seed is the secret that is encrypted twice before being sent to the {term}`Luca Server` during {ref}`Check-In <process:guest_checkin:scanner_checkin>` and ultimately protects the Guest's {term}`Contact Data`.
  - Securely[^device_storage] stored locally on the mobile device
* - {term}`data encryption key`
  - A symmetric key derived from the {term}`data secret`, used to encrypt the {term}`Contact Data`.
  - Not stored
* - {term}`data authentication key`
  - A symmetric key derived from the {term}`data secret`, used to authenticate the {term}`Contact Data`. It is also used to authenticate {term}`Check-In`s.
  - Not stored
* - {term}`tracing secret`
  - Used by the {term}`Guest App` to generate {term}`trace ID`s during {ref}`Check-In <process:guest_checkin:scanner_checkin>` and (after the {term}`Guest` granted access to it) by the {term}`Health Department` for {ref}`contact tracing<process:tracing>`.
  - Securely stored locally on the mobile device
* - {term}`guest keypair`
  - A pair of public and private key that is used to authenticate both new and updated {term}`encrypted guest data`.
  - The public key is stored on the {term}`Luca Server`. The private part is securely stored locally on the mobile device.
``````
[^secret_seed]: The reason for deriving the two secrets from a seed rather than creating both of them at random is the limited "storage capacity" of the QR code during {ref}`Check-In <process:guest_checkin:scanner_checkin>`.
[^device_storage]: All secrets stored on the device are protected using the respective OS' native credential storage mechanism. Specifically, the [Android keystore system](https://developer.android.com/training/articles/keystore) on Android and the [iOS Keychain Services](https://developer.apple.com/documentation/security/keychain_services) on iOS.

## Process

The diagram below provides an overview to the complete process.

```{code-cell} ipython3
:tags: [remove-input]

import os
import sys
sys.path.insert(0, os.path.abspath('../../lib'))

import plantumlmagic
```

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml
actor       "Guest"         as G
participant "Guest App"     as App
database    "Luca Server"   as LS
control     "SMS Service"   as SMS

G   ->  App: provide Contact Data
App ->  LS:  send phone number
LS  ->  SMS: instruct to send message\n(target phone number,\nmessage text)
SMS -->  G:  send verification TAN (via SMS or voice message)
G   ->  App: enter verification TAN
App ->  LS:  send TAN
LS  ->  LS: verify TAN
LS  --> App: verification result
App ->  App: generate secrets
App ->  App: encrypt contact data
App ->  LS:  send encrypted guest data
LS  --> App: return unique user ID
App --> G:   display QR Code
@enduml
```

### Creating the Secrets

On initial startup the {term}`Guest App` generates the following secrets:
* {term}`data secret` as 16 bytes of random data
* {term}`tracing secret` as 16 bytes of random data
* {term}`guest keypair` as an EC `secp256r1` keypair

It stores this data[^device_storage].
The Guest App then derives two keys from {term}`data secret` as follows:
* {term}`data encryption key` as `SHA256(data secret || 0x01)`, truncated to 16 bytes
* {term}`data authentication key` as `SHA256(data secret || 0x02)`

The derived keys are used in the remainder of the registration process but are not persisted on the device.

### Verifying the Contact Data

Upon first launch of the {term}`Guest App` the {term}`Guest` provides their {term}`Contact Data` to the App.

The App then verifies the Guest's phone number.
For that, the phone number the Guest entered is sent to the {term}`Luca Server`, which then creates a challenge.
Using an external {term}`SMS Service Provider` a {term}`verification TAN` is sent to that phone number either as an SMS or as a voice call.
After entering the TAN in the App it is verified by the {term}`Luca Server`.
The {term}`Luca Server` keeps no record of the Guest's phone number after that [^sms_storage].

[^sms_storage]: According to the German "Telekommunikationsgesetz" the SMS Service Provider is legally required to store the messages for 90 days.

(process:guest_registration:encryption)=
### Encrypting the Contact Data

If the TAN verification is successful, the {term}`Guest App` creates and signs {term}`encrypted guest data` as follows:
```{code} python
# pseudocode

iv = random_bytes(16)

encrypted_guest_data = AES_128(contact_data + data_authentication_key,
                               key=data_encryption_key,
                               mode=CTR,
                               iv=iv)

guest_data_mac = HMAC(encrypted_guest_data,
                      key=data_authentication_key)

guest_data_signature = guest_keypair.private.sign(encrypted_guest_data +
                                                  data_authentication_key +
                                                  iv)
```

The artifacts created here are uploaded to the {term}`Luca Server` in the next step.

### Registering to the Luca Server

The {term}`Guest App` sends the following data to the {term}`Luca Server`:
* the {term}`encrypted guest data`
* the `IV` used in the encryption
* the `guest data mac`
* the `guest data signature`
* the public key of the {term}`guest keypair`

The {term}`Luca Server` returns the Guest's {term}`user ID`. In the end of the process the two participants have stored the following data:

```{panels}
Guest App
^^^
* {term}`user ID`
* {term}`data secret`
* {term}`tracing secret`
* {term}`guest keypair` (public and private key)

---

Luca Server
^^^
* {term}`user ID`
* the {term}`guest keypair`'s public key
* the {term}`encrypted guest data`

```

### Updating the Contact Data

Guests should be able to update their {term}`Contact Data`.
This is needed, for example, in case their address or phone number changes.
Whenever a Guest changes their {term}`Contact Data` in the {term}`Guest App`, the App creates a new {term}`encrypted guest data` package by repeating the steps described in the Section {ref}`process:guest_registration:encryption`.
Using the {term}`user ID` retrieved during the initial registration, the App uploads the following data to the {term}`Luca Server`:
* the {term}`encrypted guest data`
* the `IV` used in the encryption
* the `guest data mac`
* the `guest data signature`

The {term}`Luca Server` verifies that the Guest is authorized to update the data by checking the signature with the already present {term}`guest keypair`'s public key.

(process:guest_registration:rotate_tracing_secret)=
### Rotating the Tracing Secret

The {term}`tracing secret` is used by the {term}`Guest App` to generate the {term}`trace ID`s for {term}`Check-In`s.
Whoever knows a {term}`tracing secret` (and the respective {term}`user ID`) can calculate all {term}`trace ID`s the App has derived from this secret and thus reconstruct a part of the Guest's {term}`Check-In History`.

This is desired, of course, when an {term}`Infected Guest` consents to revealing their {term}`tracing secret` to the {term}`Health Department` during {ref}`Contact Tracing<process:tracing>`.
However, the Health Department should only learn the epidemiologically relevant part of the Guest's Check-In History (cf. {ref}`Security Objective O5<objective:partial_history>`).

To guarantee this, the {term}`Guest App` rotates the {term}`tracing secret` once a day.
If the Guest is infected, the App transfers all recent, epidemiologically relevant, {term}`tracing secret`s to the {term}`Health Department`.
As a result, the Health Department can only reconstruct that part of the {term}`Check-In History` which has been created based on the shared {term}`tracing secret`s.
