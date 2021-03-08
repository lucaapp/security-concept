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

# Actors and Components

(actors:actors)=
## Actors

```{glossary}
Guest

    A person that is required to securely provide their {term}`Contact Data` to the Luca system before entering a venue and later (on infection) submit their location history ({term}`Check-In History`) to the {term}`Health Department`.

    Technically the Guest can be in one of three roles: {term}`Uninfected Guest`, {term}`Traced Guest` or {term}`Infected Guest`.
    Depending on their role, the security guarantees provided for the Guest change.
    For example, no component in the system other than the {term}`Guest App` will ever learn an {term}`Uninfected Guest`'s {term}`Contact Data`.
    In contrast, the {term}`Contact Data` of {term}`Traced Guest`s is made available to the {term}`Health Department`.

Uninfected Guest

    The default role of a Guest.
    Neither the {term}`Check-In History` nor {term}`Contact Data` has been shared with the {term}`Health Department`.

Traced Guest

    A Guest who is part of a {ref}`Contact Tracing Process<process:tracing>`.
    This Guest's {term}`Contact Data` is revealed to the {term}`Health Department`.

Infected Guest

    A Guest who is suspected of being infected with Sars-CoV2 and has consented to sharing their {term}`Check-In History` with the {term}`Health Department`.

Health Department

    A local Health Department responsible for identification of contact persons.
    This term is used synonymously for an employee that represents this Health Department.

Venue Owner

    A private person or business owner/manager of a venue that has Guests and uses _luca_ to trace contact information.

Scanner Operator

    The person who operates the {term}`Scanner Frontend` at a venue.

Luca Service Operator

    culture4life GmbH as the creator and operator of the Luca system as a whole, their backend services, phone and web applications.
    The Luca Service Operator has unrestricted access to the {term}`Luca Server` database.

Trusted 3rd Party

    A person or institution that is not affiliated with _luca_, its developers or operators.
    A trusted 3rd party is required to perform vital initialization steps regarding _luca's_ system setup.
    Note that different mentions of {term}`Trusted 3rd Party` throughout the document can refer to different institutions.

```


(actors:components)=
## Components

```{glossary}
Guest App

    The Luca Guest App is the interface for Guests.
    Guests enter their {term}`Contact Data` in the app and use the app to check-in at several locations without re-entering their contact details.

Health Department Frontend

    Enables the {term}`Health Department` to trace infection cases and contact potential contact persons.

Venue Owner Frontend

    The frontend for the managers/organizers of venues/locations/restaurants.
    Here, a professional or private user can create locations or events which will enable them to check-in Guests.

Luca Server

    Stores encrypted {term}`Check-In`s and {term}`Contact Data` and centrally orchestrates the other technical components.
    The Luca Server is never in possession of personal {term}`Contact Data` in plain text.

Scanner Frontend

    A web app that is used by the organizer or their employees to scan the QR codes produced by the {term}`Guest App` to check-in Guests.

Web-Check-In Frontend

    The Web-Check-In frontend enables venues to let Guests enter their information directly on-site on tablet device or something similar.
    This is useful if Guests are not users of the {term}`Guest App`.

Badge Personalization Frontend

    A web application to encrypt and store {term}`Contact Data` for {term}`Guest`'s that are wishing to use a {term}`Badge` to check-in at Luca locations.

Badge Generator

    Generates printable QR codes to be used by people without smartphones to allow check-ins at _luca_ venues.

Badge

    A printable QR code in the form of small badge to allow people without a smartphone to check-in at _luca_ locations.

Email Service Provider

    Used to {term}`Venue Owner`s and {term}`Health Department`s.

SMS Service Provider

    Used to validate a Guest's phone number upon entering {term}`Contact Data` in the {term}`Guest App`.
```

### Component Diagram

```{code-cell} ipython3
:tags: [remove-input]

%%plantuml

@startuml

!include ../../lib/plantuml/C4_Context.puml

HIDE_STEREOTYPE()

System(lucaServer, "Luca Server")

System(venueOwnerFE, "Venue Owner Frontend")
System(scannerFE, "Scanner Frontend")
Person(venueOwner, "Venue Owner")
Person(scannerOp, "Scanner Operator")

System(hdFE, "Health Department Frontend")
Person(hdEmpl, "Health Department Employee")

System(guestApp, "Guest App")
System(webCheckinFE, "Web-Check-In Frontend")

Person(guest, "Guest")

System(badgePersFE, "Badge Personalization Frontend")

System_Ext(badgeGen, "Badge Generator")
System_Ext(emailService, "Email Service Provider")
System_Ext(smsService, "SMS Service Provider")

BiRel_U(lucaServer, venueOwnerFE, " ")
BiRel_U(lucaServer, scannerFE, " ")
Rel_D(venueOwner, venueOwnerFE, " ")
Rel_D(scannerOp, scannerFE, " ")

BiRel_U(lucaServer, guestApp, " ")
BiRel_U(lucaServer, webCheckinFE, " ")
BiRel_U(lucaServer, badgePersFE, " ")

Rel_D(guest, guestApp, " ")
Rel_D(guest, webCheckinFE, " ")
Rel_D(guest, badgePersFE, " ")

BiRel_R(lucaServer, hdFE, " ")
Rel_L(hdEmpl, hdFE, " ")

Rel_D(lucaServer, emailService, " ")
Rel_D(lucaServer, smsService, " ")
Rel_D(badgeGen, lucaServer, " ")
Lay_R(emailService, smsService)
Lay_R(smsService, badgeGen)

SHOW_DYNAMIC_LEGEND()
@enduml
```
