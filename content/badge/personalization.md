(badge:personalization)=
# Badge Personalization

After the {term}`Badge` has been created {ref}`as described above<badge:static_badge_gen>`, it contains an encrypted contact data reference (`enc_contact_data_ref`).
This reference is conceptually very similar to the {term}`contact data reference` used by the {term}`Guest App`.
However, at this point there is no contact data associated to the reference, yet.
Guests need to personalize their {term}`Badge` using the {term}`Badge Personalization Frontend`.

## Overview

```{panels}
Participants
^^^
* {term}`Guest`
* {term}`Luca Server`

---

Components/Assets
^^^
* {term}`Badge`
* {term}`Contact Data`

---

Preconditions
^^^
* there is a {term}`Guest` that is willing to use a {term}`Badge` for {term}`Check-In`s
* the {term}`Guest` has received their {term}`Badge`
* the {term}`Badge`s was generated as described in {ref}`badge:static_badge_gen`

---

Postconditions
^^^
* some {term}`Guest` has personalized their {term}`Badge` with their {term}`Contact Data` via the {term}`Badge Personalization Frontend`
```

## Process

The {term}`Badge Personalization Frontend` requires the {term}`badge serial number` and the Guest's {term}`Contact Data`.
It creates the {term}`encrypted guest data` as follows:

```{code} python
# pseudocode

# derive the initial keying material from the serial number
seed = argon2id(entropy, salt="da3ae5ecd280924e",
                length=16, memorySize=32MiB, iterations=11, parallelism=1)

# derive secrets analogously to the Badge Generation process
level_one     = HKDF-HMAC-SHA256(seed, length=64,
                                 context="badge_crypto_assets",
                                 salt="")
data_secret   = level_one[0:16]
tracing_seed  = level_one[16:32]
guest_keypair = level_one[32:64]

level_two = HKDF-HMAC-SHA256(tracing_seed, length=48,
                             context="badge_tracing_assets",
                             salt="")

user_id                = toUuid4(level_two[0:16])
badge_verification_key = level_two[16:32]
# tracing_secret is not required in this process

# derive the symmetric encryption key from the data secret
# this key directly corresponds to the data_encryption_key used by the Guest App
data_encryption_key = SHA256(data secret || 0x01) # truncated to 16 bytes

# encrypt contact_data and badge_verification_key analogously to how the Guest
# App creates the encrypted_guest_data
# the badge_verification_key corresponds to the data_authentication_key

iv = random_bytes(16)

encrypted_guest_data = AES_128(contact_data + badge_verification_key,
                               key=data_encryption_key,
                               mode=CTR,
                               iv=iv)

badge_data_mac = HMAC(encrypted_guest_data,
                      key=badge_verification_key)

badge_data_signature = guest_keypair.private.sign(encrypted_guest_data +
                                                  badge_verification_key +
                                                  iv)

```

The {term}`Badge Personalization Frontend` sends the following data to the {term}`Luca Server`:
* the {term}`encrypted guest data`
* the `IV` used in the encryption
* the `badge data mac`
* the `badge data signature`

The {term}`Luca Server` verifies that the request is authorized by checking the provided signature with public key that was uploaded when the {ref}`Badge was generated<badge:static_badge_gen>`.

