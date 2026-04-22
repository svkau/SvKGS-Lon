DROP TABLE IF EXISTS "main"."arbetsgivare";
CREATE TABLE
       "main"."arbetsgivare" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "organisationsnamn" TEXT,
       "fora_forsakringsnummer" TEXT,
       "kapkl_kundnummer" TEXT,
       "gatuadress" TEXT,
       "postnummer" TEXT,
       "postort" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer")
);

DROP TABLE IF EXISTS "main"."anstallningar";
CREATE TABLE
       "main"."anstallningar" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "utbetalningsgrupp_namn" TEXT,
       "personalkategori" TEXT,
       "befattning" TEXT,
       "bksk_kod" TEXT,
       "bksk_klartext" TEXT,
       "befattningskod" TEXT,
       "fornamn" TEXT,
       "efternamn" TEXT,
       "skyddad" BOOLEAN,
       "nationalitet" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer") REFERENCES "arbetsgivare"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer")
);

DROP TABLE IF EXISTS "main"."lonekorningar";
CREATE TABLE
       "main"."lonekorningar" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
		"utbetalningsgrupp_namn" TEXT,
       "lonekorningsnummer" TEXT,
       "utbetalningsdatum" DATETIME,
       "fornamn" TEXT,
       "efternamn" TEXT,
       "lonespec" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonekorningsnummer"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);

DROP TABLE IF EXISTS "main"."lonetransaktioner";
CREATE TABLE
       "main"."lonetransaktioner" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
	   "transaktion_id" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "utbetalningsgrupp_namn" TEXT,
       "lonekorningsnummer" TEXT,
       "personalkategori" TEXT,
       "loneart_kod" INTEGER,
       "loneart_namn" TEXT,
       "datumstart" DATETIME,
       "datumslut" DATETIME,
       "omfattning_procent" TEXT,
       "antal" TEXT,
       "enhet" TEXT,
       "apris" TEXT,
       "belopp_sek" TEXT,
       "transaktionsrad_text" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "transaktion_id", "lonekorningsnummer"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonekorningsnummer")
		REFERENCES "lonekorningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonekorningsnummer")
);

DROP TABLE IF EXISTS "main"."lonetransaktion_konteringar";
CREATE TABLE
       "main"."lonetransaktion_konteringar" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "utbetalningsgrupp_namn" TEXT,
       "fordelning_id" INTEGER,
       "lonekorningsnummer" TEXT,
       "transaktion_id" INTEGER,
		"dim01_namn" TEXT,
		"dim01_varde" TEXT,
		"dim02_namn" TEXT,
		"dim02_varde" TEXT,
		"dim03_namn" TEXT,
		"dim03_varde" TEXT,
		"dim04_namn" TEXT,
		"dim04_varde" TEXT,
		"dim05_namn" TEXT,
		"dim05_varde" TEXT,
		"dim06_namn" TEXT,
		"dim06_varde" TEXT,
		"dim07_namn" TEXT,
		"dim07_varde" TEXT,
		"dim08_namn" TEXT,
		"dim08_varde" TEXT,
		"dim09_namn" TEXT,
		"dim09_varde" TEXT,
		"dim10_namn" TEXT,
		"dim10_varde" TEXT,
		"procentfordelning" INTEGER,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "fordelning_id", "lonekorningsnummer", "utbetalningsgrupp_id", "transaktion_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonekorningsnummer", "transaktion_id")
		REFERENCES "lonetransaktioner"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonekorningsnummer", "transaktion_id")
);

DROP TABLE IF EXISTS "main"."anstallningsperioder";
CREATE TABLE
       "main"."anstallningsperioder" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "anstallningsperiod_id" TEXT,
       "periodstart" DATETIME,
       "periodslut" DATETIME,
       "anstallningsform" TEXT,
       "avslutsorsak" TEXT,
       "loneform" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "anstallningsperiod_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);

DROP TABLE IF EXISTS "main"."arbetsmatt_heltid";
CREATE TABLE
       "main"."arbetsmatt_heltid" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "arbetsmatt_heltid_id" TEXT,
       "arbetsmatt_heltid" TEXT,
       "arbetsmatt_heltid_startdatum" DATETIME,
       "arbetsmatt_heltid_slutdatum" DATETIME,
	PRIMARY KEY ("system", "artal_start", "artal_slut","organisationsnummer","foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "arbetsmatt_heltid_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);


DROP TABLE IF EXISTS "main"."formelvariabler";
CREATE TABLE
       "main"."formelvariabler" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "variabelnamn" TEXT,
       "beskrivning" TEXT,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "variabelnamn"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer") REFERENCES "arbetsgivare"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer")
);

---------------------------
--CREATE TABLE "main"."hemkonteringar"
-------------------------

DROP TABLE IF EXISTS "main"."kostnadsfordelningar";
CREATE TABLE
       "main"."kostnadsfordelningar" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "kostnadsfordelning_id" TEXT,
	   "ordningsnummer" INTEGER,
       "kostnadsfordelning_startdatum" DATETIME,
       "kostnadsfordelning_slutdatum" DATETIME,
		"dim01_namn" TEXT,
		"dim01_varde" TEXT,
		"dim02_namn" TEXT,
		"dim02_varde" TEXT,
		"dim03_namn" TEXT,
		"dim03_varde" TEXT,
		"dim04_namn" TEXT,
		"dim04_varde" TEXT,
		"dim05_namn" TEXT,
		"dim05_varde" TEXT,
		"dim06_namn" TEXT,
		"dim06_varde" TEXT,
		"dim07_namn" TEXT,
		"dim07_varde" TEXT,
		"dim08_namn" TEXT,
		"dim08_varde" TEXT,
		"dim09_namn" TEXT,
		"dim09_varde" TEXT,
		"dim10_namn" TEXT,
		"dim10_varde" TEXT,
		"procentfordelning" INTEGER,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "kostnadsfordelning_id", ordningsnummer),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);


DROP TABLE IF EXISTS "main"."lonearter";
CREATE TABLE
       "main"."lonearter" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "loneartsnummer" TEXT,
       "personalkategori" TEXT,
       "loneart_kod" TEXT,
       "loneart_namn" TEXT,
       "loneart_formel" TEXT,
       "underlagstyp_skatt" TEXT,
       "loneart_konto" TEXT,
       "loneart_motkonto" TEXT,
       "ej_underlag_soc_avg" BOOLEAN,
       "kostnadsavdrag_soc_avg" BOOLEAN,
       "kostnadsavdrag_soc_avg_procent" TEXT,
       "fora" BOOLEAN,
       "kap_kl" BOOLEAN,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "loneartsnummer", "personalkategori"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer") REFERENCES "arbetsgivare"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer")
);

DROP TABLE IF EXISTS "main"."lonetillagg";
CREATE TABLE
       "main"."lonetillagg" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "lonetillagg_id" TEXT,
       "lonetillagg_namn" TEXT,
       "lonetillagg_varde" TEXT,
       "lonetillagg_startdatum" DATETIME,
       "lonetillagg_slutdatum" DATETIME,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "lonetillagg_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);

DROP TABLE IF EXISTS "main"."manadsloner";
CREATE TABLE
       "main"."manadsloner" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
	   "manadslon_id" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
       "manadslon_heltid_sek" TEXT,
       "manadslon_heltid_sek_startdatum" DATETIME,
       "manadslon_heltid_sek_slutdatum" DATETIME,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "manadslon_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);


DROP TABLE IF EXISTS "main"."timloner";
CREATE TABLE
       "main"."timloner" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
	   "timlon_id" INTEGER,
       "timlon_sek" TEXT,
       "timlon_sek_startdatum" DATETIME,
       "timlon_sek_slutdatum" DATETIME,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "timlon_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);


DROP TABLE IF EXISTS "main"."sysselsattningsgrader";
CREATE TABLE
       "main"."sysselsattningsgrader" ("system" TEXT,
       "artal_start" TEXT,
       "artal_slut" TEXT,
       "organisationsnummer" TEXT,
       "foretagsnummer" TEXT,
       "personnummer" TEXT,
       "anstallningsnummer" INTEGER,
       "utbetalningsgrupp_id" INTEGER,
	   "sysselsattningsgrad_id" INTEGER,
       "sysselsattningsgrad" INTEGER,
       "sysselsattningsgrad_startdatum" DATETIME,
       "sysselsattningsgrad_slutdatum" DATETIME,
	PRIMARY KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id", "sysselsattningsgrad_id"),
	FOREIGN KEY ("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
		REFERENCES "anstallningar"("system", "artal_start", "artal_slut", "organisationsnummer", "foretagsnummer", "personnummer", "anstallningsnummer", "utbetalningsgrupp_id")
);