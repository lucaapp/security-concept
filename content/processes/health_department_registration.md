(process:health_department_registration)=
# Health Department Registration

_luca_ helps {term}`Health Department`s to trace contact persons and identify infection clusters.
In order to participate in the system Health Departments need to be registered and onboarded first.

## Overview

```{panels}
Participants
^^^
* {term}`Luca Server`
* {term}`Health Department`
* {term}`Health Department Frontend`

---

Assets
^^^
* {term}`Health Department Information`

---

Preconditions
^^^
* the {term}`Health Department` is not onboarded

---

Postconditions
^^^
* the {term}`Health Department` has received a login certificate from the {term}`Luca Service Operator` (out-of-band)
* an admin user for the {term}`Health Department` has been registered
* the {term}`Health Department Information` is stored on the {term}`Luca Server`
* the Health Department's {term}`HDEKP` and {term}`HDSKP`'s public keys are stored on the {term}`Luca Server`; the private keys are stored locally at the Health Department
* relevant {term}`daily keypair`s have been re-encrypted by an existing Health Department
```

## Secrets

The following {ref}`secrets <secrets>` are involved in this process:

``````{list-table}
:header-rows: 1
:widths: 1 2 2
:name: Health Department Registration Secrets

* - Secret
  - Use / Purpose
  - Location
* - {term}`HDEKP`
  - Encrypt/decrypt the {term}`daily keypair`.
  - The private key is stored locally on the device that runs the {term}`Health Department Frontend`.
    The public key is stored on the {term}`Luca Server`.
* - {term}`HDSKP`
  - Sign the {term}`daily keypair` during {ref}`process:daily_key_rotation`.
  - The private key is stored locally on the device that runs the {term}`Health Department Frontend`.
    The public key is stored on the {term}`Luca Server`.
* - {term}`Health Department Certificate`
  - Authenticate to the {term}`Health Department Frontend`.
  - Stored locally on devices that run the {term}`Health Department Frontend`.
``````

## Process

In order to be onboarded to _luca_ the {term}`Health Department` contacts the {term}`Luca Service Operator`.
From them the Health Department receives the {term}`Health Department Certificate`.
The Luca Service Operator also helps to provide the {term}`Health Department Information` to the {term}`Luca Server` and to set up an admin user account for one of the Health Department's employees.
The admin user can now access the {term}`Health Department Frontend` using the certificate and the credentials for their user account.

When the admin user logs in for the first time the {term}`Health Department Frontend` automatically generates two keypairs: the {term}`HDEKP` and the {term}`HDSKP`.
These keypairs are required for the {ref}`Daily Key Rotation Process<process:daily_key_rotation>`.
Please refer to that chapter for more details about the keypairs' usage.
Both keypairs' public keys are uploaded to the {term}`Luca Server`.
Their private keys are stored locally.

### Re-Encryption of the Daily Keypair

In the final step of the onboarding process all recent (epidemiologically relevant) {term}`daily keypair`s need to be re-encrypted for the new {term}`Health Department`.
This is necessary in order for the new Health Department to be able to decrypt existing {term}`daily keypair`s with its {term}`HDEKP`.
The re-encryption process is triggered automatically and carried out by any other Health Department that is currently logged in to the {term}`Health Department Frontend` as follows:
* fetch all Health Departments' {term}`HDEKP` public keys (including the new Health Department's recently created key)
* download all relevant {term}`daily keypair`s
* decrypt them using its own {term}`HDEKP`'s private key
* encrypt them for all other Health Departments' {term}`HDEKP`s
* upload them back to the {term}`Luca Server`

This process is very similar to the {ref}`rotation of the daily keypair<process:daily_key_rotation>`.
Please refer to that chapter for further details.

### Adding Further (Non-Admin) Employees

The admin user can create further user accounts that do not have administrative access in the {term}`Health Department Frontend`.
Like the admin user, those users can authenticate to the Health Department Frontend using their individual credentials and the {term}`Health Department Certificate` and use it for contact tracing.
