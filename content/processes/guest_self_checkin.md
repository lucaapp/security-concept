(process:guest_self_checkin)=
# Check-In via a Printed QR Code

This variation allows the {term}`Guest App` to create {term}`Check-In`s by scanning a printed QR code.
For instance, a restaurant might place such a QR code on each available table.
In contrast to the {ref}`conventional check-in <process:guest_checkin>` the {term}`Scanner Frontend` is not involved.
Instead, the {term}`Guest App` assumes the role of the scanner and generates a {term}`Check-In` single-handedly.

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
* {term}`Check-In`

---

Preconditions
^^^
* the {term}`Guest App` is installed
* the {term}`Guest` {ref}`is registered <process:guest_registration>`
* the {term}`Venue Owner` {ref}`is registered <process:venue_registration>`

---

Postconditions
^^^
* the {term}`Guest` has created a {term}`Check-In` at the {term}`Venue Owner`'s venue
* the {term}`Luca Server` has an encrypted record of the above {term}`Check-In` event
* the {term}`Guest App` has noted the visited location in its local {term}`Check-In History`
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 1
:name: Self Check-In Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`data secret`
  - The {term}`Guest`'s secret seed to derive both the {term}`data encryption key` and the {term}`data authentication key`.
    This seed will be encrypted for the {term}`Health Department` in this process and protects the Guest's {term}`Contact Data` stored on the {term}`Luca Server` (cf. {term}`contact data reference`).
  - Securely stored locally on the mobile device (see {ref}`process:guest_registration` for further details).
* - {term}`tracing secret`
  - Used to generate an anonymous {term}`trace ID` to facilitate {ref}`contact tracing<process:tracing>` by the {term}`Health Department` (after the {term}`Guest` granted access to the {term}`tracing secret` -- rendering them an {term}`Infected Guest`).
  - Securely stored locally on the mobile device.
* - {term}`daily keypair`
  - Used to encrypt the above-mentioned {term}`data secret` on the {term}`Guest`'s mobile device before transferring it to the {term}`Scanner Frontend` via a QR code.
  - The public key is obtained from the {term}`Luca Server` [^hdskp_signature].
    The private key is known to all {term}`Health Department`s.
    (see {ref}`process:daily_key_rotation` for further details).
* - {term}`venue keypair`
  - Establishes a second encryption layer for the {term}`contact data reference` that is already encrypted with the {term}`daily keypair`.
  - Public key is known to the {term}`Luca Server` and downloaded by the {term}`Guest App` while checking in. Private key is stored by the {term}`Venue Owner`.
``````

[^hdskp_signature]: The provided public key of the {term}`daily keypair` is signed by a {term}`Health Department` using their {term}`HDSKP`. This signature is provided by the {term}`Luca Server` along with said public key.

## Process

In this variation the {term}`Guest App` conceptually assumes the role of the {term}`Scanner Frontend` as described in {ref}`the convential Check-In process <process:guest_checkin>`.
The {term}`Guest App` gains all required information from printed QR codes provided by the {term}`Venue Owner`.

### Printed QR Code Generation

To facilitate this feature, the {term}`Venue Owner` generates and provides QR codes that encode the following information:

* a valid {term}`scanner ID` for their venue
* Optional: pre-defined {ref}`additional data <process:additional_data>` fields

Those QR codes are then printed and visibly placed at the venue for {term}`Guest`s to scan using the {term}`Guest App`.
For instance, in a restaurant the {term}`Venue Owner` might place a unique QR code on each table and note the table number in the QR code's additional data.

### Check-In via the Guest App

To check-in, {term}`Guest`s scan the printed QR code using their {term}`Guest App`.
The {term}`Guest App` can now use the {term}`scanner ID` encoded in the QR code to retrieve the {term}`venue keypair`'s public key from the {term}`Luca Server`.

The {term}`Guest App` now proceeds just like for {ref}`the conventional Check-In process <process:guest_checkin:scanner_checkin>`.
Most notably, it fetches and validates the {term}`daily keypair` [^hdskp_signature] from the {term}`Luca Server`, generates a valid {term}`trace ID` using its {term}`tracing secret` and a {term}`contact data reference` (encrypted for the {term}`daily keypair`).

In {ref}`the conventional Check-In process <process:guest_checkin:upload>` this data would now be encoded into a QR code and presented to a {term}`Scanner Frontend` to finish up the {term}`Check-In` and upload it to the {term}`Luca Server`.
Instead, the {term}`Guest App` re-encrypts the generated data for the {term}`venue keypair`, associates it with the {term}`scanner ID` and uploads the finalized {term}`Check-In` to the {term}`Luca Server` itself.

The resulting {term}`Check-In` is equivalent to a {term}`Check-In` performed by the {term}`Scanner Frontend`.

## Security Considerations

### Authenticity of the {term}`venue keypair`

The printed QR code merely contains a {term}`scanner ID` which is used to fetch the public key of the {term}`venue keypair` from the {term}`Luca Server`.
At the moment, there is no way for the {term}`Guest App` to validate the authenticity of this public key.
A later version of the printed QR codes will contain the {term}`venue keypair`'s public key directly.

Note, however, that the impact of a malicious public key is limited in this scenario as it only affects the outer layer of the {term}`contact data reference`'s encryption.
The {term}`contact data reference` is still encrypted for the {term}`daily keypair` and thus only accessible for the {term}`Health Department`.
Nevertheless, a theoretical collusion between the {term}`Luca Server` and the {term}`Health Department` could still harm security objective {ref}`O6 <objective:venue_consent>`.

Until the mentioned improvement is implemented, this risk is accepted.

### Authenticity of Printed QR Codes

By nature, QR codes are easily forgable by simply copying them.
Hence, an attacker might maliciously replace QR codes of one venue with another one.
This would lead to misguided {term}`Check-In`s by {term}`Guest`s and eventually generate false information for {term}`Health Department`s during {ref}`contact tracing <process:tracing>`.

As the Luca system cannot appropriately protect itself from such attacks, it relies on the {term}`Venue Owner` to make sure that printed QR codes in their venue are not physically replaced by an attacker.

### Direct Communication of {term}`Guest App` and {term}`Luca Server`

In contrast to the {ref}`conventional Check-In process<process:guest_checkin>`, the {term}`Guest App` actively uploads its {term}`Check-In` data to the {term}`Luca Server`.
This might allow the association of user-specific meta-data (e.g. their IP address) and the {term}`Check-In`'s {term}`trace ID` by the {term}`Luca Server` (directly contradicting security objective {ref}`O2 <objective:checkin>`).
As mobile phone networks typically use NAT, the fact that the {term}`Luca Server` does not log any IP addresses and the request being unauthenticated, we do accept this risk.
