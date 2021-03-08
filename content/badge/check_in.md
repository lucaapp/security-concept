(badge:check_in)=
# Badge Check-In

In order to check-in with a Static {term}`Badge` the Guest presents the Badge's QR code to the {term}`Scanner Frontend`, the same way they would if they were using the {term}`Guest App`.
However, as the static QR code on the Badge cannot dynamically create {term}`trace ID`s, the {term}`Scanner Frontend` has to assume some of the tasks normally done by the Guest App.

The Scanner Frontend reads following information from the QR code
* `enc_contact_data_ref`
* `badge_keypair_ID`
* `tracing_seed`
* `badge_ephemeral_public_key`
* `attestation_signature`

and uses it to create a {term}`Check-In` as follows:

```{code} python
# pseudocode

# the tracing_seed was transmitted via the scanned QR code
level_two              = HKDF-HMAC-SHA256(tracing_seed, length=48,
                                          context="badge_tracing_assets",
                                          salt="")
user_id                = toUuid4(level_two[0:16])
badge_verification_key = level_two[16:32]
tracing_secret         = level_two[32:48]

# the data created below corresponds directly to the data in the QR code displayed by the Guest App
timestamp        = UNIX timestamp rounded down to the last full minute (little endian encoding)
trace_id         = HMAC-SHA256(user_id || timestamp, tracing_secret)  # truncated to 16 bytes

enc_data         = enc_contact_data_ref  # printed on the QR code
verification_tag = HMAC-SHA256(timestamp || enc_data, badge_verification_key)
```

The rest of the check-in procedure is equivalent to the {ref}`Check-In via the Mobile Scanner App<process:guest_checkin:upload>`.

(badge:check_in:considerations)=
## Security Considerations

A Static {term}`Badge` cannot provide the same security guarantees as the {term}`Guest App`.
During check-in, the {term}`Scanner Frontend` learns the Badge's {term}`tracing secret` and performs tasks that would normally be done by the Guest App.

As the QR code printed on the Badge is immutable and is the only asset required in order to check-in using the Static Badge, the Scanner Frontend now possesses all knowledge required to perform a check-in in the name of the Guest.
Obviously, it also allows the Scanner Frontend to recognize Badges it had previously scanned.
