# FGS-SVK-PERSONAL

**Svenska kyrkans anpassning av FGS Personal — elementkatalog för löneinformation**

| | |
|---|---|
| Version | 1.0 |
| Datum | [Åååå-mm-dd] |
| Baseras på | FGS Personal RAFGS2V1.0, Riksarkivet, februari 2019; EAC-CPF 2010 |
| Utfärdare | Svenska kyrkan |
| Kontakt | [e-post] |

---

## Innehåll

- 1 [Inledning](#1-inledning)
- 2 [Specifikationer](#2-specifikationer)
  - 2.1 [XML-filer i arkivpaketet](#21-xml-filer-i-arkivpaketet)
  - 2.2 [Scheman](#22-scheman)
  - 2.3 [Datatyper](#23-datatyper)
  - 2.4 [Läsanvisning](#24-läsanvisning)
- 3 [Dataelement med exempel](#3-dataelement-med-exempel)
  - 3.1 [Gemensamma EAC-CPF-kontrollelement](#31-gemensamma-eac-cpf-kontrollelement)
  - 3.2 [Organisation](#32-organisation)
  - 3.3 [Person](#33-person)
  - 3.4 [Arbetstagare](#34-arbetstagare)
  - 3.5 [Anställning](#35-anställning)
  - 3.6 [Anställningstillägg](#36-anställningstillägg)
  - 3.7 [Lönekörningar](#37-lönekörningar)
  - 3.8 [Lönetransaktioner](#38-lönetransaktioner)
  - 3.9 [Konteringar](#39-konteringar)
  - 3.10 [Referensregister](#310-referensregister)
- [Värdelistor](#värdelistor)

---

## 1. Inledning

Detta dokument är en elementkatalog för Svenska kyrkans anpassning av FGS Personal (RAFGS2V1.0) för arkivering av löneinformation ur Flex Lön. Katalogen förtecknar och beskriver samtliga XML-element som ingår i ett arkivpaket enligt anpassningen, med angivelse av datatyp, kardinalitet, XML-sökväg och exempel.

Katalogen är avsedd som praktisk referens för systemleverantörer och e-arkivadministratörer. Det normativa grunddokumentet är *Svenska kyrkans anpassning av FGS Personal* (`svk-fgs-personal-anpassning.md`), till vilket detta dokument är ett komplement.

Elementnumreringen är löpande och prefixad `SVK-LON:N`. Cross-referenser till EAC-CPF och FGS Personal anges inom parentes.

---

## 2. Specifikationer

### 2.1 XML-filer i arkivpaketet

Varje arkivpaket täcker en arbetsgivare ett uttagsår och innehåller följande XML-filer:

| Fil | Schema | Sektion i katalogen |
|---|---|---|
| `organisation/organisation.xml` | EAC-CPF + FGS Personal | 3.2 |
| `anstallningar/F_<nr>.xml` | EAC-CPF + FGS Personal + SVK-LON | 3.5, 3.6 |
| `arbetstagare/A_<pnr>.xml` | EAC-CPF + FGS Personal | 3.4 |
| `personer/P_<pnr>.xml` | EAC-CPF + FGS Personal | 3.3 |
| `loneutbetalningar/lonekorningar.xml` | SVK-LON | 3.7 |
| `loneutbetalningar/lonetransaktioner.xml` | SVK-LON | 3.8 |
| `loneutbetalningar/konteringar.xml` | SVK-LON | 3.9 |
| `register/utbetalningsgrupper.xml` | SVK-LON | 3.10 |
| `register/formelvariabler.xml` | SVK-LON | 3.10 |
| `register/lonearter.xml` | SVK-LON | 3.10 |
| `lonespecifikationer/*.html` | HTML | — |

### 2.2 Scheman

| Schema | Namnrymd / identifierare | Användning |
|---|---|---|
| EAC-CPF 2010 | `urn:isbn:1-931666-33-4` | Organisation, Person, Arbetstagare, Anställning (basstruktur) |
| FGS Personal RAFGS2V1.0 | Riksarkivets scheman | Utökade element i Anställning (`employmentDescription`) |
| SVK-LON v1 | `https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1` | Tilläggsschemat: anställningstillägg, löneutbetalningar, register |
| SVK-LON Schematron | `svk-personal-lon.sch` | Regelbaserad validering |

### 2.3 Datatyper

| Datatyp | Förklaring |
|---|---|
| string | Teckensträng utan begränsning |
| token | Teckensträng utan inledande/avslutande blanksteg och utan radbrytningar |
| date | Datum enligt ISO 8601: `YYYY-MM-DD` |
| dateTime | Datum och tid: `YYYY-MM-DDTHH:MM:SS` |
| decimal | Decimaltal med punkt som decimaltecken |
| integer | Heltal |
| boolean | `true` eller `false` |
| anyURI | URI-referens (relativ eller absolut) |
| ProcentType | Decimal 0–100 (SVK-LON-definierad begränsning) |
| ValutakodType | Tre versaler enligt ISO 4217, t.ex. `SEK` |

### 2.4 Läsanvisning

Varje element beskrivs med:

- **Elementnummer** på formen `SVK-LON:N`.
- **Elementnamn** i kursiv stil.
- **Referens** till basstandard inom parentes, t.ex. `(EAC-CPF: recordId)` eller `(FGS Personal: employmentId)`. Saknas parentes är elementet definierat enbart i SVK-LON-schemat.
- **Beskrivning** och eventuella anvisningar om obligatorium och upprepning.
- **XML-element** anger elementets namn och, vid behov, urskiljande attribut. Sökvägen anges relativt dokumentets rotelement om inget annat anges.
- **Datatyp** enligt avsnitt 2.3.

Obligatoriska element markeras med "Obligatoriskt." i beskrivningstexten. Element som kan upprepas markeras med "Elementet kan upprepas." Konditionellt obligatoriska element förklaras i sin beskrivning.

---

## 3. Dataelement med exempel

### 3.1 Gemensamma EAC-CPF-kontrollelement

EAC-CPF-dokumenten för Organisation, Person, Arbetstagare och Anställning delar en gemensam kontrollstruktur. Elementen SVK-LON:1–12 förekommer identiskt i alla fyra dokumenttyper. De efterföljande elementlistorna (3.2–3.5) beskriver enbart de dokumentspecifika elementen; kontrollelementen upprepas inte men förutsätts i varje dokument.

---

#### SVK-LON:1 - *EAC-CPF-dokument*

(EAC-CPF: eac-cpf)

Rotelement för EAC-CPF-dokumentet. Namnrymden `urn:isbn:1-931666-33-4` ska deklareras här. Vid användning av SVK-LON-element i anställningsdokumentets `additionalXMLData` deklareras dessutom SVK-LON-namnrymden.

Obligatoriskt.

**XML-element:** `eac-cpf`<br/>
**Datatyp:** —

---

#### SVK-LON:2 - *Kontroll*

(EAC-CPF: control)

Samlingselement för dokumentets administrativa metadata: identifikator, underhållsstatus och underhållshistorik.

Obligatoriskt.

**XML-element:** `control`<br/>
**Datatyp:** —

---

#### SVK-LON:3 - *Identifikator*

(EAC-CPF: recordId)

Unikt identifierar EAC-CPF-dokumentet inom arkivpaketet. Bygger på naturlig nyckel från källdata och är stabil över årsuttag — samma anställning har samma identifikator i alla paket. Se Värdelista 1 för namnmönster per dokumenttyp.

Obligatoriskt.

**XML-element:** `control/recordId`<br/>
**Datatyp:** string

---

#### SVK-LON:4 - *Underhållsstatus*

(EAC-CPF: maintenanceStatus)

Anger dokumentets aktuella underhållsstatus. Värdet ska vara `revised` för reguljära årsuttag och `new` vid första skapandet. Se Värdelista 2.

Obligatoriskt.

**XML-element:** `control/maintenanceStatus`<br/>
**Datatyp:** token

---

#### SVK-LON:5 - *Underhållsansvarig*

(EAC-CPF: maintenanceAgency)

Samlingselement för uppgift om den organisation som ansvarar för underhållet av dokumentet.

Obligatoriskt.

**XML-element:** `control/maintenanceAgency`<br/>
**Datatyp:** —

---

#### SVK-LON:6 - *Ansvarig organisations namn*

(EAC-CPF: agencyName)

Namn på den organisation som ansvarar för arkivpaketet. Ska anges som arbetsgivarens namn eller "Svenska kyrkan".

Obligatoriskt.

**XML-element:** `control/maintenanceAgency/agencyName`<br/>
**Datatyp:** string

---

#### SVK-LON:7 - *Underhållshistorik*

(EAC-CPF: maintenanceHistory)

Samlingselement för dokumentets historik av skapande och ändringar. Ska innehålla minst en `maintenanceEvent`.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory`<br/>
**Datatyp:** —

---

#### SVK-LON:8 - *Underhållshändelse*

(EAC-CPF: maintenanceEvent)

Beskriver en enskild händelse i dokumentets historia. Minst en förekomst krävs (skapandetillfället). Elementet kan upprepas vid ändringar.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory/maintenanceEvent`<br/>
**Datatyp:** —

---

#### SVK-LON:9 - *Händelsetyp*

(EAC-CPF: eventType)

Anger typen av underhållshändelse. Se Värdelista 3.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory/maintenanceEvent/eventType`<br/>
**Datatyp:** token

---

#### SVK-LON:10 - *Händelsedatum*

(EAC-CPF: eventDateTime)

Datum och tid då händelsen inträffade. Anges som `YYYY-MM-DDTHH:MM:SS`. Attributet `standardDateTime` ska innehålla samma värde i maskinläsbart format.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory/maintenanceEvent/eventDateTime`<br/>
**Datatyp:** dateTime

---

#### SVK-LON:11 - *Agenttyp*

(EAC-CPF: agentType)

Anger typen av aktör som utförde händelsen. Se Värdelista 4.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory/maintenanceEvent/agentType`<br/>
**Datatyp:** token

---

#### SVK-LON:12 - *Agent*

(EAC-CPF: agent)

Identifierar aktören som utförde händelsen, t.ex. systemnamnet "Flex Lön export" eller ett personnamn.

Obligatoriskt.

**XML-element:** `control/maintenanceHistory/maintenanceEvent/agent`<br/>
**Datatyp:** string

---

### 3.2 Organisation

Filen `organisation/organisation.xml` innehåller arbetsgivarens organisationsuppgifter. En fil per arbetsgivare och paket. Kontrollelementen SVK-LON:1–12 förutsätts.

---

#### Elementlista 1. Organisation

---

#### SVK-LON:13 - *Identitetsbeskrivning*

(EAC-CPF: cpfDescription)

Samlingselement för identitets- och beskrivningsinformation om organisationen.

Obligatoriskt.

**XML-element:** `cpfDescription`<br/>
**Datatyp:** —

---

#### SVK-LON:14 - *Identitet*

(EAC-CPF: identity)

Samlingselement för organisationens identifierande uppgifter: identifikatorer, typ och namn.

Obligatoriskt.

**XML-element:** `cpfDescription/identity`<br/>
**Datatyp:** —

---

#### SVK-LON:15 - *Enhetstyp*

(EAC-CPF: entityType)

Anger att posten avser en organisation. Värdet ska alltid vara `corporateBody` för arbetsgivardokumentet. Se Värdelista 5.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/entityType`<br/>
**Datatyp:** token

---

#### SVK-LON:16 - *Organisationsnummer*

(EAC-CPF: entityId)

Arbetsgivarens organisationsnummer enligt Bolagsverket. Anges utan bindestreck. Attributet `localType` ska ha värdet `ORG`.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/entityId[@localType="ORG"]`<br/>
**Datatyp:** string

---

#### SVK-LON:17 - *Flex-företagsnummer*

(EAC-CPF: entityId)

Arbetsgivarens interna företagsnummer i Flex Lön. Attributet `localType` ska ha värdet `FlexForetagsnummer`.

**XML-element:** `cpfDescription/identity/entityId[@localType="FlexForetagsnummer"]`<br/>
**Datatyp:** string

---

#### SVK-LON:18 - *FORA-försäkringsnummer*

(EAC-CPF: entityId)

Arbetsgivarens försäkringsnummer hos FORA för kollektivavtalade försäkringar. Anges om tillgängligt. Attributet `localType` ska ha värdet `FORA`.

**XML-element:** `cpfDescription/identity/entityId[@localType="FORA"]`<br/>
**Datatyp:** string

---

#### SVK-LON:19 - *KAP-KL-kundnummer*

(EAC-CPF: entityId)

Arbetsgivarens kundnummer hos KAP-KL för pensionshantering. Anges om tillgängligt. Attributet `localType` ska ha värdet `KAPKL`.

**XML-element:** `cpfDescription/identity/entityId[@localType="KAPKL"]`<br/>
**Datatyp:** string

---

#### SVK-LON:20 - *Namnpost*

(EAC-CPF: nameEntry)

Arbetsgivarens namn. Elementet kan upprepas om organisationen har flera namn, t.ex. kortnamn och officiellt namn.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `cpfDescription/identity/nameEntry`<br/>
**Datatyp:** —

---

#### SVK-LON:21 - *Namnandel*

(EAC-CPF: part)

Själva namnsträngen. För organisationer anges hela namnet som ett enda `part`-element.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry/part`<br/>
**Datatyp:** string

---

#### SVK-LON:22 - *Beskrivning*

(EAC-CPF: description)

Samlingselement för beskrivande uppgifter om organisationen, här adressinformation.

**XML-element:** `cpfDescription/description`<br/>
**Datatyp:** —

---

#### SVK-LON:23 - *Adress*

(EAC-CPF: places/place/address)

Samlingselement för arbetsgivarens postadress.

**XML-element:** `cpfDescription/description/places/place/address`<br/>
**Datatyp:** —

---

#### SVK-LON:24 - *Gatuadress*

(EAC-CPF: addressLine)

Arbetsgivarens gatuadress. Attributet `localType` ska ha värdet `postalAddress`.

**XML-element:** `cpfDescription/description/places/place/address/addressLine[@localType="postalAddress"]`<br/>
**Datatyp:** string

---

#### SVK-LON:25 - *Postnummer*

(EAC-CPF: addressLine)

Arbetsgivarens postnummer. Attributet `localType` ska ha värdet `postalCode`.

**XML-element:** `cpfDescription/description/places/place/address/addressLine[@localType="postalCode"]`<br/>
**Datatyp:** string

---

#### SVK-LON:26 - *Postort*

(EAC-CPF: addressLine)

Arbetsgivarens postort. Attributet `localType` ska ha värdet `postalCity`.

**XML-element:** `cpfDescription/description/places/place/address/addressLine[@localType="postalCity"]`<br/>
**Datatyp:** string

---

#### Exempel 1 – Organisation

```xml
<?xml version="1.0" encoding="UTF-8"?>
<eac-cpf xmlns="urn:isbn:1-931666-33-4"
         xmlns:xlink="http://www.w3.org/1999/xlink">
  <control>
    <recordId>ORG_1234567890</recordId>
    <maintenanceStatus>revised</maintenanceStatus>
    <maintenanceAgency>
      <agencyName>Sunne pastorat</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime standardDateTime="2023-01-15T00:00:00">2023-01-15</eventDateTime>
        <agentType>machine</agentType>
        <agent>Flex Lön export</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <identity>
      <entityType>corporateBody</entityType>
      <entityId localType="ORG">1234567890</entityId>
      <entityId localType="FlexForetagsnummer">42</entityId>
      <entityId localType="FORA">987654</entityId>
      <entityId localType="KAPKL">3</entityId>
      <nameEntry>
        <part>Sunne pastorat</part>
      </nameEntry>
    </identity>
    <description>
      <places>
        <place>
          <address>
            <addressLine localType="postalAddress">Kyrkogatan 12</addressLine>
            <addressLine localType="postalCode">68630</addressLine>
            <addressLine localType="postalCity">Sunne</addressLine>
          </address>
        </place>
      </places>
    </description>
  </cpfDescription>
</eac-cpf>
```

---

### 3.3 Person

Filen `personer/P_<pnr>.xml` innehåller personuppgifter för en arbetstagare. En fil per person och paket. Kontrollelementen SVK-LON:1–12 förutsätts; `recordId` följer mönstret `P_<personnummer>` (utan bindestreck).

---

#### Elementlista 2. Person

---

#### SVK-LON:27 - *Identitetsbeskrivning*

(EAC-CPF: cpfDescription)

Samlingselement för personens identitets- och beskrivningsinformation.

Obligatoriskt.

**XML-element:** `cpfDescription`<br/>
**Datatyp:** —

---

#### SVK-LON:28 - *Identitet*

(EAC-CPF: identity)

Samlingselement för personens identifierande uppgifter: personnummer, namn m.m.

Obligatoriskt.

**XML-element:** `cpfDescription/identity`<br/>
**Datatyp:** —

---

#### SVK-LON:29 - *Enhetstyp*

(EAC-CPF: entityType)

Anger att posten avser en person. Värdet ska alltid vara `person`. Se Värdelista 5.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/entityType`<br/>
**Datatyp:** token

---

#### SVK-LON:30 - *Personnummer*

(EAC-CPF: entityId)

Personens svenska personnummer på formatet `YYYYMMDD-NNNN`. Attributet `localType` ska ha värdet `PersonalIdentityNumber`. Antingen personnummer (SVK-LON:30) eller samordningsnummer (SVK-LON:31) måste anges.

Konditionellt obligatoriskt: minst ett av SVK-LON:30 eller SVK-LON:31 krävs.

**XML-element:** `cpfDescription/identity/entityId[@localType="PersonalIdentityNumber"]`<br/>
**Datatyp:** string

---

#### SVK-LON:31 - *Samordningsnummer*

(EAC-CPF: entityId)

Personens svenska samordningsnummer på formatet `YYYYMMDD-NNNN`, där dagsiffran är födelsedag + 60. Attributet `localType` ska ha värdet `CoordinationNumber`. Används i stället för SVK-LON:30 när personen saknar personnummer.

Konditionellt obligatoriskt: minst ett av SVK-LON:30 eller SVK-LON:31 krävs.

**XML-element:** `cpfDescription/identity/entityId[@localType="CoordinationNumber"]`<br/>
**Datatyp:** string

---

#### SVK-LON:32 - *Förnamnspost*

(EAC-CPF: nameEntry)

Namnpost för personens förnamn. Attributet `localType` ska ha värdet `forename`.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry[@localType="forename"]`<br/>
**Datatyp:** —

---

#### SVK-LON:33 - *Förnamn*

(EAC-CPF: part)

Personens förnamn som det är registrerat i Flex Lön.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry[@localType="forename"]/part`<br/>
**Datatyp:** string

---

#### SVK-LON:34 - *Efternamnpost*

(EAC-CPF: nameEntry)

Namnpost för personens efternamn. Attributet `localType` ska ha värdet `surname`.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry[@localType="surname"]`<br/>
**Datatyp:** —

---

#### SVK-LON:35 - *Efternamn*

(EAC-CPF: part)

Personens efternamn som det är registrerat i Flex Lön.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry[@localType="surname"]/part`<br/>
**Datatyp:** string

---

#### SVK-LON:36 - *Beskrivning*

(EAC-CPF: description)

Samlingselement för beskrivande uppgifter om personen: nationalitet och eventuell skyddsmarkering.

Obligatoriskt.

**XML-element:** `cpfDescription/description`<br/>
**Datatyp:** —

---

#### SVK-LON:37 - *Nationalitet*

(EAC-CPF: localDescription)

Personens nationalitet. Attributet `localType` ska ha värdet `nationality`.

Obligatoriskt.

**XML-element:** `cpfDescription/description/localDescription[@localType="nationality"]`<br/>
**Datatyp:** —

---

#### SVK-LON:38 - *Nationalitetsbeteckning*

(EAC-CPF: term)

Nationalitetsbeteckning i klartext, t.ex. `Sverige`.

Obligatoriskt.

**XML-element:** `cpfDescription/description/localDescription[@localType="nationality"]/term`<br/>
**Datatyp:** string

---

#### SVK-LON:39 - *Skyddad identitet*

(EAC-CPF: descriptiveNote)

Anger att personen har sekretessmarkering eller kvarskrivning. Elementet används enbart när skyddsmarkering föreligger. Innehållet ska vara den fasta texten `Skyddad identitet`. Åtkomstbegränsning hanteras i e-arkivets söklager — personnummer och namn bevaras i sin helhet i paketet.

Används om personen har skyddsmarkering i Flex Lön.

**XML-element:** `cpfDescription/description/descriptiveNote/p`<br/>
**Datatyp:** string

---

#### Exempel 2 – Person

```xml
<?xml version="1.0" encoding="UTF-8"?>
<eac-cpf xmlns="urn:isbn:1-931666-33-4">
  <control>
    <recordId>P_197606280696</recordId>
    <maintenanceStatus>revised</maintenanceStatus>
    <maintenanceAgency>
      <agencyName>Sunne pastorat</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime standardDateTime="2023-01-15T00:00:00">2023-01-15</eventDateTime>
        <agentType>machine</agentType>
        <agent>Flex Lön export</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <identity>
      <entityType>person</entityType>
      <entityId localType="PersonalIdentityNumber">19760628-0696</entityId>
      <nameEntry localType="forename">
        <part>Anna</part>
      </nameEntry>
      <nameEntry localType="surname">
        <part>Lindström</part>
      </nameEntry>
    </identity>
    <description>
      <localDescription localType="nationality">
        <term>Sverige</term>
      </localDescription>
    </description>
  </cpfDescription>
</eac-cpf>
```

---

#### Exempel 3 – Person med skyddad identitet

```xml
<description>
  <localDescription localType="nationality">
    <term>Sverige</term>
  </localDescription>
  <descriptiveNote>
    <p>Skyddad identitet</p>
  </descriptiveNote>
</description>
```

---

### 3.4 Arbetstagare

Filen `arbetstagare/A_<pnr>.xml` är ett tunt dokument som fungerar som krok för kopplingar mellan person och organisation. En fil per arbetstagare och paket. Dokumentet innehåller enbart kontrollelement och relationer. Kontrollelementen SVK-LON:1–12 förutsätts; `recordId` följer mönstret `A_<personnummer>` (utan bindestreck).

---

#### Elementlista 3. Arbetstagare

---

#### SVK-LON:40 - *Identitetsbeskrivning*

(EAC-CPF: cpfDescription)

Samlingselement för arbetstagardokumentets identitets- och relationsinformation.

Obligatoriskt.

**XML-element:** `cpfDescription`<br/>
**Datatyp:** —

---

#### SVK-LON:41 - *Identitet*

(EAC-CPF: identity)

Samlingselement för arbetstagarens identifierande uppgifter. Innehåller enbart enhetstyp och ett övergripande namnElement — detaljerade personuppgifter finns i persondokumentet (3.3).

Obligatoriskt.

**XML-element:** `cpfDescription/identity`<br/>
**Datatyp:** —

---

#### SVK-LON:42 - *Enhetstyp*

(EAC-CPF: entityType)

Anger att posten avser en person i rollen som arbetstagare. Värdet ska alltid vara `person`. Se Värdelista 5.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/entityType`<br/>
**Datatyp:** token

---

#### SVK-LON:43 - *Namnpost*

(EAC-CPF: nameEntry)

Arbetstagarens fullständiga namn i en sammanhållen namnpost. Anges som för- och efternamn åtskilda av mellanslag.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry`<br/>
**Datatyp:** —

---

#### SVK-LON:44 - *Fullständigt namn*

(EAC-CPF: part)

Arbetstagarens fullständiga namn.

Obligatoriskt.

**XML-element:** `cpfDescription/identity/nameEntry/part`<br/>
**Datatyp:** string

---

#### SVK-LON:45 - *Relationer*

(EAC-CPF: relations)

Samlingselement för arbetstagardokumentets relationer till organisation och persondokument.

Obligatoriskt.

**XML-element:** `relations`<br/>
**Datatyp:** —

---

#### SVK-LON:46 - *Relation till organisation*

(EAC-CPF: cpfRelation)

Pekar på den organisation där arbetstagaren är anställd. Attributet `cpfRelationType` ska ha värdet `isEmployedBy`. Attributet `xlink:href` ska peka på organisationsdokumentets `recordId`.

Obligatoriskt.

**XML-element:** `relations/cpfRelation[@cpfRelationType="isEmployedBy"]`<br/>
**Datatyp:** —

---

#### SVK-LON:47 - *Relation till person*

(EAC-CPF: cpfRelation)

Pekar på det persondokument som innehåller fullständiga personuppgifter. Attributet `cpfRelationType` ska ha värdet `sameAs`. Attributet `xlink:href` ska peka på persondokumentets `recordId`.

Obligatoriskt.

**XML-element:** `relations/cpfRelation[@cpfRelationType="sameAs"]`<br/>
**Datatyp:** —

---

#### Exempel 4 – Arbetstagare

```xml
<?xml version="1.0" encoding="UTF-8"?>
<eac-cpf xmlns="urn:isbn:1-931666-33-4"
         xmlns:xlink="http://www.w3.org/1999/xlink">
  <control>
    <recordId>A_197606280696</recordId>
    <maintenanceStatus>revised</maintenanceStatus>
    <maintenanceAgency>
      <agencyName>Sunne pastorat</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime standardDateTime="2023-01-15T00:00:00">2023-01-15</eventDateTime>
        <agentType>machine</agentType>
        <agent>Flex Lön export</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <identity>
      <entityType>person</entityType>
      <nameEntry>
        <part>Anna Lindström</part>
      </nameEntry>
    </identity>
  </cpfDescription>
  <relations>
    <cpfRelation cpfRelationType="isEmployedBy"
                 xlink:type="simple"
                 xlink:href="../organisation/organisation.xml#ORG_1234567890"/>
    <cpfRelation cpfRelationType="sameAs"
                 xlink:type="simple"
                 xlink:href="../personer/P_197606280696.xml#P_197606280696"/>
  </relations>
</eac-cpf>
```

---

### 3.5 Anställning

Filen `anstallningar/F_<anstallningsnummer>.xml` innehåller anställningsdata för en enskild anställning, inklusive befattning, grundlön och anställningstillägget (avsnitt 3.6). En fil per anställning och paket. Kontrollelementen SVK-LON:1–12 förutsätts; `recordId` följer mönstret `F_<anstallningsnummer>`.

FGS Personal utökar EAC-CPF med `employmentDescription` inuti `cpfDescription`. SVK-LON-elementen placeras i `additionalXMLData` inuti `employmentDescription`.

---

#### Elementlista 4. Anställning

---

#### SVK-LON:48 - *Identitetsbeskrivning*

(EAC-CPF: cpfDescription)

Samlingselement för anställningsdokumentets innehåll.

Obligatoriskt.

**XML-element:** `cpfDescription`<br/>
**Datatyp:** —

---

#### SVK-LON:49 - *Anställningsbeskrivning*

(FGS Personal: employmentDescription)

FGS-specifikt samlingselement för anställningens uppgifter: identifikatorer, befattning, lön och tilläggsinformation.

Obligatoriskt.

**XML-element:** `cpfDescription/employmentDescription`<br/>
**Datatyp:** —

---

#### SVK-LON:50 - *Anställningsnummer*

(FGS Personal: employmentId)

Anställningens nummer i Flex Lön. Används som primär identifierare för anställningen inom arbetsgivaren.

Obligatoriskt.

**XML-element:** `cpfDescription/employmentDescription/employmentId`<br/>
**Datatyp:** string

---

#### SVK-LON:51 - *Befattningar*

(FGS Personal: positions)

Samlingselement för anställningens befattningar. Minst en befattning ska anges.

Obligatoriskt.

**XML-element:** `cpfDescription/employmentDescription/positions`<br/>
**Datatyp:** —

---

#### SVK-LON:52 - *Befattning*

(FGS Personal: position)

En enskild befattning. Elementet kan upprepas om anställningen har haft flera befattningar.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `cpfDescription/employmentDescription/positions/position`<br/>
**Datatyp:** —

---

#### SVK-LON:53 - *Befattningskod (BKSK)*

(FGS Personal: term)

Befattningens kod och klartext enligt BKSK (Befattningskod Svenska kyrkan). Attributet `source` ska ha värdet `BKSK`. Attributet `code` innehåller den numeriska BKSK-koden. Elementets textinnehåll är klartextbeteckningen.

**XML-element:** `positions/position/term[@source="BKSK"]`<br/>
**Datatyp:** string

---

#### SVK-LON:54 - *Befattningsbeskrivning*

(FGS Personal: description)

Befattningens namn i klartext, som det är registrerat i Flex Lön. Används i tillägg till eller i stället för BKSK-koden.

**XML-element:** `positions/position/description`<br/>
**Datatyp:** string

---

#### SVK-LON:55 - *Löneavtal*

(FGS Personal: salaryAgreements)

Samlingselement för anställningens grundlönehistorik. Grundlön avser avtalad månadslön eller timlön (det FGS kallar "salary agreement"). Lönetillägg, sysselsättningsgrad och heltidsmått finns i anställningstillägget (avsnitt 3.6).

**XML-element:** `cpfDescription/employmentDescription/salaryAgreements`<br/>
**Datatyp:** —

---

#### SVK-LON:56 - *Grundlönepost*

(FGS Personal: salaryAgreement)

En enskild grundlön med tillhörande giltighetsperiod. Upprepas när lönenivån förändras. Tre attribut krävs: `salaryType`, `amount` och `currency`.

Elementet kan upprepas.

**XML-element:** `cpfDescription/employmentDescription/salaryAgreements/salaryAgreement`<br/>
**Datatyp:** —

---

#### SVK-LON:57 - *Lönetyp*

(FGS Personal: salaryType)

Anger om grundlönen är månadslön eller timlön. Se Värdelista 6.

Obligatoriskt (attribut på SVK-LON:56).

**XML-element:** `salaryAgreement/@salaryType`<br/>
**Datatyp:** token

---

#### SVK-LON:58 - *Lönebelopp*

(FGS Personal: amount)

Grundlönens belopp uttryckt i den valuta som anges i `currency`. För månadslön anges heltidsmånadslön. Decimaltal med punkt som decimaltecken.

Obligatoriskt (attribut på SVK-LON:56).

**XML-element:** `salaryAgreement/@amount`<br/>
**Datatyp:** decimal

---

#### SVK-LON:59 - *Valuta för grundlön*

(FGS Personal: currency)

Valutakod enligt ISO 4217. För Svenska kyrkans löner ska värdet alltid vara `SEK`.

Obligatoriskt (attribut på SVK-LON:56).

**XML-element:** `salaryAgreement/@currency`<br/>
**Datatyp:** ValutakodType

---

#### SVK-LON:60 - *Löneperiod*

(FGS Personal: salaryPeriod)

Samlingselement för grundlönepostens giltighetsperiod.

Obligatoriskt.

**XML-element:** `salaryAgreement/salaryPeriod`<br/>
**Datatyp:** —

---

#### SVK-LON:61 - *Datumintervall*

(FGS Personal: dateRange)

Samlingselement för löneperiodens start- och slutdatum.

Obligatoriskt.

**XML-element:** `salaryAgreement/salaryPeriod/dateRange`<br/>
**Datatyp:** —

---

#### SVK-LON:62 - *Löneperiodens startdatum*

(FGS Personal: startDate)

Datum från vilket grundlöneposten gäller.

Obligatoriskt.

**XML-element:** `salaryAgreement/salaryPeriod/dateRange/startDate`<br/>
**Datatyp:** date

---

#### SVK-LON:63 - *Löneperiodens slutdatum*

(FGS Personal: endDate)

Datum till och med vilket grundlöneposten gäller. Utelämnas om lönen gäller tills vidare.

**XML-element:** `salaryAgreement/salaryPeriod/dateRange/endDate`<br/>
**Datatyp:** date

---

#### SVK-LON:64 - *Tilläggselement*

(FGS Personal: additionalElements)

Samlingselement för anpassningsschemats data. Innehåller `additionalXMLData` med SVK-LON-elementet `anstallningstillagg`.

**XML-element:** `cpfDescription/employmentDescription/additionalElements`<br/>
**Datatyp:** —

---

#### SVK-LON:65 - *Ytterligare XML-data*

(FGS Personal: additionalXMLData)

Behållare för SVK-LON-schemat. Innehåller elementet `anstallningstillagg` i namnrymden `https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1`.

**XML-element:** `cpfDescription/employmentDescription/additionalElements/additionalXMLData`<br/>
**Datatyp:** —

---

#### SVK-LON:66 - *Relationer*

(EAC-CPF: relations)

Samlingselement för anställningsdokumentets relationer till arbetstagare och organisation.

**XML-element:** `relations`<br/>
**Datatyp:** —

---

#### SVK-LON:67 - *Relation till arbetstagare*

(EAC-CPF: cpfRelation)

Pekar på arbetstagardokumentet. Attributet `cpfRelationType` ska ha värdet `creatorOf`. Attributet `xlink:href` ska peka på arbetstagardokumentets `recordId`.

**XML-element:** `relations/cpfRelation[@cpfRelationType="creatorOf"]`<br/>
**Datatyp:** —

---

#### SVK-LON:68 - *Relation till organisation*

(EAC-CPF: cpfRelation)

Pekar på organisationsdokumentet. Attributet `cpfRelationType` ska ha värdet `isAssociatedWith`. Attributet `xlink:href` ska peka på organisationsdokumentets `recordId`.

**XML-element:** `relations/cpfRelation[@cpfRelationType="isAssociatedWith"]`<br/>
**Datatyp:** —

---

#### Exempel 5 – Anställning (förenklat)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<eac-cpf xmlns="urn:isbn:1-931666-33-4"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">
  <control>
    <recordId>F_20</recordId>
    <maintenanceStatus>revised</maintenanceStatus>
    <maintenanceAgency>
      <agencyName>Sunne pastorat</agencyName>
    </maintenanceAgency>
    <maintenanceHistory>
      <maintenanceEvent>
        <eventType>created</eventType>
        <eventDateTime standardDateTime="2023-01-15T00:00:00">2023-01-15</eventDateTime>
        <agentType>machine</agentType>
        <agent>Flex Lön export</agent>
      </maintenanceEvent>
    </maintenanceHistory>
  </control>
  <cpfDescription>
    <employmentDescription>
      <employmentId>20</employmentId>
      <positions>
        <position>
          <term source="BKSK" code="421005">Kyrkvaktmästare</term>
          <description>Kyrkvaktmästare</description>
        </position>
      </positions>
      <salaryAgreements>
        <salaryAgreement salaryType="monthlyPay" amount="28000" currency="SEK">
          <salaryPeriod>
            <dateRange>
              <startDate>2020-01-01</startDate>
            </dateRange>
          </salaryPeriod>
        </salaryAgreement>
        <salaryAgreement salaryType="monthlyPay" amount="29500" currency="SEK">
          <salaryPeriod>
            <dateRange>
              <startDate>2022-04-01</startDate>
            </dateRange>
          </salaryPeriod>
        </salaryAgreement>
      </salaryAgreements>
      <additionalElements>
        <additionalXMLData>
          <svk:anstallningstillagg>
            <!-- Se avsnitt 3.6 -->
          </svk:anstallningstillagg>
        </additionalXMLData>
      </additionalElements>
    </employmentDescription>
  </cpfDescription>
  <relations>
    <cpfRelation cpfRelationType="creatorOf"
                 xlink:type="simple"
                 xlink:href="../arbetstagare/A_197606280696.xml#A_197606280696"/>
    <cpfRelation cpfRelationType="isAssociatedWith"
                 xlink:type="simple"
                 xlink:href="../organisation/organisation.xml#ORG_1234567890"/>
  </relations>
</eac-cpf>
```

---

### 3.6 Anställningstillägg

Elementet `anstallningstillagg` placeras i anställningsdokumentets `additionalXMLData` och tillhör namnrymden `https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1`. Det samlar all anställningsspecifik information som inte ryms i FGS Personal: anställningsperioder, sysselsättningsgrad, heltidsmått, lönetillägg, kostnadsfördelningar och standardkonteringar.

Sökvägar i denna sektion är relativa till `svk:anstallningstillagg` (med prefixet `svk:` utelämnat för läsbarhet).

---

#### Elementlista 5. Anställningstillägg

---

#### SVK-LON:69 - *Anställningstillägg*

Rotelement för SVK-LON-schemat i anställningssammanhang. Placeras direkt inuti `additionalXMLData`.

**XML-element:** `svk:anstallningstillagg`<br/>
**Datatyp:** —

---

#### SVK-LON:70 - *Utbetalningsgruppreferens*

Referens till utbetalningsgruppen som anställningen tillhör. Utbetalningsgruppens fullständiga uppgifter finns i registerfilen `register/utbetalningsgrupper.xml`.

**XML-element:** `utbetalningsgruppReferens`<br/>
**Datatyp:** —

---

#### SVK-LON:71 - *Utbetalningsgrupps-id (referens)*

Id:t som matchar en `utbetalningsgrupp/id` i registret.

Obligatoriskt om SVK-LON:70 används.

**XML-element:** `utbetalningsgruppReferens/id`<br/>
**Datatyp:** string

---

#### SVK-LON:72 - *Personalkategori*

Anställningens personalkategori som den är registrerad i Flex Lön, t.ex. `MÅN` (månadsavlönad) eller `TIM` (timanställd). Används som del av primärnyckeln för lönearter.

**XML-element:** `personalkategori`<br/>
**Datatyp:** —

---

#### SVK-LON:73 - *Personalkategorikod*

Koden för personalkategorin, t.ex. `MÅN`.

Obligatoriskt om SVK-LON:72 används.

**XML-element:** `personalkategori/kod`<br/>
**Datatyp:** string

---

#### SVK-LON:74 - *Personalkategoribenämning*

Personalkategorins benämning i klartext.

**XML-element:** `personalkategori/benamning`<br/>
**Datatyp:** string

---

#### SVK-LON:75 - *Anställningsperioder*

Samlingselement för anställningens perioder. En anställning kan ha flera perioder när villkor som anställningsform eller löneform förändras.

**XML-element:** `anstallningsperioder`<br/>
**Datatyp:** —

---

#### SVK-LON:76 - *Anställningsperiod*

En enskild anställningsperiod med form, löneform och eventuell avslutsorsak. Elementet kan upprepas.

Elementet kan upprepas.

**XML-element:** `anstallningsperioder/anstallningsperiod`<br/>
**Datatyp:** —

---

#### SVK-LON:77 - *Anställningsperiod-id*

Unikt identifierar anställningsperioden inom anställningen. Härleds från källdata i Flex Lön.

Obligatoriskt.

**XML-element:** `anstallningsperiod/id`<br/>
**Datatyp:** string

---

#### SVK-LON:78 - *Giltighetsperiod*

Samlingselement för en posts giltighetstid. Används av anställningsperiod, sysselsättningsgrad, heltidsmått, lönetillägg och kostnadsfördelning. Slutdatum utelämnas för poster som löper tills vidare.

Obligatoriskt.

**XML-element:** `*/giltighetsperiod`<br/>
**Datatyp:** —

---

#### SVK-LON:79 - *Startdatum*

Datum från vilket posten gäller.

Obligatoriskt.

**XML-element:** `giltighetsperiod/startdatum`<br/>
**Datatyp:** date

---

#### SVK-LON:80 - *Slutdatum*

Datum till och med vilket posten gäller. Utelämnas för poster som löper tills vidare. Fiktiva "tills vidare"-datum från källsystemet (t.ex. 2049-01-01) ska omvandlas till utelämnat slutdatum.

**XML-element:** `giltighetsperiod/slutdatum`<br/>
**Datatyp:** date

---

#### SVK-LON:81 - *Anställningsform*

Anställningens form under perioden. Se Värdelista 7 för rekommenderade värden. Öppen sträng tillåts för källsystemsspecifika varianter.

Obligatoriskt.

**XML-element:** `anstallningsperiod/anstallningsform`<br/>
**Datatyp:** string

---

#### SVK-LON:82 - *Löneform*

Anger om anställningen ersätts med månadslön eller timlön under perioden. Se Värdelista 8.

Obligatoriskt.

**XML-element:** `anstallningsperiod/loneform`<br/>
**Datatyp:** string

---

#### SVK-LON:83 - *Avslutsorsak*

Orsaken till att anställningsperioden avslutades. Utelämnas för pågående perioder. Se Värdelista 9 för rekommenderade värden.

**XML-element:** `anstallningsperiod/avslutsorsak`<br/>
**Datatyp:** string

---

#### SVK-LON:84 - *Sysselsättningsgrader*

Samlingselement för tidsserien av sysselsättningsgrader. En ny post skapas varje gång sysselsättningsgraden förändras.

**XML-element:** `sysselsattningsgrader`<br/>
**Datatyp:** —

---

#### SVK-LON:85 - *Sysselsättningsgrad*

En enskild sysselsättningsgrad med giltighetsperiod. Elementet kan upprepas.

Elementet kan upprepas.

**XML-element:** `sysselsattningsgrader/sysselsattningsgrad`<br/>
**Datatyp:** —

---

#### SVK-LON:86 - *Sysselsättningsgrad-id*

Unikt identifierar sysselsättningsgradsposten inom anställningen.

Obligatoriskt.

**XML-element:** `sysselsattningsgrad/id`<br/>
**Datatyp:** string

---

#### SVK-LON:87 - *Sysselsättningsprocent*

Sysselsättningsgraden uttryckt i procent av heltid. Värdet 100 innebär heltid.

Obligatoriskt.

**XML-element:** `sysselsattningsgrad/procent`<br/>
**Datatyp:** ProcentType

---

#### SVK-LON:88 - *Heltidsmått*

Samlingselement för tidsserien av heltidsmått (timmar per vecka vid heltid). En ny post skapas varje gång heltidsmåttet förändras.

**XML-element:** `heltidsmatt`<br/>
**Datatyp:** —

---

#### SVK-LON:89 - *Arbetsmått*

En enskild heltidsmåttspost med giltighetsperiod. Elementet kan upprepas.

Elementet kan upprepas.

**XML-element:** `heltidsmatt/arbetsmatt`<br/>
**Datatyp:** —

---

#### SVK-LON:90 - *Arbetsmått-id*

Unikt identifierar arbetsmåttsposten inom anställningen.

Obligatoriskt.

**XML-element:** `arbetsmatt/id`<br/>
**Datatyp:** string

---

#### SVK-LON:91 - *Timmar per vecka*

Heltidsmåttet i timmar per vecka, t.ex. `40` för 40-timmarsvecka.

Obligatoriskt.

**XML-element:** `arbetsmatt/timmarPerVecka`<br/>
**Datatyp:** decimal

---

#### SVK-LON:92 - *Lönetillägg*

Samlingselement för tidsserien av lönetillägg. Ett lönetillägg är ett individuellt tillägg utöver grundlönen, t.ex. OB-tillägg eller arbetstidsförkortning. En ny post skapas varje gång tillägget förändras.

**XML-element:** `lonetillagg`<br/>
**Datatyp:** —

---

#### SVK-LON:93 - *Tillägg*

En enskild lönetilläggpost med namn, värde och giltighetsperiod. Elementet kan upprepas.

Elementet kan upprepas.

**XML-element:** `lonetillagg/tillagg`<br/>
**Datatyp:** —

---

#### SVK-LON:94 - *Tilläggs-id*

Unikt identifierar lönetilläggposten inom anställningen.

Obligatoriskt.

**XML-element:** `tillagg/id`<br/>
**Datatyp:** string

---

#### SVK-LON:95 - *Tilläggets namn*

Lönetilläggets benämning i klartext, t.ex. `OB-tillägg kväll`.

Obligatoriskt.

**XML-element:** `tillagg/namn`<br/>
**Datatyp:** string

---

#### SVK-LON:96 - *Tilläggets värde*

Tilläggets numeriska värde. Attributet `typ` anger hur värdet ska tolkas: `belopp` för kronbelopp (kräver att SVK-LON:97 anges) eller `faktor` för multiplikationsfaktor (SVK-LON:97 ska inte anges). Se Värdelista 10.

Obligatoriskt.

**XML-element:** `tillagg/varde`<br/>
**Datatyp:** decimal (med attribut `typ`)

---

#### SVK-LON:97 - *Tilläggets valuta*

Valutakod för tillägget, obligatorisk när `varde/@typ="belopp"`. Ska vara `SEK`. Ska inte anges när `varde/@typ="faktor"`.

Konditionellt obligatoriskt.

**XML-element:** `tillagg/valuta`<br/>
**Datatyp:** ValutakodType

---

#### SVK-LON:98 - *Kostnadsfördelningar*

Samlingselement för anställningens förhandsdefinierade kostnadsfördelningar. En kostnadsfördelning anger hur lönekostnaden procentuellt fördelas på konteringsdimensioner under en given period.

**XML-element:** `kostnadsfordelningar`<br/>
**Datatyp:** —

---

#### SVK-LON:99 - *Kostnadsfördelning*

En enskild kostnadsfördelningspost. En fördelning med samma `kostnadsfordelningId` och överlappande giltighetsperiod kan bestå av flera poster med `ordningsnummer` för att hantera procentuell uppdelning på dimensionsuppsättningar. Elementet kan upprepas.

Elementet kan upprepas.

**XML-element:** `kostnadsfordelningar/kostnadsfordelning`<br/>
**Datatyp:** —

---

#### SVK-LON:100 - *Kostnadsfördelnings-id*

Identifierar den logiska fördelningsgruppen. Flera poster med samma `kostnadsfordelningId` utgör tillsammans en fördelning.

Obligatoriskt.

**XML-element:** `kostnadsfordelning/kostnadsfordelningId`<br/>
**Datatyp:** string

---

#### SVK-LON:101 - *Ordningsnummer*

Anger radordning inom en fördelningsgrupp (samma `kostnadsfordelningId`). Börjar på 1.

Obligatoriskt.

**XML-element:** `kostnadsfordelning/ordningsnummer`<br/>
**Datatyp:** integer

---

#### SVK-LON:102 - *Procentfördelning (kostnadsfördelning)*

Denna posts procentandel av fördelningsgruppens totalkostnad. Summan av alla poster med samma `kostnadsfordelningId` och överlappande period ska vara 100.

Obligatoriskt.

**XML-element:** `kostnadsfordelning/procentfordelning`<br/>
**Datatyp:** ProcentType

---

#### SVK-LON:103 - *Dimensioner (kostnadsfördelning)*

Samlingselement för de konteringsdimensioner som gäller för denna post.

Obligatoriskt.

**XML-element:** `kostnadsfordelning/dimensioner`<br/>
**Datatyp:** —

---

#### SVK-LON:104 - *Dimension*

En enskild konteringsdimension med namn och värde. Elementet kan upprepas, en förekomst per dimension.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `dimensioner/dimension`<br/>
**Datatyp:** —

---

#### SVK-LON:105 - *Dimensionsnamn*

Dimensionens benämning, t.ex. `Projekt` eller `Verksamhet`.

Obligatoriskt.

**XML-element:** `dimension/namn`<br/>
**Datatyp:** string

---

#### SVK-LON:106 - *Dimensionsvärde*

Dimensionens värde för denna post, t.ex. ett projektnummer.

Obligatoriskt.

**XML-element:** `dimension/varde`<br/>
**Datatyp:** string

---

#### SVK-LON:107 - *Standardkonteringar*

Samlingselement för anställningens standardkonteringar (i Flex Lön kallat "hemkontering"). En standardkontering anger den förhandsdefinierade konteringsregel per dimension som används som standard när ingen annan regel gäller.

**XML-element:** `standardkonteringar`<br/>
**Datatyp:** —

---

#### SVK-LON:108 - *Standardkontering*

En standardkontering per konteringsdimension. Elementet kan upprepas, ett per dimension.

Elementet kan upprepas.

**XML-element:** `standardkonteringar/standardkontering`<br/>
**Datatyp:** —

---

#### SVK-LON:109 - *Dimensions-id*

Konteringsdimensionens tekniska identifierare i källsystemet.

Obligatoriskt.

**XML-element:** `standardkontering/dimensionId`<br/>
**Datatyp:** string

---

#### SVK-LON:110 - *Dimensionsnamn (standardkontering)*

Konteringsdimensionens benämning i klartext.

Obligatoriskt.

**XML-element:** `standardkontering/dimensionNamn`<br/>
**Datatyp:** string

---

#### SVK-LON:111 - *Fördelningar*

Samlingselement för standardkonteringens fördelningar inom dimensionen. Möjliggör procentuell uppdelning på flera konteringsvärden.

Obligatoriskt.

**XML-element:** `standardkontering/fordelningar`<br/>
**Datatyp:** —

---

#### SVK-LON:112 - *Fördelning*

En enskild fördelning med konteringsvärde och procentandel. Elementet kan upprepas. Summan av procentandelar inom samma `standardkontering` ska vara 100.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `fordelningar/fordelning`<br/>
**Datatyp:** —

---

#### SVK-LON:113 - *Konteringsvärde*

Det kontovärde eller den kodnyckel som gäller för denna fördelning, t.ex. ett kostnadsstelle.

Obligatoriskt.

**XML-element:** `fordelning/kontering`<br/>
**Datatyp:** string

---

#### SVK-LON:114 - *Procentandel (standardkontering)*

Denna fördelnings andel i procent.

Obligatoriskt.

**XML-element:** `fordelning/procent`<br/>
**Datatyp:** ProcentType

---

#### Exempel 6 – Anställningstillägg

```xml
<svk:anstallningstillagg
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">

  <svk:utbetalningsgruppReferens>
    <svk:id>1</svk:id>
  </svk:utbetalningsgruppReferens>

  <svk:personalkategori>
    <svk:kod>MÅN</svk:kod>
    <svk:benamning>Månadsavlönade</svk:benamning>
  </svk:personalkategori>

  <svk:anstallningsperioder>
    <svk:anstallningsperiod>
      <svk:id>1</svk:id>
      <svk:giltighetsperiod>
        <svk:startdatum>2018-05-01</svk:startdatum>
      </svk:giltighetsperiod>
      <svk:anstallningsform>Tillsvidareanställd</svk:anstallningsform>
      <svk:loneform>Månadslön</svk:loneform>
    </svk:anstallningsperiod>
  </svk:anstallningsperioder>

  <svk:sysselsattningsgrader>
    <svk:sysselsattningsgrad>
      <svk:id>1</svk:id>
      <svk:procent>100</svk:procent>
      <svk:giltighetsperiod>
        <svk:startdatum>2018-05-01</svk:startdatum>
        <svk:slutdatum>2021-08-31</svk:slutdatum>
      </svk:giltighetsperiod>
    </svk:sysselsattningsgrad>
    <svk:sysselsattningsgrad>
      <svk:id>2</svk:id>
      <svk:procent>80</svk:procent>
      <svk:giltighetsperiod>
        <svk:startdatum>2021-09-01</svk:startdatum>
      </svk:giltighetsperiod>
    </svk:sysselsattningsgrad>
  </svk:sysselsattningsgrader>

  <svk:heltidsmatt>
    <svk:arbetsmatt>
      <svk:id>1</svk:id>
      <svk:timmarPerVecka>40</svk:timmarPerVecka>
      <svk:giltighetsperiod>
        <svk:startdatum>2018-05-01</svk:startdatum>
      </svk:giltighetsperiod>
    </svk:arbetsmatt>
  </svk:heltidsmatt>

  <svk:lonetillagg>
    <svk:tillagg>
      <svk:id>1</svk:id>
      <svk:namn>OB-tillägg kväll</svk:namn>
      <svk:varde typ="belopp">1250.00</svk:varde>
      <svk:valuta>SEK</svk:valuta>
      <svk:giltighetsperiod>
        <svk:startdatum>2020-01-01</svk:startdatum>
      </svk:giltighetsperiod>
    </svk:tillagg>
  </svk:lonetillagg>

  <svk:kostnadsfordelningar>
    <svk:kostnadsfordelning>
      <svk:kostnadsfordelningId>KF1</svk:kostnadsfordelningId>
      <svk:ordningsnummer>1</svk:ordningsnummer>
      <svk:giltighetsperiod>
        <svk:startdatum>2020-01-01</svk:startdatum>
      </svk:giltighetsperiod>
      <svk:procentfordelning>100</svk:procentfordelning>
      <svk:dimensioner>
        <svk:dimension>
          <svk:namn>Verksamhet</svk:namn>
          <svk:varde>4210</svk:varde>
        </svk:dimension>
        <svk:dimension>
          <svk:namn>Projekt</svk:namn>
          <svk:varde>P-2022-001</svk:varde>
        </svk:dimension>
      </svk:dimensioner>
    </svk:kostnadsfordelning>
  </svk:kostnadsfordelningar>

  <svk:standardkonteringar>
    <svk:standardkontering>
      <svk:dimensionId>10</svk:dimensionId>
      <svk:dimensionNamn>Verksamhet</svk:dimensionNamn>
      <svk:fordelningar>
        <svk:fordelning>
          <svk:kontering>4210</svk:kontering>
          <svk:procent>100</svk:procent>
        </svk:fordelning>
      </svk:fordelningar>
    </svk:standardkontering>
  </svk:standardkonteringar>

</svk:anstallningstillagg>
```

---
### 3.7 Lönekörningar

Filen `loneutbetalningar/lonekorningar.xml` innehåller en rad per lönekörning (ett utbetalningstillfälle för en anställning). Filen är ett separat dokument i paketet med rotelement `lonekorningar` i SVK-LON-namnrymden.

---

#### Elementlista 6. Lönekörningar

---

#### SVK-LON:115 - *Lönekörningar*

Rotelement för lönekörningsfilen. Innehåller en eller flera `lonekorning`-poster.

Obligatoriskt.

**XML-element:** `svk:lonekorningar`<br/>
**Datatyp:** —

---

#### SVK-LON:116 - *Lönekörning*

En enskild lönekörning: ett utbetalningstillfälle för en specifik anställning vid ett givet datum. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `lonekorning`<br/>
**Datatyp:** —

---

#### SVK-LON:117 - *Lönekörnings-id*

Syntetiskt id på formen `LK_<år>_<löpnummer>`, t.ex. `LK_2022_000001`. Årtalet är paketets uttagsår. Löpnumret börjar om från 1 i varje paket. Används som korsreferens från lönetransaktioner.

Obligatoriskt.

**XML-element:** `lonekorning/id`<br/>
**Datatyp:** string

---

#### SVK-LON:118 - *Lönekörningsnummer*

Källsystemets eget beteckningsnummer för körningen, t.ex. `2022-09`. Bevaras från Flex Lön och används som naturlig nyckel vid ackumulering av paket.

Obligatoriskt.

**XML-element:** `lonekorning/lonekorningsnummer`<br/>
**Datatyp:** string

---

#### SVK-LON:119 - *Utbetalningsdatum*

Det datum då löneutbetalningen genomfördes.

Obligatoriskt.

**XML-element:** `lonekorning/utbetalningsdatum`<br/>
**Datatyp:** date

---

#### SVK-LON:120 - *Utbetalningsgruppreferens (lönekörning)*

Referens till utbetalningsgruppen som körningen tillhör. Strukturen är identisk med SVK-LON:70–71.

Obligatoriskt.

**XML-element:** `lonekorning/utbetalningsgruppReferens`<br/>
**Datatyp:** —

---

#### SVK-LON:121 - *Anställningsreferens*

Samlingselement för referens till den anställning som körningen avser, via personnummer och anställningsnummer.

Obligatoriskt.

**XML-element:** `lonekorning/anstallningReferens`<br/>
**Datatyp:** —

---

#### SVK-LON:122 - *Anställningsnummer (referens)*

Anställningsnumret som identifierar anställningen hos arbetsgivaren.

Obligatoriskt.

**XML-element:** `lonekorning/anstallningReferens/anstallningsnummer`<br/>
**Datatyp:** string

---

#### SVK-LON:123 - *Personnummer (referens)*

Personnumret (utan bindestreck) som identifierar personen. Matchar `recordId`-mönstret i person- och arbetstagardokumenten.

Obligatoriskt.

**XML-element:** `lonekorning/anstallningReferens/personnummer`<br/>
**Datatyp:** string

---

#### SVK-LON:124 - *Lönespecifikation*

Referens till lönespecifikationsfilen i HTML-format för denna körning. Elementet utelämnas om ingen lönespecifikation finns tillgänglig.

**XML-element:** `lonekorning/lonespecifikation`<br/>
**Datatyp:** —

---

#### SVK-LON:125 - *Länk till lönespecifikation*

Relativ URI-referens till HTML-filen, relativt lönekörningsfilen. Namnges enligt mönstret `../lonespecifikationer/<organisationsnummer>_<personnummer>_<anstallningsnummer>_<period>_lonespec.html`.

Obligatoriskt om SVK-LON:124 används.

**XML-element:** `lonekorning/lonespecifikation/@href`<br/>
**Datatyp:** anyURI

---

#### Exempel 7 – Lönekörningar

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:lonekorningar
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">

  <svk:lonekorning>
    <svk:id>LK_2022_000001</svk:id>
    <svk:lonekorningsnummer>2022-09</svk:lonekorningsnummer>
    <svk:utbetalningsdatum>2022-09-28</svk:utbetalningsdatum>
    <svk:utbetalningsgruppReferens>
      <svk:id>1</svk:id>
    </svk:utbetalningsgruppReferens>
    <svk:anstallningReferens>
      <svk:anstallningsnummer>20</svk:anstallningsnummer>
      <svk:personnummer>197606280696</svk:personnummer>
    </svk:anstallningReferens>
    <svk:lonespecifikation
        href="../lonespecifikationer/1234567890_197606280696_20_202209_lonespec.html"/>
  </svk:lonekorning>

  <svk:lonekorning>
    <svk:id>LK_2022_000002</svk:id>
    <svk:lonekorningsnummer>2022-09</svk:lonekorningsnummer>
    <svk:utbetalningsdatum>2022-09-28</svk:utbetalningsdatum>
    <svk:utbetalningsgruppReferens>
      <svk:id>1</svk:id>
    </svk:utbetalningsgruppReferens>
    <svk:anstallningReferens>
      <svk:anstallningsnummer>35</svk:anstallningsnummer>
      <svk:personnummer>198203154521</svk:personnummer>
    </svk:anstallningReferens>
  </svk:lonekorning>

</svk:lonekorningar>
```

---

### 3.8 Lönetransaktioner

Filen `loneutbetalningar/lonetransaktioner.xml` innehåller en rad per transaktionsrad ur en lönekörning. En lönekörning kan ha många transaktioner. Filen är ett separat dokument med rotelement `lonetransaktioner` i SVK-LON-namnrymden.

---

#### Elementlista 7. Lönetransaktioner

---

#### SVK-LON:126 - *Lönetransaktioner*

Rotelement för lönetransaktionsfilen.

Obligatoriskt.

**XML-element:** `svk:lonetransaktioner`<br/>
**Datatyp:** —

---

#### SVK-LON:127 - *Lönetransaktion*

En enskild transaktionsrad. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `lonetransaktion`<br/>
**Datatyp:** —

---

#### SVK-LON:128 - *Lönetransaktions-id*

Syntetiskt id på formen `LT_<år>_<löpnummer>`, t.ex. `LT_2022_000001`. Används som korsreferens från konteringar.

Obligatoriskt.

**XML-element:** `lonetransaktion/id`<br/>
**Datatyp:** string

---

#### SVK-LON:129 - *Transaktions-id*

Källsystemets eget transaktions-id. Bevaras från Flex Lön som naturlig nyckel.

Obligatoriskt.

**XML-element:** `lonetransaktion/transaktionId`<br/>
**Datatyp:** string

---

#### SVK-LON:130 - *Lönekörningsreferens*

Det syntetiska `LK_`-id:t för den lönekörning som transaktionen tillhör. Matchar SVK-LON:117.

Obligatoriskt.

**XML-element:** `lonetransaktion/lonekorningReferens`<br/>
**Datatyp:** string

---

#### SVK-LON:131 - *Personalkategori (transaktion)*

Anställningens personalkategori vid transaktionstillfället, t.ex. `MÅN`. Används tillsammans med löneart-kod för att entydigt identifiera lönearten i registret.

Obligatoriskt.

**XML-element:** `lonetransaktion/personalkategori`<br/>
**Datatyp:** string

---

#### SVK-LON:132 - *Löneart (transaktion)*

Samlingselement för den löneart som transaktionen avser.

Obligatoriskt.

**XML-element:** `lonetransaktion/loneart`<br/>
**Datatyp:** —

---

#### SVK-LON:133 - *Löneartkod (transaktion)*

Löneart-koden. Matchar `loneart/kod` i löneartregistret, tillsammans med SVK-LON:131.

Obligatoriskt.

**XML-element:** `lonetransaktion/loneart/kod`<br/>
**Datatyp:** string

---

#### SVK-LON:134 - *Löneartnamn (transaktion)*

Löneart-namnet som det var vid körningen. Bevaras för tolkningsbarhet.

Obligatoriskt.

**XML-element:** `lonetransaktion/loneart/namn`<br/>
**Datatyp:** string

---

#### SVK-LON:135 - *Period (transaktion)*

Giltighetsperiod för transaktionen, dvs. den tidsperiod lönen avser. Strukturen är identisk med SVK-LON:78–80. Utelämnas om transaktionen saknar periodinformation.

**XML-element:** `lonetransaktion/period`<br/>
**Datatyp:** —

---

#### SVK-LON:136 - *Omfattningsprocent*

Procentuell omfattning, t.ex. vid partiell sjukskrivning eller deltidsarbete. Utelämnas om ej tillämpligt.

**XML-element:** `lonetransaktion/omfattningProcent`<br/>
**Datatyp:** ProcentType

---

#### SVK-LON:137 - *Kvantitet*

Samlingselement för antal, enhet och à-pris. Används när transaktionsbeloppet beräknas som `antal × à-pris`. Utelämnas om transaktionen saknar kvantitetsinformation.

**XML-element:** `lonetransaktion/kvantitet`<br/>
**Datatyp:** —

---

#### SVK-LON:138 - *Antal*

Antal enheter, t.ex. antal timmar.

Obligatoriskt om SVK-LON:137 används.

**XML-element:** `lonetransaktion/kvantitet/antal`<br/>
**Datatyp:** decimal

---

#### SVK-LON:139 - *Enhet*

Enhetsbeteckning, t.ex. `tim` eller `dagar`. Utelämnas om ej tillämpligt.

**XML-element:** `lonetransaktion/kvantitet/enhet`<br/>
**Datatyp:** string

---

#### SVK-LON:140 - *À-pris*

Ersättning per enhet, t.ex. timlön i kronor.

Obligatoriskt om SVK-LON:137 används.

**XML-element:** `lonetransaktion/kvantitet/aPris`<br/>
**Datatyp:** decimal

---

#### SVK-LON:141 - *Belopp*

Transaktionens totala belopp i angiven valuta. Negativa belopp (avdrag, skatt, återbetalning) anges med minustecken.

Obligatoriskt.

**XML-element:** `lonetransaktion/belopp`<br/>
**Datatyp:** decimal

---

#### SVK-LON:142 - *Valuta (transaktion)*

Valutakod. Ska alltid vara `SEK`.

Obligatoriskt.

**XML-element:** `lonetransaktion/valuta`<br/>
**Datatyp:** ValutakodType

---

#### SVK-LON:143 - *Kommentar*

Fritext-kommentar från källsystemet, t.ex. transaktionsradens text i Flex Lön. Utelämnas om ej tillgängligt.

**XML-element:** `lonetransaktion/kommentar`<br/>
**Datatyp:** string

---

#### Exempel 8 – Lönetransaktioner

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:lonetransaktioner
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">

  <svk:lonetransaktion>
    <svk:id>LT_2022_000001</svk:id>
    <svk:transaktionId>80541</svk:transaktionId>
    <svk:lonekorningReferens>LK_2022_000001</svk:lonekorningReferens>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:loneart>
      <svk:kod>100</svk:kod>
      <svk:namn>Månadslön</svk:namn>
    </svk:loneart>
    <svk:period>
      <svk:startdatum>2022-09-01</svk:startdatum>
      <svk:slutdatum>2022-09-30</svk:slutdatum>
    </svk:period>
    <svk:belopp>29500.00</svk:belopp>
    <svk:valuta>SEK</svk:valuta>
  </svk:lonetransaktion>

  <svk:lonetransaktion>
    <svk:id>LT_2022_000002</svk:id>
    <svk:transaktionId>80542</svk:transaktionId>
    <svk:lonekorningReferens>LK_2022_000001</svk:lonekorningReferens>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:loneart>
      <svk:kod>340</svk:kod>
      <svk:namn>Övertid enkel</svk:namn>
    </svk:loneart>
    <svk:period>
      <svk:startdatum>2022-09-01</svk:startdatum>
      <svk:slutdatum>2022-09-30</svk:slutdatum>
    </svk:period>
    <svk:kvantitet>
      <svk:antal>8</svk:antal>
      <svk:enhet>tim</svk:enhet>
      <svk:aPris>221.25</svk:aPris>
    </svk:kvantitet>
    <svk:belopp>1770.00</svk:belopp>
    <svk:valuta>SEK</svk:valuta>
    <svk:kommentar>Övertid v 38–39</svk:kommentar>
  </svk:lonetransaktion>

  <svk:lonetransaktion>
    <svk:id>LT_2022_000003</svk:id>
    <svk:transaktionId>80543</svk:transaktionId>
    <svk:lonekorningReferens>LK_2022_000001</svk:lonekorningReferens>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:loneart>
      <svk:kod>910</svk:kod>
      <svk:namn>Preliminär skatt</svk:namn>
    </svk:loneart>
    <svk:belopp>-8742.00</svk:belopp>
    <svk:valuta>SEK</svk:valuta>
  </svk:lonetransaktion>

</svk:lonetransaktioner>
```

---

### 3.9 Konteringar

Filen `loneutbetalningar/konteringar.xml` innehåller konteringsfördelningar per lönetransaktion. En transaktion kan ha flera konteringsrader om kostnaden fördelas på flera dimensionskombinationer. Rotelement är `konteringar` i SVK-LON-namnrymden.

---

#### Elementlista 8. Konteringar

---

#### SVK-LON:144 - *Konteringar*

Rotelement för konteringsfilen.

Obligatoriskt.

**XML-element:** `svk:konteringar`<br/>
**Datatyp:** —

---

#### SVK-LON:145 - *Kontering*

En enskild konteringsrad. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `kontering`<br/>
**Datatyp:** —

---

#### SVK-LON:146 - *Konterings-id*

Syntetiskt id på formen `K_<år>_<löpnummer>`, t.ex. `K_2022_000001`.

Obligatoriskt.

**XML-element:** `kontering/id`<br/>
**Datatyp:** string

---

#### SVK-LON:147 - *Fördelnings-id*

Källsystemets id för fördelningsgruppen. Möjliggör gruppering av konteringsrader som hör samman.

Obligatoriskt.

**XML-element:** `kontering/fordelningId`<br/>
**Datatyp:** string

---

#### SVK-LON:148 - *Lönetransaktionsreferens*

Det syntetiska `LT_`-id:t för den lönetransaktion som denna kontering avser. Matchar SVK-LON:128.

Obligatoriskt.

**XML-element:** `kontering/lonetransaktionReferens`<br/>
**Datatyp:** string

---

#### SVK-LON:149 - *Procentfördelning (kontering)*

Denna konteringsrads andel av transaktionens totalkostnad i procent.

Obligatoriskt.

**XML-element:** `kontering/procentfordelning`<br/>
**Datatyp:** ProcentType

---

#### SVK-LON:150 - *Dimensioner (kontering)*

Samlingselement för de konteringsdimensioner som gäller för denna rad. Strukturen är identisk med SVK-LON:103–106.

Obligatoriskt.

**XML-element:** `kontering/dimensioner`<br/>
**Datatyp:** —

---

#### Exempel 9 – Konteringar

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:konteringar
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">

  <svk:kontering>
    <svk:id>K_2022_000001</svk:id>
    <svk:fordelningId>12301</svk:fordelningId>
    <svk:lonetransaktionReferens>LT_2022_000001</svk:lonetransaktionReferens>
    <svk:procentfordelning>60</svk:procentfordelning>
    <svk:dimensioner>
      <svk:dimension>
        <svk:namn>Verksamhet</svk:namn>
        <svk:varde>4210</svk:varde>
      </svk:dimension>
      <svk:dimension>
        <svk:namn>Projekt</svk:namn>
        <svk:varde>P-2022-001</svk:varde>
      </svk:dimension>
    </svk:dimensioner>
  </svk:kontering>

  <svk:kontering>
    <svk:id>K_2022_000002</svk:id>
    <svk:fordelningId>12302</svk:fordelningId>
    <svk:lonetransaktionReferens>LT_2022_000001</svk:lonetransaktionReferens>
    <svk:procentfordelning>40</svk:procentfordelning>
    <svk:dimensioner>
      <svk:dimension>
        <svk:namn>Verksamhet</svk:namn>
        <svk:varde>4220</svk:varde>
      </svk:dimension>
      <svk:dimension>
        <svk:namn>Projekt</svk:namn>
        <svk:varde>P-2022-002</svk:varde>
      </svk:dimension>
    </svk:dimensioner>
  </svk:kontering>

</svk:konteringar>
```

---

### 3.10 Referensregister

Referensregistren är tre separata filer i undermappen `register/`. De innehåller statisk referensdata som är stabil för ett givet uttag: utbetalningsgrupper, formelvariabler och lönearter.

---

#### Elementlista 9. Referensregister

---

**Utbetalningsgrupper** (`register/utbetalningsgrupper.xml`)

---

#### SVK-LON:151 - *Utbetalningsgrupper*

Rotelement för utbetalningsgruppsregistret.

Obligatoriskt.

**XML-element:** `svk:utbetalningsgrupper`<br/>
**Datatyp:** —

---

#### SVK-LON:152 - *Utbetalningsgrupp*

En enskild utbetalningsgrupp. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `utbetalningsgrupp`<br/>
**Datatyp:** —

---

#### SVK-LON:153 - *Utbetalningsgrupps-id*

Utbetalningsgruppens unika id, t.ex. `1`. Matchar id:t som refereras från anställningstillägg och lönekörningar.

Obligatoriskt.

**XML-element:** `utbetalningsgrupp/id`<br/>
**Datatyp:** string

---

#### SVK-LON:154 - *Utbetalningsgrupps namn*

Utbetalningsgruppens benämning, t.ex. `Månadsavlönade`.

Obligatoriskt.

**XML-element:** `utbetalningsgrupp/namn`<br/>
**Datatyp:** string

---

**Formelvariabler** (`register/formelvariabler.xml`)

---

#### SVK-LON:155 - *Formelvariabler*

Rotelement för formelvariabelregistret. Registret är en ordlista med namn och beskrivningar av variabler som används i lönearters beräkningsformler. Variablerna har inga värden i registret — de beräknas vid körning.

Obligatoriskt.

**XML-element:** `svk:formelvariabler`<br/>
**Datatyp:** —

---

#### SVK-LON:156 - *Formelvariabel*

En enskild formelvariabel. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `formelvariabel`<br/>
**Datatyp:** —

---

#### SVK-LON:157 - *Variabelnamn*

Variabelns namn som det används i formeluttrycken, t.ex. `HELTIDSLÖN` eller `SEMESTER_FAKTOR`. Ska vara unikt inom registret.

Obligatoriskt.

**XML-element:** `formelvariabel/namn`<br/>
**Datatyp:** string

---

#### SVK-LON:158 - *Variabelbeskrivning*

Mänskligt läsbar beskrivning av variabelns innebörd och beräkningsunderlag.

Obligatoriskt.

**XML-element:** `formelvariabel/beskrivning`<br/>
**Datatyp:** string

---

**Lönearter** (`register/lonearter.xml`)

---

#### SVK-LON:159 - *Lönearter*

Rotelement för löneartregistret.

Obligatoriskt.

**XML-element:** `svk:lonearter`<br/>
**Datatyp:** —

---

#### SVK-LON:160 - *Löneart*

En enskild löneart. Primärnyckeln är kombinationen av `kod` och `personalkategori` — samma kod kan förekomma i varianter för olika personalkategorier. Elementet kan upprepas.

Obligatoriskt. Elementet kan upprepas.

**XML-element:** `loneart`<br/>
**Datatyp:** —

---

#### SVK-LON:161 - *Löneartkod*

Löneartens numeriska kod i Flex Lön, t.ex. `100`.

Obligatoriskt.

**XML-element:** `loneart/kod`<br/>
**Datatyp:** string

---

#### SVK-LON:162 - *Personalkategori (löneart)*

Personalkategorin som lönearten gäller för, t.ex. `MÅN`. Utelämnas om lönesystemet saknar konceptet personalkategori.

**XML-element:** `loneart/personalkategori`<br/>
**Datatyp:** string

---

#### SVK-LON:163 - *Löneartnamn*

Löneartens namn i klartext, t.ex. `Månadslön` eller `Övertid enkel`.

Obligatoriskt.

**XML-element:** `loneart/namn`<br/>
**Datatyp:** string

---

#### SVK-LON:164 - *Beräkningsformel*

Löneartens beräkningsformel bevarad ordagrant från källsystemet, omsluten av ett CDATA-block. Attributet `syntax` anger vilket systems formelspråk formeln är skriven i, t.ex. `Flex`. Utelämnas om lönearten saknar formel.

**XML-element:** `loneart/formel`<br/>
**Datatyp:** string (med attribut `syntax`)

---

#### SVK-LON:165 - *Underlagstyp skatt*

Anger hur lönearten hanteras skattemässigt. Se Värdelista 11.

Obligatoriskt.

**XML-element:** `loneart/underlagstypSkatt`<br/>
**Datatyp:** string

---

#### SVK-LON:166 - *Kontering (löneart)*

Samlingselement för löneartens standardkonton i bokföringen.

**XML-element:** `loneart/kontering`<br/>
**Datatyp:** —

---

#### SVK-LON:167 - *Konto*

Löneartens bokföringskonto.

Obligatoriskt om SVK-LON:166 används.

**XML-element:** `loneart/kontering/konto`<br/>
**Datatyp:** string

---

#### SVK-LON:168 - *Motkonto*

Löneartens motkonto i bokföringen. Utelämnas om ej tillämpligt.

**XML-element:** `loneart/kontering/motkonto`<br/>
**Datatyp:** string

---

#### SVK-LON:169 - *Egenskaper*

Samlingselement för löneartens egenskaper avseende sociala avgifter och pensionsgrundande information.

**XML-element:** `loneart/egenskaper`<br/>
**Datatyp:** —

---

#### SVK-LON:170 - *FORA-grundande*

Anger om lönearten är grundande för FORA-försäkringar. Utelämnas om ej tillämpligt (tolkas som `false`).

**XML-element:** `loneart/egenskaper/foraGrundande`<br/>
**Datatyp:** boolean

---

#### SVK-LON:171 - *KAP-KL-grundande*

Anger om lönearten är grundande för KAP-KL-pensionen. Utelämnas om ej tillämpligt.

**XML-element:** `loneart/egenskaper/kapKlGrundande`<br/>
**Datatyp:** boolean

---

#### SVK-LON:172 - *Ej socialavgiftsgrundande*

Anger om lönearten är undantagen från socialavgifter, t.ex. vissa ersättningar. Utelämnas om ej tillämpligt (tolkas som `false`, dvs. lönearten är socialavgiftsgrundande).

**XML-element:** `loneart/egenskaper/ejSocialavgiftsgrundande`<br/>
**Datatyp:** boolean

---

#### SVK-LON:173 - *Kostnadsavdrag socialavgifter*

Samlingselement för lönearter med partiellt kostnadsavdrag på socialavgifter (t.ex. sjuklön). Utelämnas om ej tillämpligt.

**XML-element:** `loneart/egenskaper/kostnadsavdragSocAvg`<br/>
**Datatyp:** —

---

#### SVK-LON:174 - *Kostnadsavdragsprocent*

Procentsatsen för kostnadsavdraget på socialavgifter.

Obligatoriskt om SVK-LON:173 används.

**XML-element:** `loneart/egenskaper/kostnadsavdragSocAvg/procent`<br/>
**Datatyp:** ProcentType

---

#### Exempel 10 – Utbetalningsgrupper

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:utbetalningsgrupper
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">
  <svk:utbetalningsgrupp>
    <svk:id>1</svk:id>
    <svk:namn>Månadsavlönade</svk:namn>
  </svk:utbetalningsgrupp>
  <svk:utbetalningsgrupp>
    <svk:id>2</svk:id>
    <svk:namn>Timanställda</svk:namn>
  </svk:utbetalningsgrupp>
</svk:utbetalningsgrupper>
```

---

#### Exempel 11 – Formelvariabler

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:formelvariabler
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">
  <svk:formelvariabel>
    <svk:namn>HELTIDSLÖN</svk:namn>
    <svk:beskrivning>Avtalad månadslön vid heltid i kronor.</svk:beskrivning>
  </svk:formelvariabel>
  <svk:formelvariabel>
    <svk:namn>SEMESTER_FAKTOR</svk:namn>
    <svk:beskrivning>Semesterlönefaktor beräknad enligt sammalöneregeln.</svk:beskrivning>
  </svk:formelvariabel>
</svk:formelvariabler>
```

---

#### Exempel 12 – Lönearter

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svk:lonearter
    xmlns:svk="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1">

  <svk:loneart>
    <svk:kod>100</svk:kod>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:namn>Månadslön</svk:namn>
    <svk:formel syntax="Flex"><![CDATA[HELTIDSLÖN * SYSS_GRAD / 100]]></svk:formel>
    <svk:underlagstypSkatt>Tabellskatt</svk:underlagstypSkatt>
    <svk:kontering>
      <svk:konto>7010</svk:konto>
      <svk:motkonto>2710</svk:motkonto>
    </svk:kontering>
    <svk:egenskaper>
      <svk:foraGrundande>true</svk:foraGrundande>
      <svk:kapKlGrundande>true</svk:kapKlGrundande>
    </svk:egenskaper>
  </svk:loneart>

  <svk:loneart>
    <svk:kod>610</svk:kod>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:namn>Sjuklön dag 2–14</svk:namn>
    <svk:underlagstypSkatt>Tabellskatt</svk:underlagstypSkatt>
    <svk:kontering>
      <svk:konto>7090</svk:konto>
    </svk:kontering>
    <svk:egenskaper>
      <svk:ejSocialavgiftsgrundande>true</svk:ejSocialavgiftsgrundande>
      <svk:kostnadsavdragSocAvg>
        <svk:procent>80</svk:procent>
      </svk:kostnadsavdragSocAvg>
    </svk:egenskaper>
  </svk:loneart>

  <svk:loneart>
    <svk:kod>920</svk:kod>
    <svk:personalkategori>MÅN</svk:personalkategori>
    <svk:namn>Friskvård skattefri</svk:namn>
    <svk:underlagstypSkatt>Ej Skatt</svk:underlagstypSkatt>
    <svk:egenskaper>
      <svk:foraGrundande>false</svk:foraGrundande>
      <svk:kapKlGrundande>false</svk:kapKlGrundande>
      <svk:ejSocialavgiftsgrundande>true</svk:ejSocialavgiftsgrundande>
    </svk:egenskaper>
  </svk:loneart>

</svk:lonearter>
```

---

## Värdelistor

---

### Värdelista 1 – Namnmönster för recordId

| Dokumenttyp | Mönster | Exempel |
|---|---|---|
| Organisation | `ORG_<organisationsnummer>` | `ORG_1234567890` |
| Anställning | `F_<anstallningsnummer>` | `F_20` |
| Arbetstagare | `A_<personnummer>` | `A_197606280696` |
| Person | `P_<personnummer>` | `P_197606280696` |

Personnummer anges utan bindestreck. RecordId är stabila över årsuttag.

---

### Värdelista 2 – Underhållsstatus (maintenanceStatus)

| Värde | Förklaring |
|---|---|
| `new` | Dokumentet skapas för första gången. |
| `revised` | Dokumentet är en uppdaterad version. Används vid reguljära årsuttag. |
| `deleted` | Dokumentet har annullerats (används ej i reguljära leveranser). |

---

### Värdelista 3 – Händelsetyp (eventType)

| Värde | Förklaring |
|---|---|
| `created` | Dokumentet skapades. Minst en `maintenanceEvent` med detta värde krävs. |
| `revised` | Dokumentet ändrades. |
| `derived` | Dokumentet härleddes från ett annat dokument. |

---

### Värdelista 4 – Agenttyp (agentType)

| Värde | Förklaring |
|---|---|
| `human` | Händelsen utfördes av en person. |
| `machine` | Händelsen utfördes av ett system, t.ex. exportscriptet. Används vid automatiserade årsuttag. |

---

### Värdelista 5 – Enhetstyp (entityType)

| Värde | Användning |
|---|---|
| `corporateBody` | Organisation. |
| `person` | Person, Arbetstagare. |

---

### Värdelista 6 – Lönetyp (salaryType)

| Värde | Förklaring |
|---|---|
| `monthlyPay` | Fast månadslön. |
| `hourlyWage` | Timlön. |

---

### Värdelista 7 – Anställningsform

Rekommenderade värden. Öppen sträng — systemspecifika varianter tillåts.

| Värde | Förklaring |
|---|---|
| `Tillsvidareanställd` | Tillsvidareanställning utan slutdatum. |
| `Visstidsanställd` | Tidsbegränsad anställning. |
| `Provanställd` | Anställning under prövotid. |
| `Vikariat` | Vikarierande anställning. |
| `Timanställd` | Anställning med timbaserad ersättning. |

---

### Värdelista 8 – Löneform

Rekommenderade värden. Öppen sträng.

| Värde | Förklaring |
|---|---|
| `Månadslön` | Fast månadslön. |
| `Timlön` | Lön per arbetad timme. |

---

### Värdelista 9 – Avslutsorsak

Rekommenderade värden. Öppen sträng — Flex-specifika varianter tillåts.

| Värde | Förklaring |
|---|---|
| `Egen begäran` | Arbetstagaren har själv sagt upp anställningen. |
| `Pensionsavgång` | Anställning avslutad i samband med pensionering. |
| `Uppsagd pga arbetsbrist` | Arbetsgivaren har sagt upp på grund av arbetsbrist. |
| `Uppsagd av personliga skäl` | Arbetsgivaren har sagt upp på personliga skäl. |
| `Tidsbegränsad anställning upphör` | Visstidsanställning löper ut. |
| `Avliden` | Arbetstagarens död. |

---

### Värdelista 10 – Värdetyp för lönetillägg (varde/@typ)

| Värde | Förklaring | Valuta |
|---|---|---|
| `belopp` | Värdet är ett kronbelopp. `valuta` ska anges. | Krävs |
| `faktor` | Värdet är en multiplikationsfaktor, t.ex. en uppehållsfaktor. `valuta` ska inte anges. | Förbjudet |

---

### Värdelista 11 – Underlagstyp skatt

| Värde | Förklaring |
|---|---|
| `Tabellskatt` | Lönearten beskattas enligt skattetabell. |
| `Engångsskatt` | Lönearten beskattas som engångsbelopp (t.ex. retroaktiv lön). |
| `Ej Skatt` | Lönearten är skattefri (t.ex. skattefri friskvård). |

---

### Värdelista 12 – entityId-localType för Organisation

| Värde | Förklaring | Exempel |
|---|---|---|
| `ORG` | Organisationsnummer enligt Bolagsverket (10 siffror utan bindestreck). | `1234567890` |
| `FlexForetagsnummer` | Arbetsgivarens interna id i Flex Lön. | `42` |
| `FORA` | Försäkringsnummer hos FORA. | `987654` |
| `KAPKL` | Kundnummer hos KAP-KL. | `3` |

---

### Värdelista 13 – entityId-localType för Person

| Värde | Förklaring | Format |
|---|---|---|
| `PersonalIdentityNumber` | Svenskt personnummer. | `YYYYMMDD-NNNN` |
| `CoordinationNumber` | Svenskt samordningsnummer. Dagsiffran är födelsedag + 60. | `YYYYMMDD-NNNN` |

---

*Detta dokument är en del av Svenska kyrkans anpassning av FGS Personal. Det normativa grunddokumentet är `svk-fgs-personal-anpassning.md`. Schemat distribueras som `SVK-personal-lon.xsd` och valideringsreglerna som `svk-personal-lon.sch`.*
