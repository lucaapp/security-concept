(intro:landing)=
# _luca_ Security Overview

**_luca_ Sicherheitsübersicht**

_luca_ unterstützt Veranstaltungs- und Restaurantbetreiber:innen bei der verpflichtenden Aufnahme der personenbezogenen Daten ihrer Gäste im Rahmen der Bekämpfung der Covid-19-Pandemie.
Dabei legt _luca_ besonderen Wert auf den Schutz dieser Daten: Die Daten können weder von Betreiber:innen, noch vom _luca_-System gelesen werden, sondern nur von den Gesundheitsämtern, in dem Falle dass eine Kontaktnachverfolgung wegen einer bestätigten Infektion eines Gastes notwendig wird.

Nutzer:innen von _luca_ erzeugen beim Zutritt so genannte verschlüsselte Check-Ins mit ihrem Smartphone oder einem Schlüsselanhänger.
Grundidee ist, dass die personenbezogenen Daten dabei von der _luca_-App der Nutzer:in mit einem Gesundheitsamt-Schlüssel verschlüsselt und im Rahmen des Check-Ins an der Betreiber:in geschickt werden.
Die Betreiber:in verschlüsselt diese verschlüsselten Daten erneut und sendet sie, zusammen mit der Check-In-Zeit, an das _luca_-System.
Hierdurch kann weder die Betreiber:in, noch das _luca_-System oder die Gesundheitsämter die personenbezogenen Daten der Nutzer:innen lesen.

Wird bei einer Nutzerin eine Infektion mit SARS-CoV2 festgestellt, sendet die _luca_-App der Infizierten alle Check-In-Zeiten zusammen mit der ID der Betreiber:innen an das _luca_-System.
_luca_ fordert von allen diesen Betreiber:innen eine Entschlüsselung der Daten der Gäste an, die sich in der betreffenden Zeit ebenfalls eingecheckt haben, d.h. _luca_ erhält die mit dem Schlüssel des Gesundheitsamtes verschlüsselten Daten der Nutzer:innen.
Diese Daten werden dann von _luca_ an das zuständige Gesundheitsamt übermittelt, das hieraus die Daten entschlüsseln und damit die Nutzer:innen kontaktieren kann.

**_luca_ Security Overview**

Due to the Covid-19 pandemic, restaurants, event venues and other public locations are required by law to collect the contact information of their guests.
_luca_ aims to simplify this process while putting an emphasis on personal data protection.
Once a user tests positive for SARS-CoV2, only the public health authorities can access the end-user's personal data to conduct epidemiological contact tracing.
Neither the owners of event venues nor the _luca_ server can access the end-user's data at any time.

Upon entering a _luca_-enabled venue, a user creates a so-called "encrypted Check-In" using either their smartphone or a simple key fob.
This Check-In is encrypted in a way that only the public health authorities can read it.
The encrypted Check-In is then encoded as a QR code, scanned by the venue owner's software and encrypted once again so that nobody can access the user's personal information at this stage.
Now, the venue owner sends this double-encrypted Check-In to the _luca_ server along with a time stamp.

In case a _luca_ user tests positive for SARS-CoV2, the app sends the infected user's epidemiologically relevant check-ins along with the IDs of the affected venues to the _luca_ server.
_luca_ then requests these venue owners to decrypt and upload the Check-In records of every user who visited their venue at the same time as the infected person.
Note that all contact information is still encrypted by the public health authorities' key and readable by neither _luca_ nor the venue owner.
Once the public health authorities receive these Check-Ins, they can decrypt the data and contact _luca_ users who might have been exposed to SARS-CoV2.