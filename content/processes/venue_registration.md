(process:venue_registration)=
# Venue Registration

Professional {term}`Venue Owner`s can register their venue with the _luca_ system via a web application.
The venue can then be managed via a web interface in order to set up individual {term}`Scanner Frontend`s and to configure other venue-specific parameters (for example auto checkout behavior).

## Overview

```{panels}
Participants
^^^
* {term}`Luca Server`
* {term}`Venue Owner`
* {term}`Venue Owner Frontend`

---

Assets
^^^
* {term}`Venue Information`

---

Preconditions
^^^
* the venue is not registered

---

Postconditions
^^^
* the {term}`venue keypair` is available locally to the {term}`Venue Owner Frontend`
* the {term}`Venue Information` is stored on the {term}`Luca Server`
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 2
:name: Venue Registration Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`venue keypair`
  - Encrypt the {term}`contact data reference` of Guests during {ref}`check-in<process:guest_checkin>` and decrypt it during {ref}`process:tracing`.
  - Both the public and private key are stored locally by the {term}`Venue Owner Frontend`.
    The public key is shared with {term}`Scanner Frontend`s when they are set up.
``````

## Process

To initiate the process the {term}`Venue Owner` registers with their email address and a password.
They enter further information, such as the name of the venue and their contact information in the {term}`Venue Owner Frontend` (see {term}`Venue Information` for the complete list of the data collected).

Subsequently, the Venue Owner Frontend generates the {term}`venue keypair`.
Both the public and private key are stored locally.
The keypair's public key is used to set up new {term}`Scanner Frontend`s, which utilize it to encrypt Guests' {term}`contact data reference` during {ref}`process:guest_checkin`.
The keypair's private key is needed by the Venue Owner Frontend in order to lift this encryption when assisting a {term}`Health Department` in the process of {ref}`process:tracing`.

## Security Considerations

(process:venue_registration:considerations)=
### Authenticity of the Venue Keypair's Public Key

As the {term}`Venue Owner` holds no certificate with which they could sign the public key of the {term}`venue keypair` there is no secure way to validate its authenticity when it is used in the check-in process.
This affects both the {ref}`process:guest_checkin` and the {ref}`process:guest_self_checkin`.

It is therefore important that the public key is transmitted to the {term}`Scanner Frontend` on a secure out-of-band channel (specifically, not the {term}`Luca Server`).

Prospectively, this will be implemented by attaching the {term}`venue keypair`'s public key to the fragment component of the link to the {term}`Scanner Frontend`, which is created in the {term}`Venue Owner Frontend`.
For printed QR codes for self Check-In the public key will be part of the QR code.

Note that the impact of this only affects the outer layer of the {term}`contact data reference`'s encryption.
It is still encrypted with the {term}`daily keypair` and thus only accessible for the {term}`Health Department`.

### Sensitivity of the Venue Keypair

The {term}`venue keypair`'s private key must not be lost or made accessible to third parties.
Hence, organizational measures are taken to specifically inform the {term}`Venue Owner` that special care must be taken when dealing with this key.
