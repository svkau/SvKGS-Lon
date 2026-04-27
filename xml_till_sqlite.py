#!/usr/bin/env python3
"""
xml_till_sqlite.py

Transformerar ett FGS Personal XML-arkivpaket (SVK-anpassning) till en
SQLite-databas för sökning och publicering med t.ex. Datasette.

Användning:
    python xml_till_sqlite.py <paketmapp> [utdata.db]

Argument:
    paketmapp   Rotkatalog för paketet (t.ex. exempelpaket/)
    utdata.db   Valfri sökväg till SQLite-databasen.
                Standard: <paketmapp>.db

Krav:
    pip install lxml
"""

import sqlite3
import sys
from pathlib import Path
from lxml import etree

NS_EAC  = "urn:isbn:1-931666-33-4"
NS_SVK  = "https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1"
NS_XLINK = "http://www.w3.org/1999/xlink"
E = f"{{{NS_EAC}}}"
S = f"{{{NS_SVK}}}"


def parse(path: Path):
    return etree.parse(str(path)).getroot()


def txt(el, tag: str) -> str | None:
    """Textvärde för första barnelement med givet tag, None om tomt/saknas."""
    child = el.find(tag)
    if child is None:
        return None
    v = (child.text or "").strip()
    return v if v else None


def flt(el, tag: str) -> float | None:
    v = txt(el, tag)
    return float(v) if v is not None else None


# ── DDL ───────────────────────────────────────────────────────────────────────

DDL = """
CREATE TABLE IF NOT EXISTS organisation (
    record_id           TEXT PRIMARY KEY,
    organisationsnummer TEXT,
    foretagsnummer      TEXT,
    namn                TEXT,
    gatuadress          TEXT,
    postnummer          TEXT,
    postort             TEXT
);

CREATE TABLE IF NOT EXISTS personer (
    record_id    TEXT PRIMARY KEY,
    personnummer TEXT,
    pnr_typ      TEXT,   -- PersonalIdentityNumber | CoordinationNumber
    fornamn      TEXT,
    efternamn    TEXT,
    nationalitet TEXT,
    skyddad      INTEGER DEFAULT 0  -- 1 om skyddad identitet
);

CREATE TABLE IF NOT EXISTS anstallningar (
    record_id            TEXT PRIMARY KEY,
    anstallningsnummer   TEXT,
    person_record_id     TEXT REFERENCES personer(record_id),
    bksk_kod             TEXT,
    bksk_klartext        TEXT,
    befattning           TEXT,
    personalkategori     TEXT,
    utbetalningsgrupp_id TEXT,
    manadslon_belopp     REAL,
    manadslon_startdatum TEXT,
    manadslon_slutdatum  TEXT,
    timlon_belopp        REAL,
    timlon_startdatum    TEXT,
    timlon_slutdatum     TEXT
);

CREATE TABLE IF NOT EXISTS anstallningsperioder (
    id                    TEXT PRIMARY KEY,
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    startdatum            TEXT,
    slutdatum             TEXT,
    anstallningsform      TEXT,
    avslutsorsak          TEXT,
    loneform              TEXT
);

CREATE TABLE IF NOT EXISTS sysselsattningsgrader (
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    grad_id               TEXT,
    procent               REAL,
    startdatum            TEXT,
    slutdatum             TEXT,
    PRIMARY KEY (anstallning_record_id, grad_id)
);

CREATE TABLE IF NOT EXISTS heltidsmatt (
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    matt_id               TEXT,
    timmar_per_vecka      REAL,
    startdatum            TEXT,
    slutdatum             TEXT,
    PRIMARY KEY (anstallning_record_id, matt_id)
);

CREATE TABLE IF NOT EXISTS lonetillagg (
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    tillagg_id            TEXT,
    namn                  TEXT,
    varde                 REAL,
    varde_typ             TEXT,   -- belopp | faktor
    valuta                TEXT,
    startdatum            TEXT,
    slutdatum             TEXT,
    PRIMARY KEY (anstallning_record_id, tillagg_id)
);

CREATE TABLE IF NOT EXISTS kostnadsfordelningar (
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    kostnadsfordelning_id TEXT,
    ordningsnummer        INTEGER,
    startdatum            TEXT,
    slutdatum             TEXT,
    procentfordelning     REAL,
    PRIMARY KEY (anstallning_record_id, kostnadsfordelning_id, ordningsnummer)
);

CREATE TABLE IF NOT EXISTS kostnadsfordelning_dimensioner (
    anstallning_record_id TEXT,
    kostnadsfordelning_id TEXT,
    ordningsnummer        INTEGER,
    namn                  TEXT,
    varde                 TEXT,
    PRIMARY KEY (anstallning_record_id, kostnadsfordelning_id, ordningsnummer, namn)
);

CREATE TABLE IF NOT EXISTS standardkonteringar (
    anstallning_record_id TEXT REFERENCES anstallningar(record_id),
    dimension_id          TEXT,
    dimension_namn        TEXT,
    PRIMARY KEY (anstallning_record_id, dimension_id)
);

CREATE TABLE IF NOT EXISTS standardkontering_fordelningar (
    anstallning_record_id TEXT,
    dimension_id          TEXT,
    kontering             TEXT,
    procent               REAL,
    PRIMARY KEY (anstallning_record_id, dimension_id, kontering)
);

CREATE TABLE IF NOT EXISTS utbetalningsgrupper (
    id   TEXT PRIMARY KEY,
    namn TEXT
);

CREATE TABLE IF NOT EXISTS lonearter (
    kod                       TEXT,
    personalkategori          TEXT,
    namn                      TEXT,
    formel                    TEXT,
    underlagstyp_skatt        TEXT,
    konto                     TEXT,
    fora_grundande            INTEGER DEFAULT 0,
    kap_kl_grundande          INTEGER DEFAULT 0,
    ej_socialavgiftsgrundande INTEGER DEFAULT 0,
    PRIMARY KEY (kod, personalkategori)
);

CREATE TABLE IF NOT EXISTS formelvariabler (
    namn        TEXT PRIMARY KEY,
    beskrivning TEXT
);

CREATE TABLE IF NOT EXISTS lonekorningar (
    id                     TEXT PRIMARY KEY,
    lonekorningsnummer     TEXT,
    utbetalningsdatum      TEXT,
    utbetalningsgrupp_id   TEXT,
    anstallningsnummer     TEXT,
    personnummer           TEXT,
    lonespecifikation_href TEXT
);

CREATE TABLE IF NOT EXISTS lonetransaktioner (
    id                 TEXT PRIMARY KEY,
    transaktion_id     TEXT,
    lonekorning_id     TEXT REFERENCES lonekorningar(id),
    personalkategori   TEXT,
    loneart_kod        TEXT,
    loneart_namn       TEXT,
    period_startdatum  TEXT,
    period_slutdatum   TEXT,
    omfattning_procent REAL,
    belopp             REAL,
    valuta             TEXT
);

CREATE TABLE IF NOT EXISTS konteringar (
    id                 TEXT PRIMARY KEY,
    fordelning_id      TEXT,
    lonetransaktion_id TEXT REFERENCES lonetransaktioner(id),
    procentfordelning  REAL
);

CREATE TABLE IF NOT EXISTS kontering_dimensioner (
    kontering_id TEXT REFERENCES konteringar(id),
    namn         TEXT,
    varde        TEXT,
    PRIMARY KEY (kontering_id, namn)
);

CREATE TABLE IF NOT EXISTS lonespecifikationer (
    filnamn        TEXT PRIMARY KEY,
    lonekorning_id TEXT REFERENCES lonekorningar(id),
    html_innehall  TEXT
);
"""

# ── Inläsningsfunktioner ──────────────────────────────────────────────────────

def load_organisation(db, root: Path):
    path = root / "organisation" / "organisation.xml"
    if not path.exists():
        return
    r = parse(path)
    record_id = (r.findtext(f"{E}control/{E}recordId") or "").strip()
    ident = r.find(f"{E}cpfDescription/{E}identity")

    org_nr = foretag_nr = None
    for eid in ident.findall(f"{E}entityId"):
        lt = eid.get("localType", "")
        if lt == "ORG":
            org_nr = (eid.text or "").strip() or None
        elif lt == "FlexForetagsnummer":
            foretag_nr = (eid.text or "").strip() or None

    namn = txt(ident, f"{E}nameEntry/{E}part")

    gatuadress = postnummer = postort = None
    for al in r.findall(f".//{E}addressLine"):
        lt = al.get("localType", "")
        v = (al.text or "").strip() or None
        if lt == "postalAddress":
            gatuadress = v
        elif lt == "postalCode":
            postnummer = v
        elif lt == "postalCity":
            postort = v

    db.execute(
        "INSERT OR REPLACE INTO organisation VALUES (?,?,?,?,?,?,?)",
        (record_id, org_nr, foretag_nr, namn, gatuadress, postnummer, postort),
    )


def load_personer(db, root: Path):
    for path in sorted((root / "personer").glob("P_*.xml")):
        r = parse(path)
        record_id = (r.findtext(f"{E}control/{E}recordId") or "").strip()
        ident = r.find(f"{E}cpfDescription/{E}identity")

        pnr = pnr_typ = None
        for eid in ident.findall(f"{E}entityId"):
            lt = eid.get("localType", "")
            if lt in ("PersonalIdentityNumber", "CoordinationNumber"):
                pnr = (eid.text or "").strip() or None
                pnr_typ = lt

        fornamn = next(
            ((el.findtext(f"{E}part") or "").strip() or None
             for el in ident.findall(f"{E}nameEntry")
             if el.get("localType") == "forename"),
            None,
        )
        efternamn = next(
            ((el.findtext(f"{E}part") or "").strip() or None
             for el in ident.findall(f"{E}nameEntry")
             if el.get("localType") == "surname"),
            None,
        )

        desc = r.find(f"{E}cpfDescription/{E}description")
        nationalitet = skyddad = None
        if desc is not None:
            nat = desc.find(f".//{E}localDescription[@localType='nationality']/{E}term")
            nationalitet = (nat.text or "").strip() or None if nat is not None else None
            note = desc.find(f".//{E}descriptiveNote/{E}p")
            skyddad = 1 if note is not None and "skyddad" in (note.text or "").lower() else 0

        db.execute(
            "INSERT OR REPLACE INTO personer VALUES (?,?,?,?,?,?,?)",
            (record_id, pnr, pnr_typ, fornamn, efternamn, nationalitet, skyddad or 0),
        )


def load_anstallningar(db, root: Path):
    for path in sorted((root / "anstallningar").glob("F_*.xml")):
        r = parse(path)
        record_id = (r.findtext(f"{E}control/{E}recordId") or "").strip()
        emp = r.find(f"{E}cpfDescription/{E}employmentDescription")
        if emp is None:
            continue

        anst_nr = (emp.findtext(f"{E}employmentId") or "").strip() or None

        # Person-relation via creatorOf -> A_PNR -> P_PNR
        person_record_id = None
        for rel in r.findall(f"{E}relations/{E}cpfRelation"):
            if rel.get("cpfRelationType") == "creatorOf":
                href = rel.get(f"{{{NS_XLINK}}}href", "")
                fragment = href.split("#")[-1] if "#" in href else ""
                if fragment.startswith("A_"):
                    person_record_id = "P_" + fragment[2:]

        # Befattning (BKSK-term + fritext)
        pos = emp.find(f"{E}positions/{E}position")
        bksk_kod = bksk_klartext = befattning = None
        if pos is not None:
            term_el = pos.find(f"{E}term")
            if term_el is not None:
                bksk_kod = term_el.get("code") or None
                bksk_klartext = (term_el.text or "").strip() or None
            desc_el = pos.find(f"{E}description")
            befattning = (desc_el.text or "").strip() if desc_el is not None else None

        # Grundlön (senaste salaryAgreement per typ)
        manadslon_belopp = manadslon_start = manadslon_slut = None
        timlon_belopp = timlon_start = timlon_slut = None
        for sa in emp.findall(f"{E}salaryAgreements/{E}salaryAgreement"):
            sal_typ = sa.get("salaryType", "")
            amount = sa.get("amount")
            start = sa.findtext(f".//{E}startDate", "").strip() or None
            end = sa.findtext(f".//{E}endDate", "").strip() or None
            if sal_typ == "monthlyPay":
                manadslon_belopp = float(amount) if amount else None
                manadslon_start, manadslon_slut = start, end
            elif sal_typ == "hourlyPay":
                timlon_belopp = float(amount) if amount else None
                timlon_start, timlon_slut = start, end

        # SVK-tillägg
        tillagg = emp.find(f".//{S}anstallningstillagg")
        personalkategori = utbetalningsgrupp_id = None
        if tillagg is not None:
            personalkategori = txt(tillagg, f"{S}personalkategori/{S}kod")
            utbetalningsgrupp_id = txt(tillagg, f"{S}utbetalningsgruppReferens/{S}id")

        db.execute(
            "INSERT OR REPLACE INTO anstallningar VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (record_id, anst_nr, person_record_id, bksk_kod, bksk_klartext,
             befattning, personalkategori, utbetalningsgrupp_id,
             manadslon_belopp, manadslon_start, manadslon_slut,
             timlon_belopp, timlon_start, timlon_slut),
        )

        if tillagg is None:
            continue

        # Anställningsperioder
        for ap in tillagg.findall(f"{S}anstallningsperioder/{S}anstallningsperiod"):
            ap_id = (ap.findtext(f"{S}id") or "").strip()
            gp = ap.find(f"{S}giltighetsperiod")
            start = (gp.findtext(f"{S}startdatum") or "").strip() or None if gp is not None else None
            slut = (gp.findtext(f"{S}slutdatum") or "").strip() or None if gp is not None else None
            db.execute(
                "INSERT OR REPLACE INTO anstallningsperioder VALUES (?,?,?,?,?,?,?)",
                (ap_id, record_id, start, slut,
                 txt(ap, f"{S}anstallningsform"),
                 txt(ap, f"{S}avslutsorsak"),
                 txt(ap, f"{S}loneform")),
            )

        # Sysselsättningsgrader
        for sg in tillagg.findall(f"{S}sysselsattningsgrader/{S}sysselsattningsgrad"):
            sg_id = (sg.findtext(f"{S}id") or "").strip()
            procent_txt = (sg.findtext(f"{S}procent") or "").strip()
            gp = sg.find(f"{S}giltighetsperiod")
            start = (gp.findtext(f"{S}startdatum") or "").strip() or None if gp is not None else None
            slut = (gp.findtext(f"{S}slutdatum") or "").strip() or None if gp is not None else None
            db.execute(
                "INSERT OR REPLACE INTO sysselsattningsgrader VALUES (?,?,?,?,?)",
                (record_id, sg_id, float(procent_txt) if procent_txt else None, start, slut),
            )

        # Heltidsmått
        for am in tillagg.findall(f"{S}heltidsmatt/{S}arbetsmatt"):
            am_id = (am.findtext(f"{S}id") or "").strip()
            timmar_txt = (am.findtext(f"{S}timmarPerVecka") or "").strip()
            gp = am.find(f"{S}giltighetsperiod")
            start = (gp.findtext(f"{S}startdatum") or "").strip() or None if gp is not None else None
            slut = (gp.findtext(f"{S}slutdatum") or "").strip() or None if gp is not None else None
            db.execute(
                "INSERT OR REPLACE INTO heltidsmatt VALUES (?,?,?,?,?)",
                (record_id, am_id, float(timmar_txt) if timmar_txt else None, start, slut),
            )

        # Lönetillägg
        for tl in tillagg.findall(f"{S}lonetillagg/{S}tillagg"):
            tl_id = (tl.findtext(f"{S}id") or "").strip()
            varde_el = tl.find(f"{S}varde")
            varde = varde_typ = None
            if varde_el is not None:
                varde_typ = varde_el.get("typ")
                varde_txt = (varde_el.text or "").strip()
                varde = float(varde_txt) if varde_txt else None
            gp = tl.find(f"{S}giltighetsperiod")
            start = (gp.findtext(f"{S}startdatum") or "").strip() or None if gp is not None else None
            slut = (gp.findtext(f"{S}slutdatum") or "").strip() or None if gp is not None else None
            db.execute(
                "INSERT OR REPLACE INTO lonetillagg VALUES (?,?,?,?,?,?,?,?)",
                (record_id, tl_id, txt(tl, f"{S}namn"), varde, varde_typ,
                 txt(tl, f"{S}valuta"), start, slut),
            )

        # Kostnadsfördelningar
        for kf in tillagg.findall(f"{S}kostnadsfordelningar/{S}kostnadsfordelning"):
            kf_id = (kf.findtext(f"{S}kostnadsfordelningId") or "").strip()
            ordning_txt = (kf.findtext(f"{S}ordningsnummer") or "").strip()
            ordning = int(ordning_txt) if ordning_txt else None
            gp = kf.find(f"{S}giltighetsperiod")
            start = (gp.findtext(f"{S}startdatum") or "").strip() or None if gp is not None else None
            slut = (gp.findtext(f"{S}slutdatum") or "").strip() or None if gp is not None else None
            pct_txt = (kf.findtext(f"{S}procentfordelning") or "").strip()
            pct = float(pct_txt) if pct_txt else None
            db.execute(
                "INSERT OR REPLACE INTO kostnadsfordelningar VALUES (?,?,?,?,?,?)",
                (record_id, kf_id, ordning, start, slut, pct),
            )
            for dim in kf.findall(f"{S}dimensioner/{S}dimension"):
                d_namn = (dim.findtext(f"{S}namn") or "").strip()
                d_varde = (dim.findtext(f"{S}varde") or "").strip() or None
                db.execute(
                    "INSERT OR REPLACE INTO kostnadsfordelning_dimensioner VALUES (?,?,?,?,?)",
                    (record_id, kf_id, ordning, d_namn, d_varde),
                )

        # Standardkonteringar (hemkonteringar)
        for sk in tillagg.findall(f"{S}standardkonteringar/{S}standardkontering"):
            dim_id = (sk.findtext(f"{S}dimensionId") or "").strip()
            dim_namn = txt(sk, f"{S}dimensionNamn")
            db.execute(
                "INSERT OR REPLACE INTO standardkonteringar VALUES (?,?,?)",
                (record_id, dim_id, dim_namn),
            )
            for fd in sk.findall(f"{S}fordelningar/{S}fordelning"):
                kontering = txt(fd, f"{S}kontering")
                procent_txt = (fd.findtext(f"{S}procent") or "").strip()
                procent = float(procent_txt) if procent_txt else None
                db.execute(
                    "INSERT OR REPLACE INTO standardkontering_fordelningar VALUES (?,?,?,?)",
                    (record_id, dim_id, kontering, procent),
                )


def load_lonekorningar(db, root: Path):
    path = root / "loneutbetalningar" / "lonekorningar.xml"
    if not path.exists():
        return
    r = parse(path)
    for lk in r.findall(f"{S}lonekorning"):
        lk_id = (lk.findtext(f"{S}id") or "").strip()
        spec_el = lk.find(f"{S}lonespecifikation")
        spec_href = spec_el.get("href") if spec_el is not None else None
        db.execute(
            "INSERT OR REPLACE INTO lonekorningar VALUES (?,?,?,?,?,?,?)",
            (lk_id,
             txt(lk, f"{S}lonekorningsnummer"),
             txt(lk, f"{S}utbetalningsdatum"),
             txt(lk, f"{S}utbetalningsgruppReferens/{S}id"),
             txt(lk, f"{S}anstallningReferens/{S}anstallningsnummer"),
             txt(lk, f"{S}anstallningReferens/{S}personnummer"),
             spec_href),
        )


def load_lonetransaktioner(db, root: Path):
    path = root / "loneutbetalningar" / "lonetransaktioner.xml"
    if not path.exists():
        return
    r = parse(path)
    for lt in r.findall(f"{S}lonetransaktion"):
        lt_id = (lt.findtext(f"{S}id") or "").strip()
        per = lt.find(f"{S}period")
        per_start = (per.findtext(f"{S}startdatum") or "").strip() or None if per is not None else None
        per_slut = (per.findtext(f"{S}slutdatum") or "").strip() or None if per is not None else None
        omf_txt = (lt.findtext(f"{S}omfattningProcent") or "").strip()
        bel_txt = (lt.findtext(f"{S}belopp") or "").strip()
        db.execute(
            "INSERT OR REPLACE INTO lonetransaktioner VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (lt_id,
             txt(lt, f"{S}transaktionId"),
             txt(lt, f"{S}lonekorningReferens"),
             txt(lt, f"{S}personalkategori"),
             txt(lt, f"{S}loneart/{S}kod"),
             txt(lt, f"{S}loneart/{S}namn"),
             per_start, per_slut,
             float(omf_txt) if omf_txt else None,
             float(bel_txt) if bel_txt else None,
             txt(lt, f"{S}valuta")),
        )


def load_konteringar(db, root: Path):
    path = root / "loneutbetalningar" / "konteringar.xml"
    if not path.exists():
        return
    r = parse(path)
    for k in r.findall(f"{S}kontering"):
        k_id = (k.findtext(f"{S}id") or "").strip()
        pct_txt = (k.findtext(f"{S}procentfordelning") or "").strip()
        db.execute(
            "INSERT OR REPLACE INTO konteringar VALUES (?,?,?,?)",
            (k_id,
             txt(k, f"{S}fordelningId"),
             txt(k, f"{S}lonetransaktionReferens"),
             float(pct_txt) if pct_txt else None),
        )
        for dim in k.findall(f"{S}dimensioner/{S}dimension"):
            d_namn = (dim.findtext(f"{S}namn") or "").strip()
            d_varde = (dim.findtext(f"{S}varde") or "").strip() or None
            db.execute(
                "INSERT OR REPLACE INTO kontering_dimensioner VALUES (?,?,?)",
                (k_id, d_namn, d_varde),
            )


def load_register(db, root: Path):
    # Utbetalningsgrupper
    path = root / "register" / "utbetalningsgrupper.xml"
    if path.exists():
        r = parse(path)
        for ug in r.findall(f"{S}utbetalningsgrupp"):
            db.execute(
                "INSERT OR REPLACE INTO utbetalningsgrupper VALUES (?,?)",
                (txt(ug, f"{S}id"), txt(ug, f"{S}namn")),
            )

    # Lönearter
    path = root / "register" / "lonearter.xml"
    if path.exists():
        r = parse(path)
        for la in r.findall(f"{S}loneart"):
            formel_el = la.find(f"{S}formel")
            formel = (formel_el.text or "").strip() or None if formel_el is not None else None
            eg = la.find(f"{S}egenskaper")
            fora = kap = ej_social = 0
            if eg is not None:
                fora = 1 if txt(eg, f"{S}foraGrundande") == "true" else 0
                kap = 1 if txt(eg, f"{S}kapKlGrundande") == "true" else 0
                ej_social = 1 if txt(eg, f"{S}ejSocialavgiftsgrundande") == "true" else 0
            db.execute(
                "INSERT OR REPLACE INTO lonearter VALUES (?,?,?,?,?,?,?,?,?)",
                (txt(la, f"{S}kod"),
                 txt(la, f"{S}personalkategori"),
                 txt(la, f"{S}namn"),
                 formel,
                 txt(la, f"{S}underlagstypSkatt"),
                 txt(la, f"{S}kontering/{S}konto"),
                 fora, kap, ej_social),
            )

    # Formelvariabler
    path = root / "register" / "formelvariabler.xml"
    if path.exists():
        r = parse(path)
        for fv in r.findall(f"{S}formelvariabel"):
            db.execute(
                "INSERT OR REPLACE INTO formelvariabler VALUES (?,?)",
                (txt(fv, f"{S}namn"), txt(fv, f"{S}beskrivning")),
            )


def load_lonespecifikationer(db, root: Path):
    spec_dir = root / "lonespecifikationer"
    if not spec_dir.is_dir():
        return

    # Bygg mappning filnamn -> lonekorning_id utifrån lonespecifikation_href
    href_to_lk: dict[str, str] = {}
    for lk_id, href in db.execute(
        "SELECT id, lonespecifikation_href FROM lonekorningar WHERE lonespecifikation_href IS NOT NULL"
    ):
        # href är relativ från loneutbetalningar/, t.ex. "lonespecifikationer/foo.html"
        href_to_lk[Path(href).name] = lk_id

    for html_path in sorted(spec_dir.iterdir()):
        if not html_path.is_file():
            continue
        filename = html_path.name
        lk_id = href_to_lk.get(filename)
        try:
            innehall = html_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            innehall = html_path.read_text(encoding="latin-1")
        db.execute(
            "INSERT OR REPLACE INTO lonespecifikationer VALUES (?,?,?)",
            (filename, lk_id, innehall),
        )


# ── Huvud ─────────────────────────────────────────────────────────────────────

def transformera(paket_dir: str, db_path: str | None = None):
    root = Path(paket_dir)
    if not root.is_dir():
        print(f"Fel: {paket_dir} är inte en katalog", file=sys.stderr)
        sys.exit(1)

    if db_path is None:
        db_path = str(root).rstrip("/") + ".db"

    print(f"Läser paket från {root} ...")
    print(f"Skriver till    {db_path} ...")

    con = sqlite3.connect(db_path)
    con.executescript(DDL)
    con.execute("PRAGMA foreign_keys = ON")

    with con:
        print("  organisation")
        load_organisation(con, root)
        print("  personer")
        load_personer(con, root)
        print("  anstallningar + SVK-tillägg")
        load_anstallningar(con, root)
        print("  lonekorningar")
        load_lonekorningar(con, root)
        print("  lonetransaktioner")
        load_lonetransaktioner(con, root)
        print("  konteringar")
        load_konteringar(con, root)
        print("  register (utbetalningsgrupper, lonearter, formelvariabler)")
        load_register(con, root)
        print("  lonespecifikationer (HTML)")
        load_lonespecifikationer(con, root)

    con.execute("ANALYZE")
    con.close()

    # Summering
    con2 = sqlite3.connect(db_path)
    tables = [r[0] for r in con2.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )]
    print("\nTabell                              Rader")
    print("─" * 45)
    for tbl in tables:
        count = con2.execute(f"SELECT count(*) FROM [{tbl}]").fetchone()[0]
        print(f"  {tbl:<34} {count:>5}")
    con2.close()

    print(f"\nKlart! Databasen finns i: {db_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Användning: python xml_till_sqlite.py <paketmapp> [utdata.db]")
        sys.exit(1)
    transformera(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
