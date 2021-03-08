(process:guest_checkout)=
# Guest Checkout

For effective {ref}`contact tracing <process:tracing>` the {term}`Health Department`s must know in what time frame an {term}`Infected Guest` was present at any given location.
Hence, {term}`Guest`s must check-out of locations when they leave.

## Overview

```{panels}
Participants
^^^
* {term}`Guest`
* {term}`Guest App`
* {term}`Venue Owner`
* {term}`Venue Owner Frontend`
* {term}`Luca Server`

---

Assets
^^^
* {term}`Check-In`

---

Preconditions
^^^
* the {term}`Guest` recently created a {term}`Check-In` at some venue

---

Postconditions
^^^
* the {term}`Guest`'s {term}`Check-In` has a specific time period of stay
```

## Secrets

This process requires no cryptographic secrets.

## Checkout Process

Individual {term}`Check-In`s are identified by their {term}`trace ID` that is generated during the Check-In process (via the Guest App and {ref}`a QR code scanner <process:guest_checkin>`, {ref}`scanning a printed QR code <process:guest_self_checkin>` or a {ref}`static badge and QR code scanner <badge:check_in>` [^checkout_badges]).

[^checkout_badges]: Currently, there is no way for a {term}`Guest` that uses a {term}`Badge` instead of the {term}`Guest App` to perform a manual checkout. See also {ref}`process:guest_checkout:security:inaccurate_checkout`. _luca_ might implement such feature in the future.

For a checkout of some previous {term}`Check-In`, the respective {term}`trace ID` and the current timestamp are sent to the {term}`Luca Server`.
No further authentication or validation is performed and the {term}`Check-In` is annotated with the provided timestamp.

The actual checkout might be performed in one of the following ways:

### Manual App Check-out

After a {term}`Guest` checked in using the {term}`Guest App` they are presented with a "Check out" button for the currently active {term}`Check-In`.
Upon user request the {term}`Guest App` informs the {term}`Luca Server` as described above and terminates the {term}`Check-In`.
The {term}`Guest` may now perform another {term}`Check-In` at some other location.

### Automatic Check-out via a Geofence around the Current Venue

For an automatic checkout the {term}`Venue Owner` must provide their venue's geo location and a "Check-In radius" (geo-fence) in the {term}`Venue Information` during {ref}`initial venue registration <process:venue_registration>`.
Once the {term}`Guest` physically leaves the venue's radius, the mobile operating system will inform the {term}`Guest App` which performs the checkout automatically.

### Manual Venue Owner Check-out

{term}`Venue Owner`s can checkout all active {term}`Check-In`s for their venue via the {term}`Venue Owner Frontend`.
In that case, the {term}`Venue Owner Frontend` informs the {term}`Luca Server` about the {term}`Venue Owner`'s wish to end active {term}`Check-In`s at their venue.
For instance, restaurants might use this to end all remaining active {term}`Check-In`s after they close down for the day.

### Time-based Check-out after 24 hours

Regardless of the checkout mechanisms described above, any {term}`Check-In` is automatically checked out after 24 hours by the {term}`Luca Server`.

## Security Considerations

(process:guest_checkout:security:inaccurate_checkout)=
### Inaccurate or Tampered Checkout Times

Checkouts must use the {term}`trace ID` to reference their respective {term}`Check-In` to the {term}`Luca Server`.
As the {term}`trace ID` is {ref}`designed to be anonymous <process:guest_checkin:security:trace_id>`, _luca_ cannot give any authenticity guarantees regarding the stored checkout time.
Any implementation trade-offs to extend _luca's_ guarantees for the checkout time would have had an influence on security objectives {ref}`O2 <objective:checkin>` and {ref}`O3 <objective:checkin_history>`.

It is worth noting that a {term}`Health Department` usually does not blindly follow Luca's data records when identifying likely contact persons of an {term}`Infected Guest`, but draws educated real-world conclusions from them.
Therefore, any checkout times are merely seen as a hint for real-world {ref}`contact tracing <process:tracing>` activities by a {term}`Health Department`.

### Usage of Geo-Location Data by the Operating System

The above-described geo fence is implemented locally so the {term}`Guest`'s location is never stored or sent to the {term}`Luca Server`.
Additionally, the {term}`Guest` must consent to the usage of location services by the {term}`Guest App` to use this feature.
If they deny consent, they can still use _luca_ but will need to always remember to checkout manually.
