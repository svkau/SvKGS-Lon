# Svenska kyrkans anpassning av FGS Personal

**Förvaltningsgemensam specifikation (FGS) för Personalinformation — lokal anpassning för lönearkivering ur Flex Lön**

| | |
|---|---|
| Version | 1.0 |
| Datum | [Åååå-mm-dd] |
| Baseras på | FGS Personal RAFGS2V1.0, Riksarkivet, februari 2019 |
| Utfärdare | Svenska kyrkan |
| Kontakt | [e-post] |

---

## Innehåll

1. [Inledning](#1-inledning)
2. [Omfattning och avgränsningar](#2-omfattning-och-avgränsningar)
3. [Ändrade kardinaliteter](#3-ändrade-kardinaliteter)
4. [Egna värdelistor](#4-egna-värdelistor)
5. [Egna XML-scheman](#5-egna-xml-scheman)
6. [Paketstruktur](#6-paketstruktur)
7. [Specifika tolkningar och konventioner](#7-specifika-tolkningar-och-konventioner)
8. [Validering](#8-validering)
9. [Versionshistorik](#9-versionshistorik)
10. [Bilaga A: XSD-schema](#bilaga-a-xsd-schema)
11. [Bilaga B: Mappning CSV till XML](#bilaga-b-mappning-csv-till-xml)

---

## 1. Inledning

### 1.1 Syfte

Detta dokument beskriver Svenska kyrkans anpassning av den förvaltningsgemensamma specifikationen FGS Personal (RAFGS2V1.0) för arkivering av personal- och löneinformation ur lönesystemet Flex Lön. Anpassningen möjliggör att lagstadgad bevarandeinformation från Svenska kyrkans arbetsgivare överförs till e-arkivet i ett strukturerat och förvaltningsgemensamt format.

### 1.2 Bakgrund

FGS Personal tillhandahåller metadata för organisation, organisatorisk enhet, anställning, arbetstagare och person. Grundspecifikationen är medvetet avgränsad och innehåller inte element för detaljerad löneinformation — specifikationen säger uttryckligen att element saknas för "exempelvis förmåner, övertidsersättning, tjänsteresor och lönearter". För att möjliggöra fullständig arkivering av Svenska kyrkans löneinformation utökas FGS:en därför med ett tilläggsschema.

### 1.3 Giltighet

Anpassningen gäller tillsammans med grundspecifikationen RAFGS2V1.0 och Tillägget RAFGS2V1.0A20190225. De ursprungliga FGS-dokumenten ska tillämpas där inget annat anges i detta dokument.

### 1.4 Läsanvisning

Dokumentet riktar sig primärt till systemleverantörer som utvecklar export från Flex Lön till arkivpaket enligt anpassningen. Sekundära målgrupper är e-arkivadministratörer som tar emot leveranser, och framtida arkivanvändare som ska tolka arkiverat material.

För grundläggande förståelse av FGS-konceptet hänvisas till Riksarkivets dokument "Introduktion till förvaltningsgemensamma specifikationer (FGS) FGS Personal".

---

## 2. Omfattning och avgränsningar

### 2.1 Översikt

Anpassningen omfattar överföring av hela personal- och löneinformationen för en arbetsgivare ett givet år. Arkivpaketet innehåller både FGS-compliant delar (organisation, anställning, arbetstagare, person) och kompletterande delar som specificeras i detta dokument (löneutbetalningar, lönearts- och formelvariabelregister, anställningsspecifik lönestruktur).

### 2.2 Använda delar av FGS Personal

| FGS-del | Används | Kommentar |
|---|---|---|
| Organisation | Ja | Fullt stöd via EAC-CPF. Identifieringar kompletteras med egna localType-värden för Flex företagsnummer, FORA och KAP-KL. |
| Organisatorisk enhet | Nej | Svenska kyrkans arbetsgivare är GAS-enheter utan interna organisatoriska enheter i Flex Lön. Nivån utelämnas helt i anpassningen. |
| Anställning | Ja, partiellt | Se avsnitt 2.3 nedan. |
| Arbetstagare | Ja, minimalt | Dokumentet innehåller endast kontrolluppgifter och relationer. Inga skatteuppgifter, anhöriga eller bankuppgifter exporteras, enligt verksamhetsbeslut. |
| Person | Ja | Fullt stöd via EAC-CPF med utökade obligatoriska element, se avsnitt 3. |

### 2.3 Delvis användning av Anställning

Vissa anställningsrelaterade element i FGS Personal används medvetet inte, då motsvarande data hanteras i tilläggsschemat med högre upplösning. Detta är en strikt partitionering — samma data förekommer inte på båda ställena.

| FGS-element | Används | Motsvarande data i anpassningen |
|---|---|---|
| `employmentId` | Ja | Anställningsnummer från Flex |
| `positions` | Ja | Befattning med BKSK-kodning |
| `salaryAgreements` | Ja | Endast avtalad månadslön eller timlön (grundlön). Sysselsättningsgrad, heltidsmått och lönetillägg hanteras i tilläggsschemat. |
| `employmentDates` | Nej | Hanteras per anställningsperiod i tilläggsschemat. |
| `typeOfEmployment` | Nej | Hanteras per anställningsperiod i tilläggsschemat. |
| `employmentTerminations` | Nej | Hanteras per anställningsperiod i tilläggsschemat. |
| `weeklyWorkingTime` | Nej | Hanteras som heltidsmått i tilläggsschemat. |
| `typeOfWorkingTime` | Nej | Inte tillgänglig i Flex-uttaget. |
| `relations` | Ja | Till organisation och arbetstagare. |
| `additionalElements/additionalXMLData` | Ja | Omsluter tilläggsschemat. |

Övriga frivilliga FGS-element (firstWorkDay, contracts, agreements, workplaces, jobLocations, yearlyVacationDays, sideLineOccupations, fringeBenefits, paydays, retirementRegulations, testimonials, references) används inte då motsvarande information inte ingår i Flex-uttaget.

### 2.4 Information utanför FGS Personal

Följande informationstyper hanteras helt utanför FGS Personal, som separata dokument i arkivpaketet:

- Lönekörningar (en per anställd och utbetalningstillfälle)
- Lönetransaktioner (en per transaktionsrad)
- Transaktionskonteringar (bokföringsfördelningar per transaktion)
- Lönearter (referensregister)
- Formelvariabler (referensregister med definitioner av variabler som används i lönearters beräkningsformler)
- Utbetalningsgrupper (referensregister)

Dessa hanteras i sina egna XML-filer enligt tilläggsschemat, se avsnitt 5 och 6.

### 2.5 Lönespecifikationer

Utöver XML-strukturerad data levereras lönespecifikationer i HTML-format, en per anställd och utbetalningstillfälle. Dessa lagras i undermappen `lonespecifikationer/` och refereras från motsvarande `lonekorning`-element.

---

## 3. Ändrade kardinaliteter

Detta avsnitt listar element där anpassningen skärper kardinaliteter jämfört med FGS Personal. Enligt FGS-tillägget får obligatoriska element inte göras frivilliga — endast skärpning är tillåten.

### 3.1 Organisation

Inga kardinalitetsändringar. Tillägg sker via egen localType-värdelista (se avsnitt 4).

### 3.2 Person

| Element | FGS-kard. | SVK-kard. | Motivering |
|---|---|---|---|
| `entityId` med localType `PersonalIdentityNumber` eller `CoordinationNumber` | 0..* | 1..* (minst en förekomst med någon av de två localType-värdena) | Personnummer eller samordningsnummer är alltid tillgängligt i Flex Lön och utgör primär identifierare i arkivet. |
| `nameEntry` med localType `forename` | 0..1 | 1 | Förnamn lagras separat i Flex och ska alltid anges. |
| `nameEntry` med localType `surname` | 0..1 | 1 | Efternamn lagras separat i Flex och ska alltid anges. |
| `localDescription` med localType `nationality` | 0..* | 1..1 | Nationalitet finns i Flex och är obligatorisk referensdata. |

### 3.3 Anställning

| Element | FGS-kard. | SVK-kard. | Motivering |
|---|---|---|---|
| `employmentId` | 0..1 | 1 | Anställningsnummer från Flex används som obligatorisk identifierare. |
| `positions/position` | 0..* | 1..* | Varje anställning har minst en registrerad befattning. |

### 3.4 Arbetstagare

Inga kardinalitetsändringar. Dokumentet är medvetet hållt minimalt med endast kontrolluppgifter och relationer.

---

## 4. Egna värdelistor

### 4.1 Översikt

Anpassningen använder FGS Personals grundvärdelistor oförändrade där de räcker. Nedan listas endast lokala tillägg.

### 4.2 Utökning av entityId-localType (Organisation)

| Värde | Förklaring | Exempel |
|---|---|---|
| `ORG` | Organisationsnummer enligt Bolagsverket (ärvt från FGS). | `098765-4321` |
| `FlexForetagsnummer` | Flex:s interna företagsnummer, unikt inom Flex Lön. | `921` |
| `FORA` | Försäkringsnummer hos FORA för kollektivavtalade försäkringar. | `123456` |
| `KAPKL` | Kundnummer hos KAP-KL för pensionshantering. | `1` |

### 4.3 Utökning av entityId-localType (Person)

| Värde | Förklaring | Exempel |
|---|---|---|
| `PersonalIdentityNumber` | Svenskt personnummer på formatet YYYYMMDD-NNNN. | `19760628-0696` |
| `CoordinationNumber` | Svenskt samordningsnummer på formatet YYYYMMDD-NNNN där DD = födelsedag + 60. | `19770406-0060` |

### 4.4 BKSK (Befattningskod Svenska kyrkan)

Kodverket används i `positions/position/term/@source="BKSK"` för att kvalificera befattningskoden som tillhörande Svenska kyrkans egen kodstandard.

| Attribut | Värde |
|---|---|
| Source | `BKSK` |
| Deklarationsnivå | `ownValueListDeclaration` i control-avsnittet |
| Citation | [URL till kodverksdokumentation] |

Exempel på användning:

```xml
<position>
    <term source="BKSK" code="421005">Kyrkvaktmästare</term>
</position>
```

### 4.5 Värdelistor i tilläggsschemat

Tilläggsschemat använder öppna strängtyper (`xs:string`) för värdelistor, med rekommenderade värden dokumenterade här. Strikt validering mot värdelista sker vid behov i Schematron.

**4.5.1 Anställningsform** (`anstallningsform` i anställningsperiod)

| Värde | Förklaring |
|---|---|
| `Tillsvidareanställd` | Tillsvidareanställning utan slutdatum. |
| `Visstidsanställd` | Tidsbegränsad anställning. |
| `Provanställd` | Anställning under prövotid. |
| `Vikariat` | Vikarierande anställning. |
| `Timanställd` | Anställning med timbaserad ersättning. |

**4.5.2 Löneform** (`loneform` i anställningsperiod)

Motsvarar FGS-värdelistan `vcPAYMENTFREQUENCY` men anges som öppen sträng. Rekommenderade värden:

| Värde | Förklaring |
|---|---|
| `Månadslön` | Fast månadslön. |
| `Timlön` | Lön per arbetad timme. |

**4.5.3 Avslutsorsak** (`avslutsorsak` i anställningsperiod)

Speglar FGS-värdelistan `vcTYPEOFTERMINATION` men anges som öppen sträng för Flex-specifika varianter. Rekommenderade värden:

| Värde | Förklaring |
|---|---|
| `Egen begäran` | Arbetstagaren har själv sagt upp anställningen. |
| `Pensionsavgång` | Anställning avslutad i samband med pensionering. |
| `Uppsagd pga arbetsbrist` | Arbetsgivaren har sagt upp på grund av arbetsbrist. |
| `Uppsagd av personliga skäl` | Arbetsgivaren har sagt upp på personliga skäl. |
| `Avliden` | Arbetstagarens död. |

**4.5.4 Underlagstyp skatt** (`underlagstypSkatt` i löneart)

| Värde | Förklaring |
|---|---|
| `Tabellskatt` | Lönearten beskattas enligt skattetabell. |
| `Engångsskatt` | Lönearten beskattas som engångsbelopp. |
| `Ej Skatt` | Lönearten beskattas inte. |

**4.5.5 Värdetyp i lönetillägg** (`typ`-attribut på `varde`)

| Värde | Förklaring |
|---|---|
| `belopp` | Värdet är ett kronbelopp och förutsätter att `valuta` anges. |
| `faktor` | Värdet är en multiplikationsfaktor (t.ex. uppehållsfaktor). `valuta` ska inte anges. |

---

## 5. Egna XML-scheman

### 5.1 Namnrymd

Tilläggsschemat använder namnrymden:

```
https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1
```

Version ingår i namnrymden för att möjliggöra framtida icke-bakåtkompatibla ändringar utan att äldre arkivpaket påverkas.

### 5.2 Användningskontexter

Schemat används i två olika kontexter inom arkivpaketet:

**Inuti FGS-anställning via additionalXMLData**

Elementet `anstallningstillagg` hängs in under `employmentDescription/additionalElements/additionalXMLData` i varje FGS-anställningsdokument. Det innehåller anställningsspecifika tidsserier och konteringsinformation.

**Som separata dokument i paketet**

Följande är egna rotelement i sina respektive XML-filer:
- `lonekorningar` i loneutbetalningar/lonekorningar.xml
- `lonetransaktioner` i loneutbetalningar/lonetransaktioner.xml
- `konteringar` i loneutbetalningar/konteringar.xml
- `utbetalningsgrupper` i register/utbetalningsgrupper.xml
- `formelvariabler` i register/formelvariabler.xml
- `lonearter` i register/lonearter.xml

### 5.3 Schemadokument

Det kompletta XSD-schemat återfinns i Bilaga A och distribueras separat som filen `svk-personal-lon-v1.xsd`.

### 5.4 Innehåll i anstallningstillagg

Elementet grupperar alla tillägg till en FGS-anställning:

| Underelement | Beskrivning |
|---|---|
| `utbetalningsgruppReferens` | Referens till utbetalningsgrupp i registret. |
| `personalkategori` | Anställningens personalkategori (t.ex. MÅN, TIM). |
| `anstallningsperioder` | Tidsserier av anställningsperioder med form, löneform och avslutsorsak. |
| `sysselsattningsgrader` | Tidsserier av sysselsättningsgrad i procent. |
| `heltidsmatt` | Tidsserier av heltidsmått (timmar per vecka). |
| `lonetillagg` | Tidsserier av lönetillägg (belopp eller faktor). |
| `kostnadsfordelningar` | Förhandsdefinierade fördelningar av lön på konteringsdimensioner. |
| `standardkonteringar` | Per-dimension-fördelningar (kallat "hemkontering" i Flex). |

---

## 6. Paketstruktur

### 6.1 Generella principer

Varje arkivpaket täcker en arbetsgivare ett visst år och innehåller den informationen som är relevant för det året plus historisk data som överlappar. Paketet är självförsörjande — referenser mellan paketgränser undviks, och redundans accepteras som en avvägning för tillgänglighet.

Arkivpaketet levereras inom Svenska kyrkans variant av FGS Paket som yttre hölje.

### 6.2 Katalogstruktur

```
[paketidentifierare]/
├── manifest.xml                 (FGS Paket)
├── organisation/
│   └── organisation.xml         (FGS Personal, EAC-CPF)
├── anstallningar/
│   ├── F_1.xml                  (en per anställning under året)
│   ├── F_20.xml
│   └── ...
├── arbetstagare/
│   ├── A_197606280696.xml       (en per arbetstagare)
│   └── ...
├── personer/
│   ├── P_197606280696.xml       (en per person)
│   └── ...
├── loneutbetalningar/
│   ├── lonekorningar.xml
│   ├── lonetransaktioner.xml
│   └── konteringar.xml
├── register/
│   ├── lonearter.xml
│   ├── formelvariabler.xml
│   └── utbetalningsgrupper.xml
└── lonespecifikationer/
    └── [organisationsnummer]_[personnummer]_[anstallningsnummer]_[period]_lonespec.html
```

### 6.3 Namnkonventioner för recordId

FGS-dokument har unika recordId som bygger på stabila identifierare från källdata:

| Dokumenttyp | recordId-mönster | Exempel |
|---|---|---|
| Organisation | `ORG_<organisationsnummer>` | `ORG_0987654321` |
| Anställning | `F_<anstallningsnummer>` | `F_20` |
| Arbetstagare | `A_<personnummer>` | `A_197606280696` |
| Person | `P_<personnummer>` | `P_197606280696` |

RecordId-värdena är stabila över årsuttag — samma anställning har samma recordId i alla paket där den ingår.

### 6.4 Namnkonventioner för syntetiska id i löneutbetalningar

Löneutbetalningsfiler använder syntetiska id med årtalsprefix för att säkerställa unikhet vid ackumulation över årgångar:

| Objekttyp | Id-mönster | Exempel |
|---|---|---|
| Lönekörning | `LK_<år>_<löpnummer>` | `LK_2022_000001` |
| Lönetransaktion | `LT_<år>_<löpnummer>` | `LT_2022_000001` |
| Kontering | `K_<år>_<löpnummer>` | `K_2022_000001` |

Årtalet är paketets uttagsår, inte händelsens år. Löpnummer börjar om från 1 i varje nytt årsuttag. Id:na är paketlokala — referenser mellan paket görs via de naturliga nycklarna (lonekorningsnummer, transaktion_id, fordelning_id).

### 6.5 Namnkonventioner för lönespecifikationsfiler

Lönespecifikationer namnges enligt mönstret:

```
[organisationsnummer]_[personnummer]_[anstallningsnummer]_[period]_lonespec.html
```

Exempel: `0987654321_197606280696_20_202009_lonespec.html`

Namngivningen möjliggör återsökning direkt via filnamn utan att gå via XML-indexering.

---

## 7. Specifika tolkningar och konventioner

### 7.1 Tidsserier för anställningsdata

Data som förändras över tid (grundlön, sysselsättningsgrad, heltidsmått, lönetillägg, kostnadsfördelning) lagras som tidsseriepostningar med en post per giltighetsperiod. Varje post har:

- Ett unikt id inom sin typ
- Ett värde eller attributvärden
- En giltighetsperiod med startdatum och valfritt slutdatum

För poster som löper tills vidare utelämnas slutdatum helt. Fiktiva "tillsvidare"-datum (t.ex. 2049-01-01) från källsystemet översätts till utelämnat slutdatum vid export.

### 7.2 Datumformat

Datum anges enligt XSD `xs:date` (YYYY-MM-DD). Flex:s CSV-export använder `YYYY-MM-DDTHH:MM:SS` med konstant tid `T00:00:00`. Vid XML-export strippas tid-komponenten.

### 7.3 Hantering av skyddad identitet

Personer med sekretessmarkering eller kvarskrivning bevaras fullt ut i arkivpaketet med samtliga identifierande uppgifter. Anpassningen markerar status via `descriptiveNote` i Person-dokumentets `identity`-element med texten "Skyddad identitet".

Åtkomstbegränsning hanteras i e-arkivets söklager genom att söktjänster kan exkludera eller maskera personer där skyddsmarkering finns. Själva arkivpaketet innehåller fullständig information.

### 7.4 Anställning kontra anställningsperiod

Flex Lön representerar förändringar i anställningsvillkor som nya anställningsperioder inom en befintlig anställning, snarare än som nya anställningar. En anställning kan därför ha flera anställningsperioder, var och en med egen anställningsform, löneform och eventuell avslutsorsak.

Anpassningen behandlar detta strikt partitionerat:

- FGS-anställningsdokumentet innehåller *inga* datum, anställningsform eller avslutsorsak.
- All period-relaterad information finns enbart i tilläggsschemats `anstallningsperioder`.

### 7.5 Partitionering av löneinformation

Grundlön och övriga lönekomponenter hanteras på olika platser:

| Komponent | Plats | Motivering |
|---|---|---|
| Grundlön (månadslön eller timlön) | FGS `salaryAgreements` | Avtalad baslön. FGS:ens struktur passar direkt. |
| Sysselsättningsgrad | Tilläggsschema | FGS har ingen tidsseriestruktur för sysselsättning. |
| Heltidsmått | Tilläggsschema | FGS `weeklyWorkingTime` tillåter inte tidsserier. |
| Lönetillägg | Tilläggsschema | Inte täckt av FGS. |

Grundlönshistorik uttrycks som flera `salaryAgreement`-element med olika `salaryPeriod`. Samma lönebelopp förekommer inte på båda ställena — partitioneringen är strikt och utan redundans.

### 7.6 Tabellnär struktur för löneutbetalningar

Lönekörningar, lönetransaktioner och konteringar lagras som platta listor i sina respektive filer, inte nästlade i anställningsdokument. Referenser mellan filer sker via syntetiska id (inom paketet) och via naturliga nycklar (för externa referenser).

Denna tabellnära struktur speglar källdatans CSV-format och möjliggör effektiv strömning, söktabellinläsning och delvis läsning utan att behöva läsa hela paketet.

### 7.7 Negativa belopp

Lönetransaktioner med negativt belopp (skatt, avdrag, skuld) representeras med minustecken framför `belopp`-värdet. Inga typ- eller statusindikatorer används för att skilja positiva från negativa transaktioner. Detta speglar Flex:s egen representation.

### 7.8 Namngivning: "standardkontering" kontra "hemkontering"

I Flex Lön används benämningen "hemkontering" för den förhandsdefinierade konteringsregel som tillämpas per dimension och anställning. Denna anpassning använder istället benämningen "standardkontering" i XML-schemat, av två skäl:

1. "Hemkontering" är inte en vedertagen term utanför Flex-kontext och kan försvåra förståelsen för framtida läsare.
2. "Standardkontering" beskriver funktionen mer direkt — det är den kontering som används som standard när inget annat anges.

Vid mappning från Flex-data motsvarar alltså `hemkontering` → `<standardkontering>`.

### 7.9 Löneartsnycklar

Lönearter identifieras i registret via kombinationen `kod + personalkategori`. Samma löneart-kod kan förekomma i flera varianter för olika personalkategorier, med olika konton eller beräkningar. Transaktioner som refererar till en löneart måste därför inkludera både `personalkategori` och löneart-koden för att entydigt identifiera rätt löneart.

### 7.10 Bevarande av beräkningsformler

Lönearter i Flex innehåller beräkningsformler som kan vara omfattande. Formlerna bevaras ordagrant i elementet `formel`, omslutet av CDATA-block för att hantera specialtecken som `<`, `>`, `¤` (radseparator i Flex:s syntax) och svenska tecken.

Formlernas syntax är Flex-specifik och dokumenteras i Flex:s egen dokumentation. Anpassningen säkerställer bevarandet av formlerna som bevis på hur beräkningen var definierad vid arkiveringen, men tolkning kräver kunskap om Flex-syntaxen.

Registret `formelvariabler.xml` tillhandahåller mänskligt läsbara beskrivningar av de variabler som används i formlerna. Detta utgör stödmaterial för framtida tolkning.

### 7.11 Utelämnande av tomma värden

Element som saknar värde i källdata utelämnas i XML-exporten snarare än skrivs som tomma. Detta gäller alla frivilliga element. Validering av att obligatoriska element faktiskt har värden sker via XSD (strukturellt) och Schematron (där villkorliga regler krävs).

---

## 8. Validering

### 8.1 Valideringsnivåer

Arkivpaket valideras i tre nivåer:

**Strukturell validering (XSD):** Säkerställer att XML-dokumentens struktur, elementhierarki och datatyper följer schemat.

**Regelbaserad validering (Schematron):** Säkerställer affärsregler som inte kan uttryckas i XSD, såsom värdelistebegränsningar, villkorliga regler och referensintegritet.

**Manuell kvalitetskontroll:** Stickprovsgranskning av paket för att upptäcka fel som inte fångas av automatisk validering.

### 8.2 Schematron-regler

Följande typer av regler implementeras i Schematron:

**Värdelistor**
- `anstallningsform` antar värden från rekommenderad värdelista i 4.5.1.
- `loneform` antar värden från rekommenderad värdelista i 4.5.2.
- `avslutsorsak` antar värden från rekommenderad värdelista i 4.5.3.
- `underlagstypSkatt` antar värden från värdelista i 4.5.4.
- `typ`-attribut på `varde` antar värden från värdelista i 4.5.5.

**Villkorliga regler**
- Lönetillägg med `varde typ="belopp"` måste ha `valuta` angiven.
- Lönetillägg med `varde typ="faktor"` får inte ha `valuta` angiven.
- Person måste ha minst en `entityId` med localType `PersonalIdentityNumber` eller `CoordinationNumber`.
- Person måste ha `localDescription localType="nationality"`.

**Referensintegritet**
- `lonekorningReferens` i en lönetransaktion matchar en existerande lönekörning.
- `lonetransaktionReferens` i en kontering matchar en existerande lönetransaktion.
- `utbetalningsgruppReferens` matchar en existerande utbetalningsgrupp i registret.

**Unikhet**
- Kombinationen `kod + personalkategori` är unik inom `lonearter`.
- `namn` är unikt inom `formelvariabler`.
- Syntetiska id är unika inom sin fil.

**Summering**
- Procentfordelningar inom samma `kostnadsfordelningId` summerar till 100.
- Procentfordelningar inom samma `standardkontering` summerar till 100.

### 8.3 Leverantörens ansvar

Systemleverantören ansvarar för att exporten producerar validerande paket. Validering vid avsändande och mottagande rekommenderas för att upptäcka avvikelser tidigt.

---

## 9. Versionshistorik

| Version | Datum | Ändring |
|---|---|---|
| 1.0 | [Åååå-mm-dd] | Första publicerade versionen. |

---

## Bilaga A: XSD-schema

Det kompletta XML-schemat för tilläggsdomänen följer nedan. Schemat distribueras separat som filen `svk-personal-lon-v1.xsd`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1"
           targetNamespace="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1"
           elementFormDefault="qualified"
           version="1.0">
    
    <xs:annotation>
        <xs:documentation xml:lang="sv">
            Svenska kyrkans tilläggsschema till FGS Personal för löneinformation
            ur Flex Lön. Omfattar anställningstillägg (används inom FGS
            additionalXMLData), löneutbetalningar som separata dokument,
            och referensregister.
        </xs:documentation>
    </xs:annotation>
    
    
    <!-- ================================================================ -->
    <!-- GEMENSAMMA TYPER                                                 -->
    <!-- ================================================================ -->
    
    <xs:complexType name="GiltighetsperiodType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">
                Tidsperiod under vilken posten är giltig. Slutdatum utelämnas
                för poster som löper tills vidare.
            </xs:documentation>
        </xs:annotation>
        <xs:sequence>
            <xs:element name="startdatum" type="xs:date"/>
            <xs:element name="slutdatum"  type="xs:date" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:simpleType name="ValutakodType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">Valutakod enligt ISO 4217.</xs:documentation>
        </xs:annotation>
        <xs:restriction base="xs:string">
            <xs:pattern value="[A-Z]{3}"/>
        </xs:restriction>
    </xs:simpleType>
    
    <xs:simpleType name="ProcentType">
        <xs:restriction base="xs:decimal">
            <xs:minInclusive value="0"/>
            <xs:maxInclusive value="100"/>
        </xs:restriction>
    </xs:simpleType>
    
    <xs:complexType name="DimensionType">
        <xs:sequence>
            <xs:element name="namn"  type="xs:string"/>
            <xs:element name="varde" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="DimensionerType">
        <xs:sequence>
            <xs:element name="dimension" type="DimensionType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="AnstallningReferensType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">
                Referens till en anställning via anställningsnummer och personnummer.
                Används i filer som ligger utanför FGS-anställningsdokumentet.
            </xs:documentation>
        </xs:annotation>
        <xs:sequence>
            <xs:element name="anstallningsnummer" type="xs:string"/>
            <xs:element name="personnummer"       type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="UtbetalningsgruppReferensType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">
                Referens till utbetalningsgrupp definierad i register/utbetalningsgrupper.xml.
            </xs:documentation>
        </xs:annotation>
        <xs:sequence>
            <xs:element name="id" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- ANSTÄLLNINGSTILLÄGG (används i FGS additionalXMLData)            -->
    <!-- ================================================================ -->
    
    <xs:element name="anstallningstillagg" type="AnstallningstillaggType"/>
    
    <xs:complexType name="AnstallningstillaggType">
        <xs:sequence>
            <xs:element name="utbetalningsgruppReferens" type="UtbetalningsgruppReferensType" minOccurs="0"/>
            <xs:element name="personalkategori"          type="PersonalkategoriType"          minOccurs="0"/>
            <xs:element name="anstallningsperioder"      type="AnstallningsperioderType"      minOccurs="0"/>
            <xs:element name="sysselsattningsgrader"     type="SysselsattningsgraderType"     minOccurs="0"/>
            <xs:element name="heltidsmatt"               type="HeltidsmattType"               minOccurs="0"/>
            <xs:element name="lonetillagg"               type="LonetillaggType"               minOccurs="0"/>
            <xs:element name="kostnadsfordelningar"      type="KostnadsfordelningarType"      minOccurs="0"/>
            <xs:element name="standardkonteringar"       type="StandardkonteringarType"       minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="PersonalkategoriType">
        <xs:sequence>
            <xs:element name="kod"       type="xs:string"/>
            <xs:element name="benamning" type="xs:string" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="AnstallningsperioderType">
        <xs:sequence>
            <xs:element name="anstallningsperiod" type="AnstallningsperiodType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="AnstallningsperiodType">
        <xs:sequence>
            <xs:element name="id"               type="xs:string"/>
            <xs:element name="giltighetsperiod" type="GiltighetsperiodType"/>
            <xs:element name="anstallningsform" type="xs:string"/>
            <xs:element name="loneform"         type="xs:string"/>
            <xs:element name="avslutsorsak"     type="xs:string" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="SysselsattningsgraderType">
        <xs:sequence>
            <xs:element name="sysselsattningsgrad" type="SysselsattningsgradType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="SysselsattningsgradType">
        <xs:sequence>
            <xs:element name="id"               type="xs:string"/>
            <xs:element name="procent"          type="ProcentType"/>
            <xs:element name="giltighetsperiod" type="GiltighetsperiodType"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="HeltidsmattType">
        <xs:sequence>
            <xs:element name="arbetsmatt" type="ArbetsmattType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="ArbetsmattType">
        <xs:sequence>
            <xs:element name="id"               type="xs:string"/>
            <xs:element name="timmarPerVecka"   type="xs:decimal"/>
            <xs:element name="giltighetsperiod" type="GiltighetsperiodType"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LonetillaggType">
        <xs:sequence>
            <xs:element name="tillagg" type="TillaggType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="TillaggType">
        <xs:sequence>
            <xs:element name="id"     type="xs:string"/>
            <xs:element name="namn"   type="xs:string"/>
            <xs:element name="varde"  type="VardeType"/>
            <xs:element name="valuta" type="ValutakodType" minOccurs="0"/>
            <xs:element name="giltighetsperiod" type="GiltighetsperiodType"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="VardeType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">
                Värde för lönetillägg. Attributet typ anger hur värdet ska tolkas.
                Vid typ="belopp" ska valuta anges på tilläggets överordnade element.
                Vid typ="faktor" anges inget belopp — värdet är en multiplikationsfaktor.
            </xs:documentation>
        </xs:annotation>
        <xs:simpleContent>
            <xs:extension base="xs:decimal">
                <xs:attribute name="typ" type="xs:string" use="required"/>
            </xs:extension>
        </xs:simpleContent>
    </xs:complexType>
    
    <xs:complexType name="KostnadsfordelningarType">
        <xs:sequence>
            <xs:element name="kostnadsfordelning" type="KostnadsfordelningType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="KostnadsfordelningType">
        <xs:sequence>
            <xs:element name="kostnadsfordelningId" type="xs:string"/>
            <xs:element name="ordningsnummer"       type="xs:integer"/>
            <xs:element name="giltighetsperiod"     type="GiltighetsperiodType"/>
            <xs:element name="procentfordelning"    type="ProcentType"/>
            <xs:element name="dimensioner"          type="DimensionerType"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="StandardkonteringarType">
        <xs:sequence>
            <xs:element name="standardkontering" type="StandardkonteringType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="StandardkonteringType">
        <xs:annotation>
            <xs:documentation xml:lang="sv">
                Förhandsdefinierad kontering per dimension för en anställning.
                I Flex Lön kallas detta "hemkontering".
            </xs:documentation>
        </xs:annotation>
        <xs:sequence>
            <xs:element name="dimensionId"   type="xs:string"/>
            <xs:element name="dimensionNamn" type="xs:string"/>
            <xs:element name="fordelningar"  type="StandardkonteringFordelningarType"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="StandardkonteringFordelningarType">
        <xs:sequence>
            <xs:element name="fordelning" type="StandardkonteringFordelningType" 
                        maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="StandardkonteringFordelningType">
        <xs:sequence>
            <xs:element name="kontering" type="xs:string"/>
            <xs:element name="procent"   type="ProcentType"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- LÖNEKÖRNINGAR (separat fil per paket)                            -->
    <!-- ================================================================ -->
    
    <xs:element name="lonekorningar" type="LonekorningarType"/>
    
    <xs:complexType name="LonekorningarType">
        <xs:sequence>
            <xs:element name="lonekorning" type="LonekorningType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LonekorningType">
        <xs:sequence>
            <xs:element name="id"                        type="xs:string"/>
            <xs:element name="lonekorningsnummer"        type="xs:string"/>
            <xs:element name="utbetalningsdatum"         type="xs:date"/>
            <xs:element name="utbetalningsgruppReferens" type="UtbetalningsgruppReferensType"/>
            <xs:element name="anstallningReferens"       type="AnstallningReferensType"/>
            <xs:element name="lonespecifikation"         type="LonespecifikationType" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LonespecifikationType">
        <xs:attribute name="href" type="xs:anyURI" use="required"/>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- LÖNETRANSAKTIONER (separat fil per paket)                        -->
    <!-- ================================================================ -->
    
    <xs:element name="lonetransaktioner" type="LonetransaktionerType"/>
    
    <xs:complexType name="LonetransaktionerType">
        <xs:sequence>
            <xs:element name="lonetransaktion" type="LonetransaktionType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LonetransaktionType">
        <xs:sequence>
            <xs:element name="id"                   type="xs:string"/>
            <xs:element name="transaktionId"        type="xs:string"/>
            <xs:element name="lonekorningReferens"  type="xs:string"/>
            <xs:element name="personalkategori"     type="xs:string"/>
            <xs:element name="loneart"              type="TransaktionLoneartType"/>
            <xs:element name="period"               type="GiltighetsperiodType" minOccurs="0"/>
            <xs:element name="omfattningProcent"    type="ProcentType" minOccurs="0"/>
            <xs:element name="kvantitet"            type="KvantitetType" minOccurs="0"/>
            <xs:element name="belopp"               type="xs:decimal"/>
            <xs:element name="valuta"               type="ValutakodType"/>
            <xs:element name="kommentar"            type="xs:string" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="TransaktionLoneartType">
        <xs:sequence>
            <xs:element name="kod"  type="xs:string"/>
            <xs:element name="namn" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="KvantitetType">
        <xs:sequence>
            <xs:element name="antal" type="xs:decimal"/>
            <xs:element name="enhet" type="xs:string" minOccurs="0"/>
            <xs:element name="aPris" type="xs:decimal"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- KONTERINGAR (separat fil per paket)                              -->
    <!-- ================================================================ -->
    
    <xs:element name="konteringar" type="KonteringarType"/>
    
    <xs:complexType name="KonteringarType">
        <xs:sequence>
            <xs:element name="kontering" type="KonteringType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="KonteringType">
        <xs:sequence>
            <xs:element name="id"                      type="xs:string"/>
            <xs:element name="fordelningId"            type="xs:string"/>
            <xs:element name="lonetransaktionReferens" type="xs:string"/>
            <xs:element name="procentfordelning"       type="ProcentType"/>
            <xs:element name="dimensioner"             type="DimensionerType"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- REGISTER: UTBETALNINGSGRUPPER                                    -->
    <!-- ================================================================ -->
    
    <xs:element name="utbetalningsgrupper" type="UtbetalningsgrupperType"/>
    
    <xs:complexType name="UtbetalningsgrupperType">
        <xs:sequence>
            <xs:element name="utbetalningsgrupp" type="UtbetalningsgruppType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="UtbetalningsgruppType">
        <xs:sequence>
            <xs:element name="id"   type="xs:string"/>
            <xs:element name="namn" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- REGISTER: FORMELVARIABLER                                        -->
    <!-- ================================================================ -->
    
    <xs:element name="formelvariabler" type="FormelvariablerType"/>
    
    <xs:complexType name="FormelvariablerType">
        <xs:sequence>
            <xs:element name="formelvariabel" type="FormelvariabelType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="FormelvariabelType">
        <xs:sequence>
            <xs:element name="namn"        type="xs:string"/>
            <xs:element name="beskrivning" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    
    
    <!-- ================================================================ -->
    <!-- REGISTER: LÖNEARTER                                              -->
    <!-- ================================================================ -->
    
    <xs:element name="lonearter" type="LonearterType"/>
    
    <xs:complexType name="LonearterType">
        <xs:sequence>
            <xs:element name="loneart" type="LoneartType" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LoneartType">
        <xs:sequence>
            <xs:element name="kod"                type="xs:string"/>
            <xs:element name="personalkategori"   type="xs:string"/>
            <xs:element name="namn"               type="xs:string"/>
            <xs:element name="formel"             type="xs:string" minOccurs="0"/>
            <xs:element name="underlagstypSkatt"  type="xs:string"/>
            <xs:element name="kontering"          type="LoneartKonteringType" minOccurs="0"/>
            <xs:element name="egenskaper"         type="LoneartEgenskaperType" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LoneartKonteringType">
        <xs:sequence>
            <xs:element name="konto"    type="xs:string"/>
            <xs:element name="motkonto" type="xs:string" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="LoneartEgenskaperType">
        <xs:sequence>
            <xs:element name="foraGrundande"             type="xs:boolean" minOccurs="0"/>
            <xs:element name="kapKlGrundande"            type="xs:boolean" minOccurs="0"/>
            <xs:element name="ejSocialavgiftsgrundande"  type="xs:boolean" minOccurs="0"/>
            <xs:element name="kostnadsavdragSocAvg"      type="KostnadsavdragSocAvgType" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    
    <xs:complexType name="KostnadsavdragSocAvgType">
        <xs:sequence>
            <xs:element name="procent" type="ProcentType"/>
        </xs:sequence>
    </xs:complexType>
    
</xs:schema>
```

---

## Bilaga B: Mappning CSV till XML

Denna bilaga visar hur fält i Flex:s CSV-uttag mappas till element i anpassningens XML-struktur. Paket-implicita fält (system, artal_start, artal_slut, organisationsnummer, foretagsnummer) utelämnas i XML eftersom de ges av paketkontexten via FGS Paket.

### B.1 arbetsgivare.csv

Målfil: `organisation/organisation.xml`

| CSV-fält | XML-element |
|---|---|
| organisationsnummer | `entityId localType="ORG"` |
| foretagsnummer | `entityId localType="FlexForetagsnummer"` |
| organisationsnamn | `nameEntry/part` |
| fora_forsakringsnummer | `entityId localType="FORA"` (om ej tomt) |
| kapkl_kundnummer | `entityId localType="KAPKL"` (om ej tomt) |
| gatuadress | `addressLine localType="postalAddress"` |
| postnummer | `addressLine localType="postalCode"` |
| postort | `addressLine localType="postalCity"` |

### B.2 anstallningar.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` samt `personer/P_<personnummer>.xml`

Anställningsdokument:

| CSV-fält | XML-element |
|---|---|
| anstallningsnummer | `recordId` (med prefix F_), `employmentId` |
| befattning | `position/description` |
| bksk_kod | `position/term/@code` med `@source="BKSK"` |
| bksk_klartext | `position/term` (textinnehåll) |
| utbetalningsgrupp_id | `anstallningstillagg/utbetalningsgruppReferens/id` |
| utbetalningsgrupp_namn | Registerfil utbetalningsgrupper.xml |
| personalkategori | `anstallningstillagg/personalkategori/kod` |
| befattningskod | Reserverat för framtida bruk (ej använt i exempeldata) |

Persondokument:

| CSV-fält | XML-element |
|---|---|
| personnummer | `entityId localType="PersonalIdentityNumber"` eller `CoordinationNumber` |
| fornamn | `nameEntry localType="forename"/part` |
| efternamn | `nameEntry localType="surname"/part` |
| skyddad | `descriptiveNote/p` med värdet "Skyddad identitet" (om sant) |
| nationalitet | `localDescription localType="nationality"/term` |

### B.3 anstallningsperioder.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/anstallningsperioder`

| CSV-fält | XML-element |
|---|---|
| anstallningsperiod_id | `anstallningsperiod/id` |
| periodstart | `anstallningsperiod/giltighetsperiod/startdatum` |
| periodslut | `anstallningsperiod/giltighetsperiod/slutdatum` (om ej tomt) |
| anstallningsform | `anstallningsperiod/anstallningsform` |
| avslutsorsak | `anstallningsperiod/avslutsorsak` (om ej tomt) |
| loneform | `anstallningsperiod/loneform` |

### B.4 manadsloner.csv och timloner.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `salaryAgreements` (FGS-standard)

| CSV-fält | XML-element |
|---|---|
| manadslon_heltid_sek / timlon_sek | `salaryAgreement/@amount` |
| manadslon_heltid_sek_startdatum / timlon_sek_startdatum | `salaryAgreement/salaryPeriod/dateRange/startDate` |
| manadslon_heltid_sek_slutdatum / timlon_sek_slutdatum | `salaryAgreement/salaryPeriod/dateRange/endDate` (om ej tomt) |

`salaryType="monthlyPay"` för månadslön, `salaryType="hourlyWage"` för timlön. `currency="SEK"` sätts konstant.

### B.5 sysselsattningsgrader.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/sysselsattningsgrader`

| CSV-fält | XML-element |
|---|---|
| sysselsattningsgrad_id | `sysselsattningsgrad/id` |
| sysselsattningsgrad | `sysselsattningsgrad/procent` |
| sysselsattningsgrad_startdatum | `sysselsattningsgrad/giltighetsperiod/startdatum` |
| sysselsattningsgrad_slutdatum | `sysselsattningsgrad/giltighetsperiod/slutdatum` (om ej tomt) |

### B.6 arbetsmatt_heltid.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/heltidsmatt`

| CSV-fält | XML-element |
|---|---|
| arbetsmatt_heltid_id | `arbetsmatt/id` |
| arbetsmatt_heltid | `arbetsmatt/timmarPerVecka` |
| arbetsmatt_heltid_startdatum | `arbetsmatt/giltighetsperiod/startdatum` |
| arbetsmatt_heltid_slutdatum | `arbetsmatt/giltighetsperiod/slutdatum` (om ej tomt) |

### B.7 lonetillagg.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/lonetillagg`

| CSV-fält | XML-element |
|---|---|
| lonetillagg_id | `tillagg/id` |
| lonetillagg_namn | `tillagg/namn` |
| lonetillagg_varde | `tillagg/varde` (innehåll) |
| lonetillagg_startdatum | `tillagg/giltighetsperiod/startdatum` |
| lonetillagg_slutdatum | `tillagg/giltighetsperiod/slutdatum` (om ej tomt och ej fiktivt "tills vidare"-datum) |

`typ`-attribut på `varde` sätts till "belopp" eller "faktor" beroende på tilläggets natur. `valuta` sätts till "SEK" vid typ="belopp".

### B.8 kostnadsfordelningar.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/kostnadsfordelningar`

| CSV-fält | XML-element |
|---|---|
| kostnadsfordelning_id | `kostnadsfordelning/kostnadsfordelningId` |
| ordningsnummer | `kostnadsfordelning/ordningsnummer` |
| kostnadsfordelning_startdatum | `kostnadsfordelning/giltighetsperiod/startdatum` |
| kostnadsfordelning_slutdatum | `kostnadsfordelning/giltighetsperiod/slutdatum` (om ej tomt) |
| dim01..dim10_namn/varde | `kostnadsfordelning/dimensioner/dimension/namn` och `/varde` (endast för ifyllda dimensioner) |
| procentfordelning | `kostnadsfordelning/procentfordelning` |

### B.9 hemkonteringar.csv

Målfil: `anstallningar/F_<anstallningsnummer>.xml` inom `anstallningstillagg/standardkonteringar`

| CSV-fält | XML-element |
|---|---|
| dimension_id | `standardkontering/dimensionId` |
| dimension_namn | `standardkontering/dimensionNamn` |
| kontering1..5 / procent1..5 | `standardkontering/fordelningar/fordelning` (en per ifylld kombination) |

### B.10 lonekorningar.csv

Målfil: `loneutbetalningar/lonekorningar.xml`

| CSV-fält | XML-element |
|---|---|
| (genererad) | `lonekorning/id` = `LK_<år>_<löpnr>` |
| lonekorningsnummer | `lonekorning/lonekorningsnummer` |
| utbetalningsdatum | `lonekorning/utbetalningsdatum` |
| utbetalningsgrupp_id | `lonekorning/utbetalningsgruppReferens/id` |
| personnummer, anstallningsnummer | `lonekorning/anstallningReferens` |
| lonespec | `lonekorning/lonespecifikation/@href` (om ej tomt) |

### B.11 lonetransaktioner.csv

Målfil: `loneutbetalningar/lonetransaktioner.xml`

| CSV-fält | XML-element |
|---|---|
| (genererad) | `lonetransaktion/id` = `LT_<år>_<löpnr>` |
| transaktion_id | `lonetransaktion/transaktionId` |
| lonekorningsnummer + anstallningsnummer | Översätts till `lonekorningReferens` (syntetiskt LK-id) |
| personalkategori | `lonetransaktion/personalkategori` |
| loneart_kod | `lonetransaktion/loneart/kod` |
| loneart_namn | `lonetransaktion/loneart/namn` |
| datumstart | `lonetransaktion/period/startdatum` (om ej tomt) |
| datumslut | `lonetransaktion/period/slutdatum` (om ej tomt) |
| omfattning_procent | `lonetransaktion/omfattningProcent` (om ej tomt) |
| antal | `lonetransaktion/kvantitet/antal` (om gruppen inkluderas) |
| enhet | `lonetransaktion/kvantitet/enhet` (om ej tomt) |
| apris | `lonetransaktion/kvantitet/aPris` (om gruppen inkluderas) |
| belopp_sek | `lonetransaktion/belopp` |
| (konstant) | `lonetransaktion/valuta` = "SEK" |
| transaktionsrad_text | `lonetransaktion/kommentar` (om ej tomt) |

### B.12 lonetransaktion_konteringar.csv

Målfil: `loneutbetalningar/konteringar.xml`

| CSV-fält | XML-element |
|---|---|
| (genererad) | `kontering/id` = `K_<år>_<löpnr>` |
| fordelning_id | `kontering/fordelningId` |
| transaktion_id + lonekorningsnummer + anstallningsnummer | Översätts till `lonetransaktionReferens` (syntetiskt LT-id) |
| dim01..dim10_namn/varde | `kontering/dimensioner/dimension/namn` och `/varde` (endast ifyllda) |
| procentfordelning | `kontering/procentfordelning` |

### B.13 lonearter.csv

Målfil: `register/lonearter.xml`

| CSV-fält | XML-element |
|---|---|
| loneart_kod | `loneart/kod` |
| personalkategori | `loneart/personalkategori` |
| loneart_namn | `loneart/namn` |
| loneart_formel | `loneart/formel` (i CDATA, om ej tomt) |
| underlagstyp_skatt | `loneart/underlagstypSkatt` |
| loneart_konto | `loneart/kontering/konto` (om ej tomt) |
| loneart_motkonto | `loneart/kontering/motkonto` (om ej tomt) |
| ej_underlag_soc_avg | `loneart/egenskaper/ejSocialavgiftsgrundande` = true (om ifyllt) |
| kostnadsavdrag_sov_avg | Utlöser `loneart/egenskaper/kostnadsavdragSocAvg`-gruppen |
| kostnadsavdrag_soc_avg_procent | `loneart/egenskaper/kostnadsavdragSocAvg/procent` |
| fora | `loneart/egenskaper/foraGrundande` = true (om ifyllt) |
| kap_kl | `loneart/egenskaper/kapKlGrundande` = true (om ifyllt) |

Fältet `loneartsnummer` ingår inte i registret — det är en Flex-intern löpnummer som saknar värde i arkivet.

### B.14 formelvariabler.csv

Målfil: `register/formelvariabler.xml`

| CSV-fält | XML-element |
|---|---|
| variabelnamn | `formelvariabel/namn` |
| beskrivning | `formelvariabel/beskrivning` |

---

*Detta dokument är en del av Svenska kyrkans anpassning av FGS Personal. De ursprungliga FGS-dokumenten, som förblir oförändrade, utgör den auktoritativa grundspecifikationen. Detta dokument beskriver enbart avvikelserna och tilläggen för Svenska kyrkans användning.*
