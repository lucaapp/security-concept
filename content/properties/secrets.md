(secrets)=
# Secrets and Identifiers

(secrets:secrets)=
## System-wide List of Secrets

``````{glossary}
daily keypair

    The keypair whose public key is used by the {term}`Guest App` to encrypt the secret part of the {term}`Check-In` data.
    It's private key is used by a {term}`Health Department` during the process of {ref}`Contact Tracing<process:tracing>`.

    The keypair's public key is signed using the {term}`HDSKP` and stored on the {term}`Luca Server`.
    Its private key is encrypted for each registered Health Department's {term}`HDEKP`.
    The encrypted private keys are stored on the {term}`Luca Server`.

    The daily keypair's life cycle and usage is detailed in the chapter {ref}`process:daily_key`.

badge keypair
    The keypair that encrypts {term}`contact data reference`s for static {term}`Badge`s.
    The public key is used exclusively by a {term}`Trusted 3rd Party` during {ref}`the generation of static Badges <badge:static_badge_gen>`.
    It's private key is owned by the Health Department and is used to decrypt {term}`Check-In`s created using a static Badge.

badge attestation keypair
    This keypair signs static {term}`Badge`s during {ref}`their generation <badge:static_badge_gen>`.
    Its private key is kept in the {term}`Luca Server` and is used via an authenticated API endpoint by the {term}`Badge Generator`.
    The {term}`Scanner Frontend` uses the public key to verify that a presented {term}`Badge` is valid and registered with the {term}`Luca Server`.

data secret

    A secret cryptographic seed which is used to derive both the {term}`data encryption key` and the {term}`data authentication key`.
    This seed is encrypted twice before being sent to the {term}`Luca Server` during {ref}`Check-In <process:guest_checkin:scanner_checkin>` and ultimately protects the Guest's {term}`Contact Data`.
    It is stored locally in the {term}`Guest App`.

data encryption key

    A symmetric key derived from the {term}`data secret`, used to encrypt the {term}`Contact Data`.

data authentication key

    A symmetric key derived from the {term}`data secret` during {ref}`process:guest_registration`.
    It is used to authenticate the Guest's {term}`Contact Data` and {term}`Check-In`s.
    The {term}`data authentication key` is stored encrypted on the {term}`Luca Server` as a part of the {term}`encrypted guest data`.

guest keypair

    An asymmetric keypair created during the {ref}`process:guest_registration`.

    The keypair's private key is used to sign the {term}`encrypted guest data` and {term}`guest data transfer object`.
    The public key is uploaded to the {term}`Luca Server`.

HDEKP

    The "Health Department Encryption Keypair" is used to encrypt the {term}`daily keypair`'s private key.
    Each Health Department has their own HDEKP.

    The public of this keypair is signed using the {term}`HDSKP` and stored on the Luca Server.
    The private key is stored locally at the Health Department.

HDSKP

    The "Health Department Signing Keypair" is used to authenticate the {term}`HDEKP`.
    Each Health Department has their own HDSKP.

Health Department Certificate

    A certificate that identifies a {term}`Health Department`.
    It is used to authenticate to the {term}`Health Department Frontend`.

    This certificate is created in a manual process by the {term}`Luca Service Operator` and signed by an external, trusted Certificate Authority.

tracing secret

    A randomly generated seed used to derive {term}`trace ID`s when {ref}`checking in using the Guest App<process:guest_checkin>`.
    It is stored locally on the {term}`Guest App` until it is shared with the {term}`Health Department` during {ref}`contact tracing<process:tracing>`.
    Moreover, the tracing secret is rotated on a regular basis in order to limit the number of {term}`trace ID`s that can be reconstruced when the secret is shared.

tracing TAN

    The tracing TAN (Transaction Authentication Number) is a human readable code that is used during the process of {ref}`Contact Tracing <process:tracing>`.
    By requesting a TAN from the {term}`Luca Server` and communicating it to the {term}`Health Department` an {term}`Infected Guest` grants the Health Department access to their {term}`Contact Data`.

    ```{note}
    This TAN is not to be confused with the {term}`verification TAN`, which is involved in the {ref}`process:guest_registration` process to verify the Guest's phone number.
    ```

venue keypair

    An asymmetric keypair generated locally in the {term}`Venue Owner Frontend` upon {ref}`process:venue_registration`.
    The keypair's public key is used by the {term}`Scanner Frontend` to add the outer layer of encryption to the {term}`contact data reference` (which is already encrypted for the {term}`daily keypair`) during {ref}`Guest Check-In<process:guest_checkin>`.
    Its private key is stored locally.

verification TAN

    The verification TAN (Transaction Authentication Number) is a human readable code that is used to verify the Guest's phone number during {ref}`process:guest_registration`.

badge serial number
    The 12-digit serial number that is printed on the flip-side of each {term}`Badge`.
    A 56-bit random number that acts as a seed to derive all secrets associated with the {term}`Badge` and encoded into the {term}`Badge`'s QR code.
``````

## Glossary

```{glossary}
user ID

    A unique identifier for the Guest in the Luca system.
    It indexes the {term}`encrypted guest data` and is also used to derive {term}`trace ID`s during {ref}`Guest Check-In<process:guest_checkin>`.

trace ID

    An opaque identifier derived from a Guest's {term}`user ID` and {term}`tracing secret` during {ref}`Guest Check-In<process:guest_checkin>`.
    It is used to identify {term}`Check-In`s by an {term}`Infected Guest` after that Guest shared their {term}`tracing secret` with the {term}`Health Department`.

venue ID

    An unique identifier for a venue registered in the Luca system.
    The venue ID is linked to the {term}`Venue Information` stored by the {term}`Luca Server`.

scanner ID

    An unique identifier for an instance of a {term}`Scanner Information` associated with a specific venue.
    Given the scanner ID the {term}`Scanner Frontend` can start performing {term}`Check-In`s for the associated venue.

daily keypair ID

    An identifier for the {term}`daily keypair`.

verification tag

    A tag used to verify the authenticity of the {term}`contact data reference`.

encrypted guest data

    This object contains the {term}`Contact Data` and {term}`data authentication key`.
    It is encrypted with the {term}`data encryption key`, signed with the {term}`guest keypair` and uploaded to the {term}`Luca Server` during {ref}`process:guest_registration`.

guest data transfer object

    This object contains an {term}`Infected Guest`'s {term}`tracing secret`s, {term}`user ID` and {term}`data secret`.
    During {ref}`process:tracing` the {term}`Guest App` encrypts the {term}`guest data transfer object` for the {term}`daily keypair` and shares it (via the {term}`Luca Server`) with the {term}`Health Department`.

contact data reference

    The {term}`contact data reference` combines the {term}`user ID`, the {term}`data secret` and a {term}`verification tag`.
    Encrypted with both the {term}`daily keypair` and the {term}`venue keypair` it is included in each {term}`Check-In` during {ref}`Guest Check-In<process:guest_checkin>`.
```
