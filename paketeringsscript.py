#!/usr/bin/env python3
"""
paketeringsscript.py

Konverterar Flex Lön CSV-uttag till XML-arkivpaket enligt
Svenska kyrkans anpassning av FGS Personal.

Användning:
    python paketeringsscript.py <csv-katalog> [utdata-katalog]

Argument:
    csv-katalog     Katalog med CSV-filer (t.ex. csv/0987654321)
    utdata-katalog  Valfri utdatakatalog. Standard: <csv-katalog>_paket

Krav:
    pip install lxml
"""

import csv
import sys
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from lxml import etree

# ── Namnrymder ───────────────────────────────────────────────────────────────
NS_EAC   = "urn:isbn:1-931666-33-4"
NS_XLINK = "http://www.w3.org/1999/xlink"
NS_SVK   = "https://earkiv.svenskakyrkan.se/schemas/SVK-personal-lon/v1"

NSMAP_EAC = {None: NS_EAC, "xlink": NS_XLINK, "svk": NS_SVK}
NSMAP_SVK = {None: NS_SVK}

# Fiktiva "tills vidare"-datum
TILLS_VIDARE = {"2049-01-01"}


# ── Hjälpfunktioner ───────────────────────────────────────────────────────────

def read_csv(filepath: Path) -> list[dict]:
    """Läser pipe-avgränsad CSV med UTF-8 BOM-hantering."""
    with open(filepath, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="|"))


def strip_date(value: str, omit_tills_vidare: bool = True) -> str | None:
    """Konverterar YYYY-MM-DDTHH:MM:SS -> YYYY-MM-DD. None för tomma/fiktiva datum."""
    if not value or not value.strip():
        return None
    d = value.strip().split("T")[0]
    if omit_tills_vidare and d in TILLS_VIDARE:
        return None
    return d or None


def clean_pnr(pnr: str) -> str:
    """Returnerar personnummer utan omgivande blanksteg, tom sträng om bara blankt."""
    return pnr.strip() if pnr else ""


def pnr_to_id(pnr: str) -> str:
    """Tar bort bindestreck för ID-användning: 19760628-0696 -> 197606280696."""
    return pnr.replace("-", "")


def is_samordningsnummer(pnr: str) -> bool:
    """Samordningsnummer har dagsiffra >= 61 (födelsedag + 60)."""
    p = pnr.replace("-", "")
    if len(p) >= 8:
        try:
            return int(p[6:8]) >= 61
        except ValueError:
            pass
    return False


def nonempty(s: str) -> str | None:
    """None för tomma/blank strängar, annars .strip()."""
    v = s.strip() if s else ""
    return v if v else None


def sub(parent, tag: str, text: str | None = None, **attribs):
    """Skapar SubElement och sätter eventuellt textinnehåll."""
    el = etree.SubElement(parent, tag, **attribs)
    if text is not None:
        el.text = text
    return el


def write_xml(path: Path, root) -> None:
    etree.ElementTree(root).write(
        path, xml_declaration=True, encoding="UTF-8", pretty_print=True
    )


# ── EAC-CPF control-block ─────────────────────────────────────────────────────

def add_control(parent, record_id: str, agency_name: str, creation_date: str) -> None:
    ctrl = sub(parent, f"{{{NS_EAC}}}control")
    sub(ctrl, f"{{{NS_EAC}}}recordId", record_id)
    sub(ctrl, f"{{{NS_EAC}}}maintenanceStatus", "revised")
    agency = sub(ctrl, f"{{{NS_EAC}}}maintenanceAgency")
    sub(agency, f"{{{NS_EAC}}}agencyName", agency_name)
    hist = sub(ctrl, f"{{{NS_EAC}}}maintenanceHistory")
    ev = sub(hist, f"{{{NS_EAC}}}maintenanceEvent")
    sub(ev, f"{{{NS_EAC}}}eventType", "created")
    sub(ev, f"{{{NS_EAC}}}eventDateTime", creation_date,
        standardDateTime=f"{creation_date}T00:00:00")
    sub(ev, f"{{{NS_EAC}}}agentType", "machine")
    sub(ev, f"{{{NS_EAC}}}agent", "Flex Lön export / paketeringsscript.py")


def add_giltighetsperiod(parent, start: str | None, slut: str | None) -> None:
    gp = sub(parent, f"{{{NS_SVK}}}giltighetsperiod")
    if start:
        sub(gp, f"{{{NS_SVK}}}startdatum", start)
    if slut:
        sub(gp, f"{{{NS_SVK}}}slutdatum", slut)


def extract_dimensions(row: dict) -> list[tuple[str, str]]:
    """Extraherar icke-tomma dim01..dim10 par från en CSV-rad."""
    dims = []
    for i in range(1, 11):
        n = row.get(f"dim{i:02d}_namn", "").strip()
        v = row.get(f"dim{i:02d}_varde", "").strip()
        if n:
            dims.append((n, v))
    return dims


# ── Organisation ──────────────────────────────────────────────────────────────

def build_organisation(ag: dict, agency_name: str, creation_date: str,
                       org_record_id: str) -> etree._Element:
    root = etree.Element(f"{{{NS_EAC}}}eac-cpf", nsmap=NSMAP_EAC)
    add_control(root, org_record_id, agency_name, creation_date)

    cpf = sub(root, f"{{{NS_EAC}}}cpfDescription")
    identity = sub(cpf, f"{{{NS_EAC}}}identity")
    sub(identity, f"{{{NS_EAC}}}entityType", "corporateBody")
    sub(identity, f"{{{NS_EAC}}}entityId", ag["organisationsnummer"].strip(),
        localType="ORG")
    sub(identity, f"{{{NS_EAC}}}entityId", ag["foretagsnummer"].strip(),
        localType="FlexForetagsnummer")
    if v := nonempty(ag.get("fora_forsakringsnummer", "")):
        sub(identity, f"{{{NS_EAC}}}entityId", v, localType="FORA")
    if v := nonempty(ag.get("kapkl_kundnummer", "")):
        sub(identity, f"{{{NS_EAC}}}entityId", v, localType="KAPKL")
    ne = sub(identity, f"{{{NS_EAC}}}nameEntry")
    sub(ne, f"{{{NS_EAC}}}part", agency_name)

    desc = sub(cpf, f"{{{NS_EAC}}}description")
    places = sub(desc, f"{{{NS_EAC}}}places")
    place = sub(places, f"{{{NS_EAC}}}place")
    addr = sub(place, f"{{{NS_EAC}}}address")
    if v := nonempty(ag.get("gatuadress", "")):
        sub(addr, f"{{{NS_EAC}}}addressLine", v, localType="postalAddress")
    if v := nonempty(ag.get("postnummer", "")):
        sub(addr, f"{{{NS_EAC}}}addressLine", v, localType="postalCode")
    if v := nonempty(ag.get("postort", "")):
        sub(addr, f"{{{NS_EAC}}}addressLine", v, localType="postalCity")

    return root


# ── Person ────────────────────────────────────────────────────────────────────

def build_person(pnr: str, fornamn: str, efternamn: str, nationalitet: str,
                 skyddad: bool, agency_name: str, creation_date: str) -> etree._Element:
    pnr_id = pnr_to_id(pnr)
    root = etree.Element(f"{{{NS_EAC}}}eac-cpf", nsmap=NSMAP_EAC)
    add_control(root, f"P_{pnr_id}", agency_name, creation_date)

    cpf = sub(root, f"{{{NS_EAC}}}cpfDescription")
    identity = sub(cpf, f"{{{NS_EAC}}}identity")
    sub(identity, f"{{{NS_EAC}}}entityType", "person")
    local_type = "CoordinationNumber" if is_samordningsnummer(pnr) else "PersonalIdentityNumber"
    sub(identity, f"{{{NS_EAC}}}entityId", pnr, localType=local_type)
    fn = sub(identity, f"{{{NS_EAC}}}nameEntry", localType="forename")
    sub(fn, f"{{{NS_EAC}}}part", fornamn)
    en = sub(identity, f"{{{NS_EAC}}}nameEntry", localType="surname")
    sub(en, f"{{{NS_EAC}}}part", efternamn)

    desc = sub(cpf, f"{{{NS_EAC}}}description")
    nat = sub(desc, f"{{{NS_EAC}}}localDescription", localType="nationality")
    sub(nat, f"{{{NS_EAC}}}term", nationalitet or "")
    if skyddad:
        note = sub(desc, f"{{{NS_EAC}}}descriptiveNote")
        sub(note, f"{{{NS_EAC}}}p", "Skyddad identitet")

    return root


# ── Arbetstagare ──────────────────────────────────────────────────────────────

def build_arbetstagare(pnr: str, fornamn: str, efternamn: str, agency_name: str,
                       creation_date: str, org_record_id: str) -> etree._Element:
    pnr_id = pnr_to_id(pnr)
    root = etree.Element(f"{{{NS_EAC}}}eac-cpf", nsmap=NSMAP_EAC)
    add_control(root, f"A_{pnr_id}", agency_name, creation_date)

    cpf = sub(root, f"{{{NS_EAC}}}cpfDescription")
    identity = sub(cpf, f"{{{NS_EAC}}}identity")
    sub(identity, f"{{{NS_EAC}}}entityType", "person")
    ne = sub(identity, f"{{{NS_EAC}}}nameEntry")
    sub(ne, f"{{{NS_EAC}}}part", f"{fornamn} {efternamn}".strip())

    relations = sub(root, f"{{{NS_EAC}}}relations")
    sub(relations, f"{{{NS_EAC}}}cpfRelation",
        cpfRelationType="isEmployedBy",
        **{f"{{{NS_XLINK}}}type": "simple",
           f"{{{NS_XLINK}}}href": f"../organisation/organisation.xml#{org_record_id}"})
    sub(relations, f"{{{NS_EAC}}}cpfRelation",
        cpfRelationType="sameAs",
        **{f"{{{NS_XLINK}}}type": "simple",
           f"{{{NS_XLINK}}}href": f"../personer/P_{pnr_id}.xml#P_{pnr_id}"})

    return root


# ── Anställning ───────────────────────────────────────────────────────────────

def build_anstallning(anst: dict, manadsloner: list, timloner: list,
                      anstperioder: list, syssgrader: list, heltidsmatt: list,
                      lonetillagg: list, kostnadsfordelningar: list,
                      hemkonteringar: list, agency_name: str,
                      creation_date: str, org_record_id: str) -> etree._Element:
    nr  = anst["anstallningsnummer"].strip()
    pnr = clean_pnr(anst["personnummer"])

    root = etree.Element(f"{{{NS_EAC}}}eac-cpf", nsmap=NSMAP_EAC)
    add_control(root, f"F_{nr}", agency_name, creation_date)

    cpf     = sub(root, f"{{{NS_EAC}}}cpfDescription")
    emp     = sub(cpf,  f"{{{NS_EAC}}}employmentDescription")
    sub(emp, f"{{{NS_EAC}}}employmentId", nr)

    # Befattning
    positions = sub(emp, f"{{{NS_EAC}}}positions")
    pos = sub(positions, f"{{{NS_EAC}}}position")
    if bksk := nonempty(anst.get("bksk_kod", "")):
        klartext = nonempty(anst.get("bksk_klartext", "")) or ""
        sub(pos, f"{{{NS_EAC}}}term", klartext, source="BKSK", code=bksk)
    if befattning := nonempty(anst.get("befattning", "")):
        sub(pos, f"{{{NS_EAC}}}description", befattning)

    # Grundlöner
    salary_rows = (
        [("monthlyPay", r["manadslon_heltid_sek"],
          r["manadslon_heltid_sek_startdatum"], r["manadslon_heltid_sek_slutdatum"])
         for r in manadsloner]
        + [("hourlyWage", r["timlon_sek"],
            r["timlon_sek_startdatum"], r["timlon_sek_slutdatum"])
           for r in timloner]
    )
    if salary_rows:
        sal_agr = sub(emp, f"{{{NS_EAC}}}salaryAgreements")
        for sal_type, amount, start_raw, slut_raw in salary_rows:
            start = strip_date(start_raw)
            if not start:
                continue
            sa = sub(sal_agr, f"{{{NS_EAC}}}salaryAgreement",
                     salaryType=sal_type, amount=amount.strip(), currency="SEK")
            sp = sub(sa, f"{{{NS_EAC}}}salaryPeriod")
            dr = sub(sp, f"{{{NS_EAC}}}dateRange")
            sub(dr, f"{{{NS_EAC}}}startDate", start)
            if slut := strip_date(slut_raw):
                sub(dr, f"{{{NS_EAC}}}endDate", slut)

    # additionalXMLData / anstallningstillagg
    add_el  = sub(emp, f"{{{NS_EAC}}}additionalElements")
    add_xml = sub(add_el, f"{{{NS_EAC}}}additionalXMLData")
    tillagg = sub(add_xml, f"{{{NS_SVK}}}anstallningstillagg")

    if ug := nonempty(anst.get("utbetalningsgrupp_id", "")):
        ug_ref = sub(tillagg, f"{{{NS_SVK}}}utbetalningsgruppReferens")
        sub(ug_ref, f"{{{NS_SVK}}}id", ug)

    if pk := nonempty(anst.get("personalkategori", "")):
        pk_el = sub(tillagg, f"{{{NS_SVK}}}personalkategori")
        sub(pk_el, f"{{{NS_SVK}}}kod", pk)

    if anstperioder:
        aps = sub(tillagg, f"{{{NS_SVK}}}anstallningsperioder")
        for ap in anstperioder:
            ap_el = sub(aps, f"{{{NS_SVK}}}anstallningsperiod")
            sub(ap_el, f"{{{NS_SVK}}}id", ap["anstallningsperiod_id"].strip())
            add_giltighetsperiod(ap_el,
                                 strip_date(ap["periodstart"]),
                                 strip_date(ap["periodslut"]))
            sub(ap_el, f"{{{NS_SVK}}}anstallningsform", ap["anstallningsform"].strip())
            sub(ap_el, f"{{{NS_SVK}}}loneform", ap["loneform"].strip())
            if avs := nonempty(ap.get("avslutsorsak", "")):
                sub(ap_el, f"{{{NS_SVK}}}avslutsorsak", avs)

    if syssgrader:
        sgs = sub(tillagg, f"{{{NS_SVK}}}sysselsattningsgrader")
        for sg in syssgrader:
            sg_el = sub(sgs, f"{{{NS_SVK}}}sysselsattningsgrad")
            sub(sg_el, f"{{{NS_SVK}}}id", sg["sysselsattningsgrad_id"].strip())
            sub(sg_el, f"{{{NS_SVK}}}procent", sg["sysselsattningsgrad"].strip())
            add_giltighetsperiod(sg_el,
                                 strip_date(sg["sysselsattningsgrad_startdatum"]),
                                 strip_date(sg["sysselsattningsgrad_slutdatum"]))

    if heltidsmatt:
        hm = sub(tillagg, f"{{{NS_SVK}}}heltidsmatt")
        for h in heltidsmatt:
            am = sub(hm, f"{{{NS_SVK}}}arbetsmatt")
            sub(am, f"{{{NS_SVK}}}id", h["arbetsmatt_heltid_id"].strip())
            sub(am, f"{{{NS_SVK}}}timmarPerVecka", h["arbetsmatt_heltid"].strip())
            add_giltighetsperiod(am,
                                 strip_date(h["arbetsmatt_heltid_startdatum"]),
                                 strip_date(h["arbetsmatt_heltid_slutdatum"]))

    if lonetillagg:
        lt_cont = sub(tillagg, f"{{{NS_SVK}}}lonetillagg")
        for lt in lonetillagg:
            tl = sub(lt_cont, f"{{{NS_SVK}}}tillagg")
            sub(tl, f"{{{NS_SVK}}}id",   lt["lonetillagg_id"].strip())
            sub(tl, f"{{{NS_SVK}}}namn", lt["lonetillagg_namn"].strip())
            varde_val = lt["lonetillagg_varde"].strip()
            # Heuristik: decimaler <= 10 tolkas som faktor, övriga som belopp.
            # Granska manuellt vid oklara fall.
            try:
                typ = "faktor" if float(varde_val) <= 10 and "." in varde_val else "belopp"
            except ValueError:
                typ = "belopp"
            sub(tl, f"{{{NS_SVK}}}varde", varde_val, typ=typ)
            if typ == "belopp":
                sub(tl, f"{{{NS_SVK}}}valuta", "SEK")
            add_giltighetsperiod(tl,
                                 strip_date(lt["lonetillagg_startdatum"]),
                                 strip_date(lt["lonetillagg_slutdatum"]))

    if kostnadsfordelningar:
        kf_cont = sub(tillagg, f"{{{NS_SVK}}}kostnadsfordelningar")
        for kf in kostnadsfordelningar:
            dims = extract_dimensions(kf)
            if not dims:
                continue
            kf_el = sub(kf_cont, f"{{{NS_SVK}}}kostnadsfordelning")
            sub(kf_el, f"{{{NS_SVK}}}kostnadsfordelningId", kf["kostnadsfordelning_id"].strip())
            sub(kf_el, f"{{{NS_SVK}}}ordningsnummer", kf["ordningsnummer"].strip())
            add_giltighetsperiod(kf_el,
                                 strip_date(kf["kostnadsfordelning_startdatum"]),
                                 strip_date(kf["kostnadsfordelning_slutdatum"]))
            sub(kf_el, f"{{{NS_SVK}}}procentfordelning", kf["procentfordelning"].strip())
            dims_el = sub(kf_el, f"{{{NS_SVK}}}dimensioner")
            for n, v in dims:
                dim = sub(dims_el, f"{{{NS_SVK}}}dimension")
                sub(dim, f"{{{NS_SVK}}}namn", n)
                sub(dim, f"{{{NS_SVK}}}varde", v)

    if hemkonteringar:
        sk_cont = sub(tillagg, f"{{{NS_SVK}}}standardkonteringar")
        for hk in hemkonteringar:
            sk = sub(sk_cont, f"{{{NS_SVK}}}standardkontering")
            sub(sk, f"{{{NS_SVK}}}dimensionId",   hk["dimension_id"].strip())
            sub(sk, f"{{{NS_SVK}}}dimensionNamn", hk["dimension_namn"].strip())
            ford = sub(sk, f"{{{NS_SVK}}}fordelningar")
            for i in range(1, 6):
                k = nonempty(hk.get(f"kontering{i}", ""))
                p = nonempty(hk.get(f"procent{i}", ""))
                if k and p:
                    f_el = sub(ford, f"{{{NS_SVK}}}fordelning")
                    sub(f_el, f"{{{NS_SVK}}}kontering", k)
                    sub(f_el, f"{{{NS_SVK}}}procent", p)

    # Relationer (om personnummer finns)
    if pnr:
        pnr_id = pnr_to_id(pnr)
        relations = sub(root, f"{{{NS_EAC}}}relations")
        sub(relations, f"{{{NS_EAC}}}cpfRelation",
            cpfRelationType="creatorOf",
            **{f"{{{NS_XLINK}}}type": "simple",
               f"{{{NS_XLINK}}}href": f"../arbetstagare/A_{pnr_id}.xml#A_{pnr_id}"})
        sub(relations, f"{{{NS_EAC}}}cpfRelation",
            cpfRelationType="isAssociatedWith",
            **{f"{{{NS_XLINK}}}type": "simple",
               f"{{{NS_XLINK}}}href": f"../organisation/organisation.xml#{org_record_id}"})

    return root


# ── Lönekörningar ─────────────────────────────────────────────────────────────

def build_lonekorningar(rows: list, artal: str) -> tuple[etree._Element, dict]:
    """Returnerar (root, lk_lookup) där lk_lookup: (pnr, anstNr, lkNr) -> LK_id."""
    root      = etree.Element(f"{{{NS_SVK}}}lonekorningar", nsmap=NSMAP_SVK)
    lk_lookup = {}

    for seq, row in enumerate(rows, 1):
        lk_id = f"LK_{artal}_{seq:06d}"
        pnr   = clean_pnr(row["personnummer"])
        nr    = row["anstallningsnummer"].strip()
        lkn   = row["lonekorningsnummer"].strip()
        lk_lookup[(pnr, nr, lkn)] = lk_id

        lk = sub(root, f"{{{NS_SVK}}}lonekorning")
        sub(lk, f"{{{NS_SVK}}}id", lk_id)
        sub(lk, f"{{{NS_SVK}}}lonekorningsnummer", lkn)
        if utb := strip_date(row["utbetalningsdatum"]):
            sub(lk, f"{{{NS_SVK}}}utbetalningsdatum", utb)
        ug = sub(lk, f"{{{NS_SVK}}}utbetalningsgruppReferens")
        sub(ug, f"{{{NS_SVK}}}id", row["utbetalningsgrupp_id"].strip())
        ar = sub(lk, f"{{{NS_SVK}}}anstallningReferens")
        sub(ar, f"{{{NS_SVK}}}anstallningsnummer", nr)
        sub(ar, f"{{{NS_SVK}}}personnummer", pnr)
        if lonespec := nonempty(row.get("lonespec", "")):
            sub(lk, f"{{{NS_SVK}}}lonespecifikation",
                href=lonespec.replace("\\", "/"))

    return root, lk_lookup


# ── Lönetransaktioner ─────────────────────────────────────────────────────────

def build_lonetransaktioner(rows: list, artal: str,
                            lk_lookup: dict) -> tuple[etree._Element, dict]:
    """Returnerar (root, lt_lookup) där lt_lookup: (pnr, nr, lkn, t_id) -> LT_id."""
    root      = etree.Element(f"{{{NS_SVK}}}lonetransaktioner", nsmap=NSMAP_SVK)
    lt_lookup = {}

    for seq, row in enumerate(rows, 1):
        lt_id = f"LT_{artal}_{seq:06d}"
        pnr   = clean_pnr(row["personnummer"])
        nr    = row["anstallningsnummer"].strip()
        lkn   = row["lonekorningsnummer"].strip()
        t_id  = row["transaktion_id"].strip()
        lt_lookup[(pnr, nr, lkn, t_id)] = lt_id

        lt = sub(root, f"{{{NS_SVK}}}lonetransaktion")
        sub(lt, f"{{{NS_SVK}}}id",              lt_id)
        sub(lt, f"{{{NS_SVK}}}transaktionId",   t_id)
        sub(lt, f"{{{NS_SVK}}}lonekorningReferens",
            lk_lookup.get((pnr, nr, lkn), ""))
        sub(lt, f"{{{NS_SVK}}}personalkategori", row["personalkategori"].strip())

        loneart = sub(lt, f"{{{NS_SVK}}}loneart")
        sub(loneart, f"{{{NS_SVK}}}kod",  row["loneart_kod"].strip())
        sub(loneart, f"{{{NS_SVK}}}namn", row["loneart_namn"].strip())

        d_start = strip_date(row.get("datumstart", ""))
        d_slut  = strip_date(row.get("datumslut", ""))
        if d_start or d_slut:
            period = sub(lt, f"{{{NS_SVK}}}period")
            if d_start:
                sub(period, f"{{{NS_SVK}}}startdatum", d_start)
            if d_slut:
                sub(period, f"{{{NS_SVK}}}slutdatum", d_slut)

        if v := nonempty(row.get("omfattning_procent", "")):
            if v not in ("0", "0.0"):
                sub(lt, f"{{{NS_SVK}}}omfattningProcent", v)

        antal = nonempty(row.get("antal", ""))
        apris = nonempty(row.get("apris", ""))
        if antal and apris:
            try:
                if float(antal) != 0 or float(apris) != 0:
                    kv = sub(lt, f"{{{NS_SVK}}}kvantitet")
                    sub(kv, f"{{{NS_SVK}}}antal", antal)
                    if enhet := nonempty(row.get("enhet", "")):
                        sub(kv, f"{{{NS_SVK}}}enhet", enhet)
                    sub(kv, f"{{{NS_SVK}}}aPris", apris)
            except ValueError:
                pass

        sub(lt, f"{{{NS_SVK}}}belopp", row["belopp_sek"].strip())
        sub(lt, f"{{{NS_SVK}}}valuta", "SEK")

        if kommentar := nonempty(row.get("transaktionsrad_text", "")):
            sub(lt, f"{{{NS_SVK}}}kommentar", kommentar)

    return root, lt_lookup


# ── Konteringar ───────────────────────────────────────────────────────────────

def build_konteringar(rows: list, artal: str, lt_lookup: dict) -> etree._Element:
    root = etree.Element(f"{{{NS_SVK}}}konteringar", nsmap=NSMAP_SVK)

    for seq, row in enumerate(rows, 1):
        pnr  = clean_pnr(row["personnummer"])
        nr   = row["anstallningsnummer"].strip()
        lkn  = row["lonekorningsnummer"].strip()
        t_id = row["transaktion_id"].strip()
        dims = extract_dimensions(row)

        k = sub(root, f"{{{NS_SVK}}}kontering")
        sub(k, f"{{{NS_SVK}}}id",            f"K_{artal}_{seq:06d}")
        sub(k, f"{{{NS_SVK}}}fordelningId",  row["fordelning_id"].strip())
        sub(k, f"{{{NS_SVK}}}lonetransaktionReferens",
            lt_lookup.get((pnr, nr, lkn, t_id), ""))
        sub(k, f"{{{NS_SVK}}}procentfordelning", row["procentfordelning"].strip())

        dims_el = sub(k, f"{{{NS_SVK}}}dimensioner")
        for n, v in dims:
            dim = sub(dims_el, f"{{{NS_SVK}}}dimension")
            sub(dim, f"{{{NS_SVK}}}namn", n)
            sub(dim, f"{{{NS_SVK}}}varde", v)

    return root


# ── Register ──────────────────────────────────────────────────────────────────

def build_utbetalningsgrupper(anstallningar: list) -> etree._Element:
    root = etree.Element(f"{{{NS_SVK}}}utbetalningsgrupper", nsmap=NSMAP_SVK)
    seen: dict[str, str] = {}
    for a in anstallningar:
        ug_id   = a["utbetalningsgrupp_id"].strip()
        ug_namn = a.get("utbetalningsgrupp_namn", "").strip()
        if ug_id not in seen:
            seen[ug_id] = ug_namn
    for ug_id, ug_namn in sorted(seen.items()):
        ug = sub(root, f"{{{NS_SVK}}}utbetalningsgrupp")
        sub(ug, f"{{{NS_SVK}}}id",   ug_id)
        sub(ug, f"{{{NS_SVK}}}namn", ug_namn)
    return root


def build_lonearter(rows: list) -> etree._Element:
    root = etree.Element(f"{{{NS_SVK}}}lonearter", nsmap=NSMAP_SVK)
    for row in rows:
        la = sub(root, f"{{{NS_SVK}}}loneart")
        sub(la, f"{{{NS_SVK}}}kod", row["loneart_kod"].strip())
        if pk := nonempty(row.get("personalkategori", "")):
            sub(la, f"{{{NS_SVK}}}personalkategori", pk)
        sub(la, f"{{{NS_SVK}}}namn", row["loneart_namn"].strip())
        if formel := nonempty(row.get("loneart_formel", "")):
            f_el = sub(la, f"{{{NS_SVK}}}formel", syntax="Flex")
            f_el.text = etree.CDATA(formel)
        sub(la, f"{{{NS_SVK}}}underlagstypSkatt", row["underlagstyp_skatt"].strip())
        konto    = nonempty(row.get("loneart_konto", ""))
        motkonto = nonempty(row.get("loneart_motkonto", ""))
        if konto:
            kt = sub(la, f"{{{NS_SVK}}}kontering")
            sub(kt, f"{{{NS_SVK}}}konto", konto)
            if motkonto:
                sub(kt, f"{{{NS_SVK}}}motkonto", motkonto)

        ej_soc    = nonempty(row.get("ej_underlag_soc_avg", ""))
        kostn_sov = nonempty(row.get("kostnadsavdrag_sov_avg", ""))
        kostn_pct = nonempty(row.get("kostnadsavdrag_soc_avg_procent", ""))
        fora      = nonempty(row.get("fora", ""))
        kap_kl    = nonempty(row.get("kap_kl", ""))
        has_props = any([
            fora    and fora.lower()    == "true",
            kap_kl  and kap_kl.lower()  == "true",
            ej_soc  and ej_soc.lower()  == "true",
            kostn_sov,
        ])
        if has_props:
            eg = sub(la, f"{{{NS_SVK}}}egenskaper")
            if fora   and fora.lower()   == "true":
                sub(eg, f"{{{NS_SVK}}}foraGrundande", "true")
            if kap_kl and kap_kl.lower() == "true":
                sub(eg, f"{{{NS_SVK}}}kapKlGrundande", "true")
            if ej_soc and ej_soc.lower() == "true":
                sub(eg, f"{{{NS_SVK}}}ejSocialavgiftsgrundande", "true")
            if kostn_sov:
                ka = sub(eg, f"{{{NS_SVK}}}kostnadsavdragSocAvg")
                if kostn_pct:
                    sub(ka, f"{{{NS_SVK}}}procent", kostn_pct)
    return root


def build_formelvariabler(rows: list) -> etree._Element:
    root = etree.Element(f"{{{NS_SVK}}}formelvariabler", nsmap=NSMAP_SVK)
    for row in rows:
        fv = sub(root, f"{{{NS_SVK}}}formelvariabel")
        sub(fv, f"{{{NS_SVK}}}namn",        row["variabelnamn"].strip())
        sub(fv, f"{{{NS_SVK}}}beskrivning", row["beskrivning"].strip())
    return root


# ── Paketgenerering ──────────────────────────────────────────────────────────

def paketera(csv_dir: str, output_dir: str | None = None) -> None:
    csv_path_in = Path(csv_dir)
    if not csv_path_in.is_dir():
        print(f"Fel: katalogen '{csv_path_in}' finns inte.", file=sys.stderr)
        sys.exit(1)

    prefix = csv_path_in.name

    def csv(suffix: str) -> Path:
        return csv_path_in / f"{prefix}_{suffix}.csv"

    print(f"Läser CSV-filer från {csv_path_in} ...")
    arbetsgivare  = read_csv(csv("arbetsgivare"))
    anstallningar = read_csv(csv("anstallningar"))
    anstperioder  = read_csv(csv("anstallningsperioder"))
    manadsloner   = read_csv(csv("manadsloner"))
    timloner      = read_csv(csv("timloner"))
    syssgrader    = read_csv(csv("sysselsattningsgrader"))
    heltidsmatt   = read_csv(csv("arbetsmatt_heltid"))
    lonetillagg   = read_csv(csv("lonetillagg"))
    kostnadsf     = read_csv(csv("kostnadsfordelningar"))
    hemkont       = read_csv(csv("hemkonteringar"))
    lonekorningar = read_csv(csv("lonekorningar"))
    lonetrans     = read_csv(csv("lonetransaktioner"))
    trans_kont    = read_csv(csv("lonetransaktion_konteringar"))
    lonearter     = read_csv(csv("lonearter"))
    formelvar     = read_csv(csv("formelvariabler"))

    if not arbetsgivare:
        print("Fel: arbetsgivare.csv är tom.", file=sys.stderr)
        sys.exit(1)

    ag            = arbetsgivare[0]
    artal         = ag["artal_slut"].strip()
    agency_name   = ag["organisationsnamn"].strip()
    creation_date = datetime.today().strftime("%Y-%m-%d")
    orgnr_clean   = ag["organisationsnummer"].strip().replace("-", "")
    org_record_id = f"ORG_{orgnr_clean}"

    out = Path(output_dir) if output_dir else Path(f"{csv_path_in}_paket")
    for d in ["organisation", "anstallningar", "arbetstagare", "personer",
              "loneutbetalningar", "register", "lonespecifikationer"]:
        (out / d).mkdir(parents=True, exist_ok=True)

    print(f"Genererar XML-paket i {out} ...")

    # Organisation
    write_xml(out / "organisation" / "organisation.xml",
              build_organisation(ag, agency_name, creation_date, org_record_id))
    print("  organisation/organisation.xml")

    # Indexera CSV-rader per anstallningsnummer
    def idx(rows: list) -> dict:
        d = defaultdict(list)
        for r in rows:
            d[r["anstallningsnummer"].strip()].append(r)
        return d

    ap_idx = idx(anstperioder)
    ml_idx = idx(manadsloner)
    tl_idx = idx(timloner)
    sg_idx = idx(syssgrader)
    hm_idx = idx(heltidsmatt)
    lt_idx = idx(lonetillagg)
    kf_idx = idx(kostnadsf)
    hk_idx = idx(hemkont)

    # Kontrollera att anstallningsnummer är unika (datakvalitet)
    seen_nr: set[str] = set()
    for anst in anstallningar:
        nr = anst["anstallningsnummer"].strip()
        if nr in seen_nr:
            print(f"  Varning: anstallningsnummer {nr} förekommer flera gånger i "
                  f"anstallningar.csv – senare rad skriver över F_{nr}.xml.",
                  file=sys.stderr)
        seen_nr.add(nr)

    # Anställningar + samla personuppgifter
    person_cache: dict[str, dict] = {}
    for anst in anstallningar:
        nr  = anst["anstallningsnummer"].strip()
        pnr = clean_pnr(anst["personnummer"])
        write_xml(
            out / "anstallningar" / f"F_{nr}.xml",
            build_anstallning(
                anst=anst,
                manadsloner=ml_idx[nr], timloner=tl_idx[nr],
                anstperioder=ap_idx[nr], syssgrader=sg_idx[nr],
                heltidsmatt=hm_idx[nr], lonetillagg=lt_idx[nr],
                kostnadsfordelningar=kf_idx[nr], hemkonteringar=hk_idx[nr],
                agency_name=agency_name, creation_date=creation_date,
                org_record_id=org_record_id,
            ),
        )
        print(f"  anstallningar/F_{nr}.xml")
        if pnr and pnr not in person_cache:
            person_cache[pnr] = {
                "fornamn":    anst.get("fornamn", "").strip(),
                "efternamn":  anst.get("efternamn", "").strip(),
                "nationalitet": anst.get("nationalitet", "").strip(),
                "skyddad":    anst.get("skyddad", "").strip().lower() in ("true", "1", "ja"),
            }
        elif not pnr:
            print(f"  Varning: F_{nr} saknar personnummer – P_/A_-filer skapas ej.")

    # Person + Arbetstagare
    for pnr, info in person_cache.items():
        pnr_id = pnr_to_id(pnr)
        write_xml(out / "personer"     / f"P_{pnr_id}.xml",
                  build_person(pnr, info["fornamn"], info["efternamn"],
                               info["nationalitet"], info["skyddad"],
                               agency_name, creation_date))
        print(f"  personer/P_{pnr_id}.xml")
        write_xml(out / "arbetstagare" / f"A_{pnr_id}.xml",
                  build_arbetstagare(pnr, info["fornamn"], info["efternamn"],
                                     agency_name, creation_date, org_record_id))
        print(f"  arbetstagare/A_{pnr_id}.xml")

    # Löneutbetalningar
    lk_root, lk_lookup = build_lonekorningar(lonekorningar, artal)
    write_xml(out / "loneutbetalningar" / "lonekorningar.xml", lk_root)
    print("  loneutbetalningar/lonekorningar.xml")

    lt_root, lt_lookup = build_lonetransaktioner(lonetrans, artal, lk_lookup)
    write_xml(out / "loneutbetalningar" / "lonetransaktioner.xml", lt_root)
    print("  loneutbetalningar/lonetransaktioner.xml")

    write_xml(out / "loneutbetalningar" / "konteringar.xml",
              build_konteringar(trans_kont, artal, lt_lookup))
    print("  loneutbetalningar/konteringar.xml")

    # Register
    write_xml(out / "register" / "utbetalningsgrupper.xml",
              build_utbetalningsgrupper(anstallningar))
    print("  register/utbetalningsgrupper.xml")

    write_xml(out / "register" / "lonearter.xml", build_lonearter(lonearter))
    print("  register/lonearter.xml")

    write_xml(out / "register" / "formelvariabler.xml",
              build_formelvariabler(formelvar))
    print("  register/formelvariabler.xml")

    # Lönespecifikationer
    spec_src = csv_path_in / "lonespecifikationer"
    spec_dst = out / "lonespecifikationer"
    if spec_src.is_dir():
        count = sum(
            1 for f in spec_src.iterdir()
            if f.is_file() and shutil.copy2(f, spec_dst / f.name) is not None or f.is_file()
        )
        print(f"  lonespecifikationer/ ({len(list(spec_src.iterdir()))} filer kopierade)")

    print(f"\nKlart! Paketet finns i: {out}")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    paketera(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
