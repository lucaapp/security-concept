# Assets

```{glossary}
Check-In

    The central artifact that enables the {term}`Health Department` to contact {term}`Traced Guest`s.
    It is created with each {ref}`check-in process<process:guest_checkin>` and encodes the information that a Guest is located at a specific location at a specific time.
    However, the information which Guest the Check-In belongs to (specifically, their {term}`Contact Data`) is only made available to the Health Department during {ref}`process:tracing` and is never available to any other actor in the system.

    Each Check-In contains the following information:
     * the venue where the Check-In was created
     * the check-in time
     * the check-out time
     * a {term}`trace ID` that can be connected to an {term}`Infected Guest` during contact tracing
     * the encrypted {term}`contact data reference` that can be used by the Health Department to contact {term}`Traced Guest`s

Check-In History

    A collection of multiple {term}`Check-In`s that all belong to the same Guest.
    This asset is only made availabe to the {term}`Health Department` when an {term}`Infected Guest` decides to share it with the Health Department to aid in {ref}`process:tracing`.
    It allows the Health Department to reconstruct all venues the Guest has visited during the epidemiologically relevant timespan.

Contact Data

    The personal contact data that is entered by the Guest into the Guest App upon registration.
    It contains the following information[^ifsg]:
     * first and last name
     * full address (street, street number, city, postal code)
     * phone number
     * email address

Health Department Information

    The meta data collected by the {term}`Luca Server` about a Health Department during {ref}`process:health_department_registration`.
    The following information is stored:
     * name of the Health Department
     * for each configured employee:
       * first and last name
       * email address
       * phone number (if provided)

Venue Information

    The meta data about a venue.
    The following information is stored:
     * name of the venue
     * name, email address and phone number contact person for this venue
     * full address of the venue
     * geo-coordinates of the venue
     * configured Check-In radius
     * configured number of tables

Scanner Information

    The meta data of a QR code scanner tied to a venue.
    {term}`Venue Owner`s can create any number of unique scanners for their venue.
    The {term}`Luca Server` maintains the following information for each scanner:
    * {term}`scanner ID`
    * {term}`venue ID`
    * a plaintext name of the scanner
    * the public key of the {term}`venue keypair`
```

[^ifsg]: _luca_ is required to collect this information in order to comply with the German [Infektionsschutzgesetz](https://www.gesetze-im-internet.de/ifsg/index.html) law and all federal states' implementations of the law.
