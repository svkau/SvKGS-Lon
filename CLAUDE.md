# CLAUDE.md

Guide for Claude Code when working on this repository.

## What this project is

Svenska kyrkans lokala anpassning av **FGS Personal** (Riksarkivets Förvaltningsgemensamma Specifikation för personalinformation, RAFGS2V1.0) för arkivering av personal- och lönedata ur lönesystemet **Flex Lön**. Målet är att kunna ta emot årliga CSV-uttag från Flex och transformera dem till ett strukturerat XML-arkivpaket.

Arkitekturen utformades så att den inte ska vara alltför bunden till Flex — framtida uttag från andra lönesystem (Kontek, Agda, Hogia m.fl.) ska kunna använda samma XML-struktur.

## Repository layout

```
.
├── CLAUDE.md                          # Denna fil
├── svk-fgs-personal-anpassning.md     # Anpassningsdokumentet (huvuddokument)
├── svk-personal-lon.xsd               # XSD-schema för tilläggsschemat
├── svk-personal-lon.sch               # Schematron-regler (XSLT 1-kompatibla)
└── ...                                # Övriga arbetsfiler, exempel, testdata
```

XSD:n ligger också inline i anpassningsdokumentets Bilaga A. Vid ändringar måste båda platserna uppdateras samtidigt.

## Designfilosofi (viktig att förstå innan ändringar)

### Strikt partitionering mellan FGS och tilläggsschema

Samma data finns aldrig på två ställen. Det betyder:

- **Grundlön** (månadslön/timlön) ligger i FGS `salaryAgreements`.
- **Sysselsättningsgrad, heltidsmått, lönetillägg, anställningsperioder** ligger *enbart* i tilläggsschemat.
- FGS-element som `employmentDates`, `typeOfEmployment`, `employmentTerminations`, `weeklyWorkingTime` används *inte* — motsvarande data bor i tilläggsschemats `anstallningsperioder`.

### Tre typer av identifierare — känn skillnaden

| Typ | Användning | Stabilitet över år |
|---|---|---|
| `recordId` i FGS-dokument (ORG_, F_, A_, P_) | FGS-interna nycklar byggda på naturliga id:n | Stabil över år — samma anställning har samma F_-id i alla paket |
| Syntetiska id (LK_2022_000001, LT_2022_000001, K_2022_000001) | Enbart för korsreferenser mellan filer inom ett paket | Paketlokala, årtalsprefix för globalunikhet |
| Naturliga nycklar (lonekorningsnummer "2020-09", transaktion_id) | Källdata som bevaras i XML | Stabila där källsystemet har stabila id:n |

Vid ackumulering av flera årgångar i t.ex. SQLite är det `recordId` som matchar över år (UPSERT-semantik), inte syntetiska id:n.

### Två sorters datamodeller — tabellnär vs nästlad

- **Tabellnär** (platta listor med explicita referenser): lönekörningar, lönetransaktioner, konteringar. En fil per tabell. Speglar CSV-ursprunget.
- **Nästlad** (hierarkisk): anställningsdata med sina tidsserier inuti FGS-anställningsdokumentet via `additionalXMLData`.

Kostnadsfördelningar och standardkonteringar (Flex:s "hemkontering") är nästlade i anställningsdokumentet — de är anställningsegenskaper, inte transaktionsflöden.

### Skyddad identitet

Full bevaring i arkivpaketet. Ingen maskning av personnummer, namn eller andra uppgifter. Flaggas via `descriptiveNote` i Person-dokumentet. Åtkomstbegränsning sker i e-arkivets söklager, inte i paketet.

### Namnkonventioner

- **Svenska** i tilläggsschemats elementnamn (markerar gränsen mot engelska FGS-element).
- **Namnrymd**: `https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1`. Version i namnrymden — ändras till v2 vid icke-bakåtkompatibla ändringar.
- **"standardkontering"** används i schemat för det Flex kallar "hemkontering" (mer vedertagen term).

## Teknisk miljö

- **Validering**: Python med `lxml.isoschematron` (XSLT 1-baserat). Schematron-reglerna är skrivna för XSLT 1-kompatibilitet — inga XSLT 2-funktioner som `matches()`, `for-each-group`, `xs:date`-aritmetik.
- **Datumjämförelse i Schematron**: Görs via `number(translate(datum, '-', ''))` för numerisk jämförelse av YYYY-MM-DD-strängar.
- **Referensintegritet via `document()`**: Reglerna är defensivt skrivna — om filen inte finns i förväntad relativ sökväg hoppas kontrollen tyst över. Möjliggör isolerad validering.

## Paketstruktur

```
[paketidentifierare]/
├── manifest.xml                 (FGS Paket — yttre hölje)
├── organisation/organisation.xml
├── anstallningar/F_<num>.xml    (en per anställning)
├── arbetstagare/A_<pnr>.xml     (en per arbetstagare, tunn)
├── personer/P_<pnr>.xml
├── loneutbetalningar/
│   ├── lonekorningar.xml        (tabellnär)
│   ├── lonetransaktioner.xml    (tabellnär)
│   └── konteringar.xml          (tabellnär)
├── register/
│   ├── lonearter.xml
│   ├── formelvariabler.xml
│   └── utbetalningsgrupper.xml
└── lonespecifikationer/*.html
```

Ett paket = en arbetsgivare × ett uttagsår. Paketet innehåller hela den historik som är känd vid uttagstillfället. Framtida paket upprepar data som fortfarande är relevant — redundans accepteras för att hålla paket självförsörjande.

## Vanliga uppgifter

### Lägga till ny regel i Schematron

1. Formulera regeln som `<assert>` (blockerar) eller `<report>` (varnar).
2. Lägg till ett testfall i `test_full.py` — både positivt och negativt exempel.
3. Kör `python3 test_full.py` och verifiera att alla 14+ tester passerar.
4. Kontrollera att regeln fungerar i XSLT 1 (ingen `matches()`, `tokenize()`, `xs:date`-aritmetik).

### Ändra XSD-schema

1. Uppdatera `svk-personal-lon.xsd` (separat fil om den finns, annars inline i anpassningsdokumentet).
2. Uppdatera motsvarande XSD i Bilaga A av `svk-fgs-personal-anpassning.md`.
3. Om ändringen är icke-bakåtkompatibel: bumpa namnrymden till v2.
4. Uppdatera Bilaga B (mappningstabellen) om CSV→XML-mappningen påverkas.

### Lägga till nytt fält från Flex

1. Kontrollera vad fältet faktiskt innehåller i riktiga Flex-data — testa inte bara med dokumentationsantaganden.
2. Bestäm om det hör hemma i befintlig struktur eller kräver nytt element.
3. Se om fältet är generiskt (bör finnas i schemat) eller Flex-specifikt (bör kanske hanteras via ett attribut som `syntax="Flex"` eller liknande).
4. Dokumentera beslutet i anpassningsdokumentet.

### Skapa XML från CSV-data

Mappningen finns i anpassningsdokumentets Bilaga B, tabell för tabell. Några återkommande konverteringar:

- Datum: `2020-09-01T00:00:00` → `2020-09-01` (strippa tid)
- Decimaler: komma → punkt (men Flex-data verkar redan använda punkt i belopp)
- Tomma fält: utelämnas helt i XML, skrivs inte som `<element/>`
- Fiktiva "tills vidare"-datum (t.ex. 2049-01-01): utelämnas som slutdatum
- Multiradiga formler med `¤` som separator: bevaras ordagrant i CDATA

## Vad som *inte* är i scope

Följande designdiskussioner har vi medvetet parkerat:

- **Negativa belopp och korrigeringstransaktioner**: Representeras som minustecken på belopp. Ingen separat typ- eller statusindikator. Utökad dokumentation kan tillkomma om Flex-beteendet visar sig mer komplext.
- **Procentsummering**: Kontroll att procentfordelningar inom samma `kostnadsfordelningId` summerar till 100 är utelämnad från Schematron (kräver XSLT 2-aggregering). Görs i Python-validering istället.
- **Personnummer-kontrollsiffra**: Bara formatvalidering, inte modulus-10-kontroll. Ligger utanför XSLT 1:s bekväma räckvidd.

## Nyckelbeslut som inte är uppenbara vid läsning

- **Organisatorisk enhet**: Används ej — Svenska kyrkans arbetsgivare är GAS-enheter utan interna enheter i Flex.
- **Arbetstagare**: Dokumentet är medvetet tunt (bara control och relations). Fungerar som krok för framtida utökning via `additionalXMLData`.
- **Lönearter**: Primärnyckel är sammansatt (`kod + personalkategori`) eftersom samma kod kan ha olika varianter för olika kategorier. För icke-Flex-system där personalkategori saknas är den tom/utelämnad.
- **Formelvariabler**: Är en *ordlista med namn och beskrivning*, inte ett värderegister. Variablerna har inga värden i registret — de beräknas vid körning. Registret finns för att göra formlerna tolkningsbara.
- **Personnummer vs samordningsnummer**: Två skilda `localType`-värden i `entityId` (PersonalIdentityNumber, CoordinationNumber). Samordningsnummer känns igen på att dagsiffran är +60.

## Källor att konsultera vid tveksamheter

- `svk-fgs-personal-anpassning.md` — det auktoritativa anpassningsdokumentet
- Riksarkivets FGS Personal (RAFGS2V1.0) och FGS Personal Tillägg (RAFGS2V1.0A20190225)
- Flex:s egen dokumentation för systemspecifika begrepp och formelsyntax
- Beställningsunderlaget för Flex-uttaget för CSV-strukturen
