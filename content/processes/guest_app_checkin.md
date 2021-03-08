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

(process:guest_checkin)=
# Check-In via Mobile Phone App

## Overview

```{panels}
Participants
^^^
* {term}`Guest`
* {term}`Guest App`
* {term}`Scanner Operator`
* {term}`Scanner Frontend`
* {term}`Luca Server`

---

Assets
^^^
* {term}`Check-In`
* {term}`Venue Information`

---

Preconditions
^^^
* the {term}`Guest App` is installed
* the {term}`Guest` {ref}`is registered <process:guest_registration>`
* the {term}`Venue Owner` {ref}`is registered <process:venue_registration>`
* the {term}`Scanner Frontend` is ready to scan

---

Postconditions
^^^
* the {term}`Guest` has created a {term}`Check-In` at the {term}`Venue Owner`'s venue
* the {term}`Guest` has checked-out of the venue at a later point in time
* the {term}`Luca Server` has an encrypted record of the above {term}`Check-In` Event
* the {term}`Guest App` has noted the visited location in its local {term}`Check-In History`
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: Guest Check-In Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`data secret`
  - The {term}`Guest`'s secret seed to derive both the {term}`data encryption key` and the {term}`data authentication key`.
    This seed will be encrypted for the {term}`Health Department` in this process before being transported to the {term}`Scanner Frontend` via a QR code and protects the Guest's {term}`Contact Data` stored on the {term}`Luca Server`.
  - Securely stored locally on the mobile device (see {ref}`process:guest_registration` for further details)
* - {term}`data authentication key`
  - A symmetric key derived from the {term}`data secret`, used to bind the {term}`Check-In` data to the current time stamp of the Check-In event.
  - Not stored
* - {term}`tracing secret`
  - Used to generate an anonymous {term}`trace ID` to facilitate {ref}`contact tracing<process:tracing>` by the {term}`Health Department` (after the {term}`Guest` granted access to the {term}`tracing secret` -- rendering them an {term}`Infected Guest`).
  - Securely stored locally on the mobile device
* - {term}`daily keypair`
  - Used to encrypt the above-mentioned {term}`data secret` on the {term}`Guest`'s mobile device before transferring it to the {term}`Scanner Frontend` via a QR code.
  - The public key is obtained from the {term}`Luca Server` [^hdskp_signature]. The private key is known to all {term}`Health Department`s (see {ref}`process:daily_key_rotation` for further details).
``````

[^hdskp_signature]: The provided public key of the {term}`daily keypair` is signed by a {term}`Health Department` using their {term}`HDSKP`. This signature is provided by the {term}`Luca Server` along with said public key.

## Process

This describes how {term}`Guest`s use _luca's_ {term}`Guest App` to generate so-called {term}`Check-In`s at specific venues.
For that, {term}`Venue Owner`s deploy {term}`Scanner Frontend`s that read QR codes generated by the {term}`Guest App`.
Note that there are other ways a {term}`Guest` might check-in to a venue: Please refer to {ref}`badge:check_in` and {ref}`process:guest_self_checkin` for further details.

Check-Ins can be used at a later time by {term}`Health Department`s to reconstruct an {term}`Infected Guest`'s {term}`Check-In History` (given that the {term}`Infected Guest` has given their consent).
Check-Ins of other Guests can be associated with the {term}`Infected Guest`'s {term}`Check-In History` to allow for {ref}`process:tracing`.

In any case the Check-In data that is transferred and stored on the {term}`Luca Server` does not reveal information about the Guest's identity ({ref}`O1 <objective:contact_data>`, {ref}`O2 <objective:checkin>`).
Neither does the Luca system learn about a Guest's habits ({ref}`O3 <objective:checkin_history>`).

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml
actor       "Guest"            as G
participant "Guest App"        as App
participant "Scanner Frontend" as SF
database    "Luca Server"      as LS

== Daily Public Key Update (once per day) ==

?o->    App: Update daily\npublic key
activate App
App ->  LS:  Fetch latest daily public key
LS  --> App: daily public key, creation timestamp, issuer_id,  signature
App ->  LS:  Fetch HDSKP certificate for issuer_id
LS  --> App: HDSKP public key
App --> App: Validate HDSKP and daily public key
deactivate App

== QR Code Generation ==

G   ->  App: Enable Check-In Function
activate App
App ->  App: Prepare QR code\n(repeat once a minute)
activate App
App ->  App: Encrypt contact data reference\nwith daily public key
App --> App: Generate QR code\n(with current trace ID)
deactivate App
App --> SF:  Present QR code
activate SF

== Scanning & Check-In ==

SF  ->  SF:  Validate checksum and timestamp
SF  ->  SF:  Encrypt Check-In with venue public key
SF  ->  LS:  Upload Check-In (Trace ID)
deactivate SF

== Guest Feedback ==

group Frequent Polling [concurrent to the Check-In]
    App ->  LS:  Poll for latest TraceID
    LS  --> App
end
App --> G:   Check-In successful

@enduml
```

### Preparation

Before generating any QR codes to perform Check-Ins the {term}`Guest App` will fetch the latest {term}`daily keypair` public key from the {term}`Luca Server` (see {ref}`process:daily_key_rotation`).
The provided public key comes with a reference to the issuing Health Department, a creation timestamp and a signature by a {term}`Health Department`'s {term}`HDSKP` certificate.
The Guest App must validate this signature before encrypting anything with the fetched public key.
Validation of the signature is subject to the planned improvement {ref}`appendix:planned:hdekp_hdskp`.
Furthermore, keys that are older than seven days are not considered valid anymore.

(process:guest_checkin:scanner_checkin)=
### Scanner Check-In

QR codes generated by the {term}`Guest App` are valid for a short period of time and the whole generation process described below is repeated every minute.
Each {term}`trace ID` is generated as HMAC-SHA256 of the Guest's {term}`user ID` and a current quantized timestamp (clamped to the latest full minute) as `data` and the {term}`tracing secret` as `key`.
The resulting value is truncated to the first 16 bytes.
Subsequently, the Guest App {ref}`asymmetrically encrypts<appendix:algorithms:asymmetric_encryption>` the Guest's {term}`user ID` and the {term}`data secret` for the {term}`daily keypair`.
The IV is defined as the first 16 bytes of the ephemeral public key used in the DLIES.
The Guest App then calculates a {term}`verification tag` as HMAC-SHA256 of the timestamp and the encrypted data as `data` and the {term}`data authentication key` as key, truncated to the first 8 bytes.
A four-byte checksum (truncated SHA256) of all the previously generated data blob is appended as an integrity check to detect faulty QR code reads [^qr_code_checksum].

[^qr_code_checksum]: The QR code standard already includes an error correction mechanism. However, some dedicated QR code scanner hardware acts as keyboard input device to forward QR code data to the _luca_ web application. As this data transfer appears to be error prone, we added checksumming on application level as well.

### QR Code Generation and Check-In

The app generates a new QR code every minute, for each code the app generates the following:

```{code}
timestamp        = UNIX timestamp rounded down to the last full minute (little endian encoding)
trace_id         = HMAC-SHA256(user_id || timestamp, tracing_secret)  # truncated to 16 bytes
ephemeral_keys   = a new secp256r1 key pair (for DLIES with the daily public key)
dh_key           = ECDH(ephemeral_keys.private, daily_keypair.public)
enc_key          = SHA256(dh_key || 0x01)  # truncated to 16 bytes
iv               = ephemeral_keys.public   # truncated to 16 bytes
enc_data         = AES-128-CTR(userId || data_secret, enc_key, iv)
verification_tag = HMAC-SHA256(timestamp || enc_data, data_authentication_key)
```

#### Security Considerations

(process:guest_checkin:security:trace_id)=
##### `trace_id`

The {term}`trace ID` (`trace_id`) depends on the {term}`user ID` (`user_id`) of the Guest, the current quantized timestamp and the Guest's {term}`tracing secret`.
Hence, all {term}`trace ID`s for any given minute can be calculated given the {term}`user ID` and the {term}`tracing secret` (which is stored securely inside the {term}`Guest App`).
Without the tracing secret, the Guest's trace IDs can neither be linked to (a) the Guest themselves (fulfilling {ref}`O2 <objective:checkin>`) nor (b) to other trace IDs of the same Guest (fulfilling {ref}`O3 <objective:checkin_history>`).

If tested positive for Sars-CoV2 a {term}`Guest` may consent to sharing their {term}`tracing secret` with the {term}`Health Department` (rendering them an {term}`Infected Guest`).
This facilitates the Health Department to trace the Infected Guest's {term}`Check-In History` (fulfilling {ref}`O4 <objective:guest_consent>`).
See {ref}`process:tracing` for further details.

To restrict the disclosed time interval of the {term}`Infected Guest`'s {term}`Check-In History` the Guest App regularly changes the {term}`tracing secret` (see {ref}`process:guest_registration:rotate_tracing_secret`).
The Guest App shares only the {term}`tracing secret`s that were valid in an epidemiologically relevant time frame (about two weeks) with the {term}`Health Department` (fulfilling {ref}`O5 <objective:partial_history>`).


(process:guest_checkin:security:verification_tag)=
##### `verification_tag`

The encrypted data `enc_data` is not authenticated as it would usually be the case (cf. Encrypt-then-MAC).
We assume that neither the {term}`Luca Server` nor the {term}`Venue Owner` can benefit from altering `enc_data` in any meaningful way.
Instead, the `verification_tag` binds the {term}`Check-In`'s timestamp to the {term}`data secret` to avoid replay attacks by an adversary that learned about `enc_data` but not the {term}`data secret`.
Otherwise, said adversary might use `enc_data` to create {term}`Check-In`s with the identity of the {term}`Guest` that owns the {term}`data secret`.
Binding the `timestamp` to the data secret mitigates this replay to a short window of opportunity (about one minute) assuming that the {term}`Scanner Frontend` validates that `timestamp`s in Check-Ins are recent.

##### Authenticity of the HDSKP

The {term}`HDSKP` is generated in the {term}`Health Department Frontend` during {ref}`the registration process <process:health_department_registration>` and remains known exclusively to the respective {term}`Health Department`.
Currently, the {term}`Health Department`s provide only verbatim public keys as HDSKP.
A {ref}`future version of Luca<appendix:planned:hdekp_hdskp>` will also provide means to verify the authenticity of the HDSKP against a trusted third party.

#### QR Code Construction

````{margin}
```{list-table}
:header-rows: 1

* - `device_type`
  - `value`
* - iOS
  - 0x00
* - Android
  - 0x01
* - Static
  - 0x02
* - Web App
  - 0x03
* - Form
  - 0x04
```
````

The App then displays a QR code containing:

* `version` (QR code protocol version)
* `device_type`
* `key_id` (ID of the {term}`daily keypair` used for this Check-In)
* `timestamp`
* `trace_id`
* `enc_data`
* `ephemeral_keys.public`
* `verification_tag`
* `checksum`

The payload is concatenated and encoded with ASCII85 to be displayed as a QR code.

(process:guest_checkin:upload)=
### QR Code Scanning, Validation and Check-In Upload

The {term}`Scanner Frontend` reads the above QR code using either a mobile phone camera or a dedicated scanner hardware.
Before doing any further processing, it validates the `checksum` to detect reader errors.
Furthermore, the contained `timestamp` is compared to the Scanner's local clock with a reasonable grace period.
If either the `checksum` or the `timestamp` checks fail, no further processing is performed.
Any further cryptographic validity checks cannot be performed by the {term}`Scanner Frontend`.

Next, the relevant {term}`Check-In` data fields are encrypted by the {term}`Scanner Frontend` using the {term}`venue keypair`'s public key (whose private key is in possession of the {term}`Venue Owner`) as follows:

```{code}
eph_scanner_keys = a new secp256r1 key pair (for DLIES with the venue public key)
dh_key           = ECDH(eph_scanner_keys.private, venue_keypair.public)
enc_key          = SHA256(dh_key || 0x01)  # truncated to 16 bytes
auth_key         = SHA256(dh_key || 0x02)
iv               = random_bytes(16)

version       = 0x03  # protocol version of the encrypted data record
check_in_data = version || key_id || ephemeral_keys.public || verification_tag || enc_data

venue_enc_data     = AES-128-CTR(check_in_data, enc_key, iv)
venue_enc_data_mac = HMAC-SHA256(venue_enc_data, auth_key)
```

At last, the following data is uploaded to the {term}`Luca Server` for each successful {term}`Check-In`.

* `trace_id`
* `scanner_id`
* `device_type`
* `timestamp`
* `venue_enc_data`
* `venue_enc_data_mac`
* `iv`
* `eph_scanner_keys.public`

````{margin}
```{note}
_luca_ stores both the time sent and the time the request was received
```
````

When storing this information the {term}`Luca Server` associates it with the `venue_id` (determined via the `scanner_id`) and the Check-In time.
No further processing is done in the Luca Server.

#### Security Considerations

##### Second Layer of Encryption

As required by {ref}`O6: Venue Consent <objective:venue_consent>`, the {term}`Health Department` shall be prevented from single-handedly decrypting {term}`Guest`'s {term}`Contact Data`.
The Luca system is designed to "replace" the paper-based guest lists in physical venues that provide the same security guarantee.
Hence, {term}`Scanner Frontend`s encrypt the already encrypted {term}`Contact Data` in {term}`Check-In`s and remove this encryption layer only on authoritative request of a {term}`Health Department`.
See {ref}`process:tracing` for further details.

##### Authenticity of {term}`venue keypair`

When encrypting the (encrypted) user data (`enc_data`) and the additional data with the {term}`venue keypair`'s public key the authenticity of that public key is crucial.
Plese refer to the {ref}`security considerations regarding Venue Registration<process:venue_registration:considerations>` for further details.

##### `scanner_id`

The `scanner_id` sent as part of the Check-In data is the only indicator _luca_ can use in order to infer the associated venue.
Forging a non-existent `scanner_id` could potentially allow an attacker to send bogus data to the {term}`Luca Server`.
However, this does not reveal any information to the attacker in any scenario.

On a similar note, knowing the `scanner_id` of a venue basically allows the impersonation of the venue's {term}`Scanner Frontend`.
This is accepted; more specifically, this is specifically desired in the {ref}`Self Check-In scenario <process:guest_self_checkin>`.

### QR Code Scanning Feedback

The described process relies on the uni-directional communication from the {term}`Guest App` to the {term}`Scanner Frontend` to perform a {term}`Check-In` by scanning a dynamic QR code.
Theoretically, this allows Guest Check-Ins even without a constant internet connection of the Guest App.
Nevertheless, user feedback by the {term}`Guest App` for a successfully scanned QR code is seen as desirable.

Therefore, the {term}`Guest App` polls the {term}`Luca Server` via an unauthenticated connection.
This inquires whether a Check-In was uploaded by a {term}`Scanner Frontend` with a {term}`trace ID` that the {term}`Guest App` recently generated.
Once this inquiry polling request is acknowledged by the {term}`Luca Server`, the {term}`Guest App` assumes that a successful QR code scan and Check-In was performed.
Some UI feedback is provided to the {term}`Guest`.

#### Security Considerations

This polling request might leak information about the association of a just checked-in {term}`trace ID` and the identity of the {term}`Guest` (directly contradicting {ref}`O2 <objective:checkin>`).
As mobile phone network typically use NAT, the fact that the {term}`Luca Server` does not log any IP addresses and the connection being unauthenticated, we do accept this risk.