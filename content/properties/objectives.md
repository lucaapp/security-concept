(objectives)=
# Security Objectives

_luca_ provides the following guarantees to the respective actors in the system:

% this useless headline is only needed to make the useful headlines less huge
## List of Objectives

(objective:contact_data)=
### O1. An Uninfected Guest's Contact Data is known only to their Guest App

The Guest's personal data is undisclosed as long as they didn't test positive (and become an {term}`Infected Guest`) or show up in a tracing process by a {term}`Health Department` (and become a {term}`Traced Guest`).

(objective:checkin)=
### O2. An Uninfected Guest's Check-Ins cannot be associated to the Guest

Individual {term}`Check-In`s of an {term}`Uninfected Guest` are not disclosed. Only when a Check-In shows up in a tracing process (making the Guest a {term}`Traced Guest`), is this particular Check-In disclosed to the {term}`Health Department`.

Naturally, the Guest App itself may have knowledge about the Check-Ins.

(objective:checkin_history)=
### O3. An Uninfected or Traced Guest's Check-Ins cannot be associated to each other

The entire {term}`Check-In History` of a Guest is disclosed to the {term}`Health Department` if, and only if, the Guest tested positive and explicitly consents to the tracing (making them an {term}`Infected Guest`). Thus, not even an anonymous {term}`Check-In History` can be generated.

Note that the Guest App may keep a local history of Check-Ins.

(objective:guest_consent)=
### O4. An Infected Guest's Check-In History is disclosed to the Health Department only after their consent

Even if a Guest tested positive and is in contact with the {term}`Health Department`, they can decide not to share their {term}`Check-In History`.

(objective:partial_history)=
### O5. The Health Department learns only the relevant part of the Infected Guest's Check-In History

The {term}`Health Department` only learns the epidemiologically relevant part of a Guest's {term}`Check-In History`.

(objective:venue_consent)=
### O6. Traced Guest's Contact Data is disclosed to the Health Department only after Venue Owners' consent

This requirement is meant to mitigate illicit disclosure of arbitrary Guests' contact information by the authorities.
