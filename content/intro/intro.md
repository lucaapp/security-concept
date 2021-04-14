(intro:intro)=
# Introduction

## About this Document

This document describes the security concepts of the [_luca_](https://luca-app.de) system as well as the processes and cryptographic functions in technical detail.
It also explains the guarantees _luca_ provides to its users and how these guarantees are accomplished.

Both _luca_ and this document are continuously improved and in active development.
If you discover any issues with the concepts in this document or any mismatch between the document and _luca_'s behaviour, please contact us directly at security@luca-app.de for responsible disclosure.

We greatly appreciate your feedback.

## Contributors

This document is owned by culture4life GmbH, which is also responsible for the development of _luca_.
It is continuously developed and reviewed in cooperation with security experts and partners such as neXenio GmbH.

## Guarantees Provided by _luca_

_luca_'s main goal is to protect guests' personal data.
The technical description of the guarantees _luca_ aims to provide to its users can be found in the chapter {ref}`objectives`.

In contrast to the paper-based approach to collecting contact data at restaurants and other public venues, _luca_ is designed to prevent the venue's staff, _luca_ itself and other 3rd parties from accessing this data.
Public health authorities (i.e. "Gesundheitsämter") are the only entity that can access the relevant personal data of guests to conduct contact tracing of users who have been potentially exposed to SARS-CoV2.
Similar to the traditional paper-based contact data collection, the health authorities need the venue owner's consent to access this information.

_luca_ aims to underpin all {ref}`security and data protection objectives and guarantees <objectives>` with cryptographic protocols wherever feasible.
This document describes the current implementation status of the _luca_ system and provides security considerations where some aspects of these guarantees are not yet fully met.

Please also note the {ref}`planned improvements<appendix:planned>`.

## Overview

The remainder of this document is divided into six sections.
The first section, "System Overview", explains the important components, assets, security objectives and cryptographic secrets in the system.
Section two describes how different actors are onboarded and registered in the system.
Sections three and four describe the parts of the system most visible to our users: the various ways users can check-in at _luca_ venues.
Finally, the section "Contact Tracing" describes how public health authorities can use _luca_ to identify chains of infection with the explicit consent of _luca_ venues.
The appendix contains technical details about the cryptography used in _luca_ and improvements scheduled for the near future.
