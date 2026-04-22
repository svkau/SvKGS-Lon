<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        queryBinding="xslt"
        xml:lang="sv">
    
    <title>Svenska kyrkans anpassning av FGS Personal — valideringsregler</title>
    
    <ns uri="https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1"
        prefix="svk"/>
    
    <p>
        Schematron-regler för XML-filer enligt anpassningens tilläggsschema
        (namnrymd https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1).
        Reglerna är skrivna för XSLT 1-kompatibilitet och kan valideras med
        lxml.isoschematron i Python eller motsvarande XSLT 1-baserade verktyg.
    </p>
    
    <p>
        Vissa regler som kräver komplex aggregering eller datumaritmetik är
        medvetet utelämnade och dokumenteras i anpassningsdokumentet som
        "extern validering krävs".
    </p>
    
    
    <!-- ================================================================ -->
    <!-- NYCKLAR FÖR UNIKHETSKONTROLLER OCH KORSREFERENSER                -->
    <!-- ================================================================ -->
    
    <xsl:key name="loneart-nyckel"
             match="svk:loneart"
             use="concat(svk:kod, '|', svk:personalkategori)"/>
    
    <xsl:key name="formelvariabel-namn"
             match="svk:formelvariabel"
             use="svk:namn"/>
    
    <xsl:key name="utbetalningsgrupp-id"
             match="svk:utbetalningsgrupp"
             use="svk:id"/>
    
    <xsl:key name="lonekorning-id"
             match="svk:lonekorning"
             use="svk:id"/>
    
    <xsl:key name="lonetransaktion-id"
             match="svk:lonetransaktion"
             use="svk:id"/>
    
    
    <!-- ================================================================ -->
    <!-- DATUMFORMAT OCH GILTIGHETSPERIODER                               -->
    <!-- ================================================================ -->
    
    <pattern id="datumformat">
        <title>Datumformat enligt xs:date</title>
        
        <rule context="svk:startdatum | svk:slutdatum | svk:utbetalningsdatum">
            <assert test="string-length(.) = 10 
                        and substring(., 5, 1) = '-' 
                        and substring(., 8, 1) = '-'">
                Datum <value-of select="local-name()"/> ska vara på formatet YYYY-MM-DD,
                men värdet är "<value-of select="."/>".
            </assert>
        </rule>
    </pattern>
    
    <pattern id="giltighetsperiod-ordning">
        <title>Startdatum ska vara tidigare än eller lika med slutdatum</title>
        
        <rule context="svk:giltighetsperiod[svk:slutdatum]">
            <assert test="number(translate(svk:startdatum, '-', '')) 
                       &lt;= number(translate(svk:slutdatum, '-', ''))">
                Startdatum (<value-of select="svk:startdatum"/>) ska vara tidigare
                än eller lika med slutdatum (<value-of select="svk:slutdatum"/>).
            </assert>
        </rule>
        
        <rule context="svk:period[svk:slutdatum]">
            <assert test="number(translate(svk:startdatum, '-', '')) 
                       &lt;= number(translate(svk:slutdatum, '-', ''))">
                Startdatum (<value-of select="svk:startdatum"/>) ska vara tidigare
                än eller lika med slutdatum (<value-of select="svk:slutdatum"/>)
                i lönetransaktionens period.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- LÖNETILLÄGG — VILLKORLIGA REGLER FÖR VÄRDE OCH VALUTA            -->
    <!-- ================================================================ -->
    
    <pattern id="lonetillagg-varde-valuta">
        <title>Lönetilläggs värdetyp styr om valuta krävs</title>
        
        <rule context="svk:tillagg[svk:varde/@typ = 'belopp']">
            <assert test="svk:valuta">
                Lönetillägg med varde typ="belopp" måste ha valuta angiven.
                Id: <value-of select="svk:id"/>.
            </assert>
        </rule>
        
        <rule context="svk:tillagg[svk:varde/@typ = 'faktor']">
            <assert test="not(svk:valuta)">
                Lönetillägg med varde typ="faktor" ska inte ha valuta angiven.
                Id: <value-of select="svk:id"/>.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="lonetillagg-vardetyp">
        <title>Värdetyp ska vara en rekommenderad term</title>
        
        <rule context="svk:varde">
            <assert test="@typ">
                Elementet varde måste ha attributet typ.
            </assert>
            <report test="@typ and not(@typ = 'belopp' or @typ = 'faktor')">
                Värdetyp "<value-of select="@typ"/>" är inte en rekommenderad term.
                Godkända termer är "belopp" och "faktor".
            </report>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- VÄRDELISTOR — VARNINGAR FÖR OKÄNDA TERMER                        -->
    <!-- ================================================================ -->
    
    <pattern id="anstallningsform-vardelista">
        <title>Anställningsform enligt rekommenderad värdelista</title>
        
        <rule context="svk:anstallningsform">
            <report test="not(
                . = 'Tillsvidareanställd' or
                . = 'Visstidsanställd' or
                . = 'Provanställd' or
                . = 'Vikariat' or
                . = 'Timanställd'
            )">
                Anställningsform "<value-of select="."/>" finns inte i den rekommenderade
                värdelistan (avsnitt 4.5.1 i anpassningsdokumentet). Kontrollera om
                värdet är avsiktligt.
            </report>
        </rule>
    </pattern>
    
    <pattern id="loneform-vardelista">
        <title>Löneform enligt rekommenderad värdelista</title>
        
        <rule context="svk:loneform">
            <report test="not(
                . = 'Månadslön' or
                . = 'Timlön'
            )">
                Löneform "<value-of select="."/>" finns inte i den rekommenderade
                värdelistan (avsnitt 4.5.2 i anpassningsdokumentet). Kontrollera om
                värdet är avsiktligt.
            </report>
        </rule>
    </pattern>
    
    <pattern id="avslutsorsak-vardelista">
        <title>Avslutsorsak enligt rekommenderad värdelista</title>
        
        <rule context="svk:avslutsorsak">
            <report test="not(
                . = 'Egen begäran' or
                . = 'Pensionsavgång' or
                . = 'Uppsagd pga arbetsbrist' or
                . = 'Uppsagd av personliga skäl' or
                . = 'Avliden'
            )">
                Avslutsorsak "<value-of select="."/>" finns inte i den rekommenderade
                värdelistan (avsnitt 4.5.3 i anpassningsdokumentet). Kontrollera om
                värdet är avsiktligt.
            </report>
        </rule>
    </pattern>
    
    <pattern id="underlagstyp-skatt-vardelista">
        <title>Underlagstyp skatt enligt värdelista</title>
        
        <rule context="svk:underlagstypSkatt">
            <report test="not(
                . = 'Tabellskatt' or
                . = 'Engångsskatt' or
                . = 'Ej Skatt'
            )">
                Underlagstyp skatt "<value-of select="."/>" finns inte i
                värdelistan (avsnitt 4.5.4 i anpassningsdokumentet).
            </report>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- VALUTA                                                           -->
    <!-- ================================================================ -->
    
    <pattern id="valuta-format">
        <title>Valutakod enligt ISO 4217</title>
        
        <rule context="svk:valuta">
            <assert test="string-length(.) = 3">
                Valutakod ska vara tre tecken lång enligt ISO 4217,
                men värdet är "<value-of select="."/>".
            </assert>
            <assert test="translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '') = ''">
                Valutakod ska bestå av enbart stora bokstäver A-Z,
                men värdet är "<value-of select="."/>".
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- UNIKHET INOM FIL (Muenchian-stil via xsl:key)                    -->
    <!-- ================================================================ -->
    
    <pattern id="loneart-unikhet">
        <title>Kombinationen kod+personalkategori är unik inom lonearter</title>
        
        <rule context="svk:loneart">
            <assert test="count(key('loneart-nyckel', 
                                    concat(svk:kod, '|', svk:personalkategori))) = 1">
                Kombinationen kod "<value-of select="svk:kod"/>" och
                personalkategori "<value-of select="svk:personalkategori"/>"
                förekommer flera gånger i lonearter.xml. Varje kombination måste
                vara unik.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="formelvariabel-unikhet">
        <title>Formelvariabelnamn är unikt inom formelvariabler</title>
        
        <rule context="svk:formelvariabel">
            <assert test="count(key('formelvariabel-namn', svk:namn)) = 1">
                Formelvariabelnamn "<value-of select="svk:namn"/>" förekommer
                flera gånger i formelvariabler.xml. Varje namn måste vara unikt.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="utbetalningsgrupp-unikhet">
        <title>Utbetalningsgruppens id är unikt</title>
        
        <rule context="svk:utbetalningsgrupp">
            <assert test="count(key('utbetalningsgrupp-id', svk:id)) = 1">
                Utbetalningsgrupp id "<value-of select="svk:id"/>" förekommer
                flera gånger i utbetalningsgrupper.xml.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="lonekorning-unikhet">
        <title>Lönekörnings syntetiska id är unikt</title>
        
        <rule context="svk:lonekorning">
            <assert test="count(key('lonekorning-id', svk:id)) = 1">
                Lönekörnings id "<value-of select="svk:id"/>" förekommer flera
                gånger i lonekorningar.xml.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="lonetransaktion-unikhet">
        <title>Lönetransaktions syntetiska id är unikt</title>
        
        <rule context="svk:lonetransaktion">
            <assert test="count(key('lonetransaktion-id', svk:id)) = 1">
                Lönetransaktions id "<value-of select="svk:id"/>" förekommer
                flera gånger i lonetransaktioner.xml.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- ID-FORMAT                                                        -->
    <!-- ================================================================ -->
    
    <pattern id="syntetiska-id-format">
        <title>Syntetiska id ska följa mönstret PREFIX_ÅR_LÖPNR</title>
        
        <rule context="svk:lonekorning/svk:id">
            <assert test="starts-with(., 'LK_')">
                Lönekörnings id ska börja med "LK_", men värdet är "<value-of select="."/>".
            </assert>
        </rule>
        
        <rule context="svk:lonetransaktion/svk:id">
            <assert test="starts-with(., 'LT_')">
                Lönetransaktions id ska börja med "LT_", men värdet är "<value-of select="."/>".
            </assert>
        </rule>
        
        <rule context="svk:kontering/svk:id">
            <assert test="starts-with(., 'K_')">
                Konterings id ska börja med "K_", men värdet är "<value-of select="."/>".
            </assert>
        </rule>
    </pattern>
    
    <pattern id="lonetransaktion-referens-format">
        <title>Lonetransaktionreferens ska börja med LT_</title>
        
        <rule context="svk:lonetransaktionReferens">
            <assert test="starts-with(., 'LT_')">
                Referensen "<value-of select="."/>" ska följa mönstret
                LT_ÅR_LÖPNR.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="lonekorning-referens-format">
        <title>Lonekorningreferens ska börja med LK_</title>
        
        <rule context="svk:lonekorningReferens">
            <assert test="starts-with(., 'LK_')">
                Referensen "<value-of select="."/>" ska följa mönstret
                LK_ÅR_LÖPNR.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- REFERENSINTEGRITET MELLAN FILER                                  -->
    <!-- ================================================================ -->
    
    <!--
        Dessa regler förutsätter att valideringen körs i en komplett
        paketkontext med standardiserade sökvägar relativt den fil som
        valideras. Om motsvarande fil saknas (t.ex. vid isolerad validering
        av en enskild fil) hoppar reglerna över kontrollen utan att fela.
        Justera document()-sökvägarna om er paketstruktur avviker från
        den som beskrivs i anpassningsdokumentet.
    -->
    
    <pattern id="lonetransaktion-hanvisning-till-lonekorning">
        <title>Lönetransaktions lonekorningReferens matchar existerande lönekörning</title>
        
        <rule context="svk:lonetransaktion/svk:lonekorningReferens">
            <assert test="not(document('lonekorningar.xml', /))
                        or document('lonekorningar.xml', /)//svk:lonekorning/svk:id = .">
                Lönetransaktionens referens till lönekörning
                "<value-of select="."/>" matchar ingen existerande lönekörning
                i lonekorningar.xml.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="kontering-hanvisning-till-lonetransaktion">
        <title>Konterings lonetransaktionReferens matchar existerande transaktion</title>
        
        <rule context="svk:kontering/svk:lonetransaktionReferens">
            <assert test="not(document('lonetransaktioner.xml', /))
                        or document('lonetransaktioner.xml', /)//svk:lonetransaktion/svk:id = .">
                Konteringens referens till lönetransaktion
                "<value-of select="."/>" matchar ingen existerande transaktion
                i lonetransaktioner.xml.
            </assert>
        </rule>
    </pattern>
    
    <pattern id="utbetalningsgrupp-hanvisning">
        <title>Utbetalningsgruppreferens matchar existerande grupp i registret</title>
        
        <rule context="svk:utbetalningsgruppReferens">
            <assert test="not(document('../register/utbetalningsgrupper.xml', /))
                        or document('../register/utbetalningsgrupper.xml', /)
                          //svk:utbetalningsgrupp/svk:id = svk:id">
                Referensen till utbetalningsgrupp "<value-of select="svk:id"/>"
                matchar ingen existerande grupp i register/utbetalningsgrupper.xml.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- FORMEL — SYNTAX-ATTRIBUT REKOMMENDERAT                           -->
    <!-- ================================================================ -->
    
    <pattern id="formel-syntax">
        <title>Formelns syntax bör markeras</title>
        
        <rule context="svk:loneart/svk:formel">
            <report test="not(@syntax)">
                Lönearts formel saknar syntax-attribut. Attributet rekommenderas
                för att markera vilket källsystems formelspråk formeln tillhör,
                t.ex. syntax="Flex".
            </report>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- KVANTITET — KONSEKVENS I ANGIVELSER                              -->
    <!-- ================================================================ -->
    
    <pattern id="kvantitet-konsistens">
        <title>Kvantitetsgrupp ska ha både antal och aPris när den används</title>
        
        <rule context="svk:kvantitet">
            <assert test="svk:antal">
                Kvantitetselementet måste innehålla antal.
            </assert>
            <assert test="svk:aPris">
                Kvantitetselementet måste innehålla aPris.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- ANSTÄLLNINGSREFERENS                                             -->
    <!-- ================================================================ -->
    
    <pattern id="anstallningsreferens-faltinnehall">
        <title>Anställningsreferens ska ha både nummer och personnummer</title>
        
        <rule context="svk:anstallningReferens">
            <assert test="string-length(normalize-space(svk:anstallningsnummer)) > 0">
                Anställningsreferens ska innehålla ett anställningsnummer.
            </assert>
            <assert test="string-length(normalize-space(svk:personnummer)) > 0">
                Anställningsreferens ska innehålla ett personnummer eller
                samordningsnummer.
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- PERSONNUMMER OCH SAMORDNINGSNUMMER — GRUNDLÄGGANDE FORMATKOLL    -->
    <!-- ================================================================ -->
    
    <pattern id="personnummer-grundformat">
        <title>Personnummer ska ha rätt längd och bindestreckposition</title>
        
        <rule context="svk:personnummer">
            <assert test="string-length(.) = 13 and substring(., 9, 1) = '-'">
                Personnummer "<value-of select="."/>" ska vara på formatet
                YYYYMMDD-NNNN (13 tecken med bindestreck i position 9).
            </assert>
        </rule>
    </pattern>
    
    
    <!-- ================================================================ -->
    <!-- PROCENTVÄRDEN                                                    -->
    <!-- ================================================================ -->
    
    <!--
        Övergripande kontroll av procentvärden görs i XSD (typen ProcentType
        tillåter endast 0-100). Schematron används här inte för enskilda
        värden utan skulle kunna användas för att kontrollera att summerade
        procentfordelningar inom samma grupp blir exakt 100. Sådan summering
        över grupper är dock svår att uttrycka i XSLT 1 och är därför
        utelämnad — extern validering krävs för det.
    -->
    
    
    <!-- ================================================================ -->
    <!-- UTELÄMNAT AV DESIGN                                              -->
    <!-- ================================================================ -->
    
    <!--
        Följande regler är utelämnade eftersom de kräver konstruktioner
        som inte är enkelt uttryckbara i XSLT 1:
        
        1. Summering av procentfordelningar inom kostnadsfordelningId-grupp
           (kräver for-each-group eller komplex Muenchian-konstruktion).
        
        2. Summering av procent inom standardkontering/fordelningar
           (samma skäl).
        
        3. Kontroll att procentfordelningar i kontering.xml med samma
           fordelningId summerar till 100 (samma skäl).
        
        4. Kontroll att personnummer har giltig kontrollsiffra
           (kräver modulus-aritmetik på ett sätt som är besvärligt i XSLT 1).
        
        5. Kontroll att lonekorningsnummer har formatet YYYY-MM
           (kräver regex som inte finns i XSLT 1).
        
        Dessa kontroller implementeras lämpligen i Python-koden som genererar
        eller konsumerar XML-filerna.
    -->
    
</schema>
