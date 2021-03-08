(process:additional_data)=
# Additional Check-In Data

_luca_ provides the functionality to associate a {term}`Check-In` with additional data.
This can be done by either the {term}`Guest App` or by the {term}`Scanner Frontend`.
Additional data is designed to be non-sensitive data that can be used to narrow down possible contact persons among all guests of a venue.
For instance, this might be the table number a {term}`Guest` was placed at in a restaurant.
Regardless of which app creates the {term}`Check-In`, the additional data is encrypted using the {term}`venue keypair` before being uploaded.
