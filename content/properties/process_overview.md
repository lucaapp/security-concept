# Overview of Processes

_luca's_ primary goal is to automate the identification of contact persons for venues, restaurants and locations and ease the {term}`Health Department`'s identification of possible contact persons of infected persons.

The table below provides a high-level overview of the involved processes to achieve this goal.
The chapters in this part explain each process in detail.

``````{list-table}
:header-rows: 1
:widths: 1 2
:name: Core Processes

* - Process Name
  - Purpose
* - {ref}`process:guest_registration`
  - Set up a smartphone to use the {term}`Guest App` in order to check-in at venues using _luca_.
* - {ref}`process:venue_registration`
  - Register an event or a venue with the Luca system and enable it to check-in Guests via _luca_.
* - {ref}`process:health_department_registration`
  - Onboard a {term}`Health Department` to the Luca system.
* - {ref}`process:daily_key_rotation`
  - Regular rotation of the {term}`daily keypair`.
* - {ref}`process:guest_checkin`
  - Transmit encrypted contact information to the {term}`Health Department` so it can be used for {ref}`process:tracing`.
* - {ref}`process:tracing`
  - Retrieve a {term}`Traced Guest`'s {term}`Contact Data` in case of an infection.
* - {ref}`badge:static_badge_gen`, {ref}`badge:personalization`, {ref}`badge:check_in`
  - Set up a Static QR code {term}`Badge`, personalize it with the {term}`Contact Data` of its owner and use it to check-in at venues without using a smartphone.
``````
