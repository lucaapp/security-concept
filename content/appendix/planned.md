(appendix:planned)=
# Planned Improvements

_luca_ is under continuous development.
This appendix collects improvements we are currently working on.

(appendix:planned:hdekp_hdskp)=
## Certification of Health Department Keypairs

The two keypairs of each {term}`Health Department`, the Health Department Signing Keypair {term}`HDSKP` and the Health Department Encryption Keypair {term}`HDEKP`, play a crucial role in the _luca_ system.
As described in the chapter {ref}`process:daily_key` the {term}`HDSKP` is used to sign the {term}`daily keypair`.
This signature is verified by the {term}`Guest App` during {ref}`check-in<process:guest_checkin>`.
The {term}`HDEKP` also plays an important role in the process of {ref}`Daily Public Key Rotation<process:daily_key>`: the new {term}`daily keypair` is made accessible to all {term}`Health Department`'s {term}`HDEKP`s registered in _luca_.
Consequently, the authenticity of these two keypairs is of great importance.

During the pilot phase _luca_ did not rely on a third party PKI to ensure the authenticity of those public keys.
Hence, {term}`Guest App`s and {term}`Health Department`s currently need to rely on the {term}`Luca Server` and {term}`Luca Service Operator` to ensure the authenticity of the keypairs.

With the country-wide rollout of _luca_ the {term}`HDSKP` and {term}`HDEKP` public keys will be signed by certificates issued by Bundesdruckerei's subsidiary company [D-Trust GmbH](https://d-trust.net).
Those certificates will be based on one of D-Trust's global root certificates, provide revocation mechanisms and will be issued only after manual validation of the requesting Health Department's identity.
Both the {term}`Guest App` and the {term}`Health Department`s will then rely on a chain of trust to ensure the authenticity of {term}`HDSKP` and {term}`HDEKP`.

We will update this document accordingly.
