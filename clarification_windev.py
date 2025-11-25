#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
clarification_windev.py
Full rewrite with all requested features:
- Bilingual cartouche (FR + EN)
- Steps 1..5 processing for .wdw files (internal_properties removal, properties flattening/preservation,
  p_codes processing, removal of events without code, mapping event types and control/column types)
- Anomaly analysis and logging into FR_*.log and EN_*.log with insertion at head (most recent first)
- Each .clair file is prefixed with header: source, processing times, anomalies count
- Preservation of code blocks and indentation rules
- Checks for optional dependency 'chardet' and clear instructions
- CLI with --dir and --lang options
- Robust error handling and bilingual messages
- Written to /mnt/data/clarification_windev.py by the assistant on request
"""

# -----------------------------------------------------------------------------
# Cartouche (FR and EN)
# -----------------------------------------------------------------------------
# [FR]
# Nom du script       : clarification_windev.py
# Créateur            : Christophe Charron (CCN)
# Assistant (IA)      : GPT-5 Thinking mini (assistant)
# Date de création    : 2025-11-14
#
# But :
#   Clarifier des fichiers texte WinDev (.wdw) représentant des fenêtres
#   pour produire des fichiers "clarifiés" utiles pour générer des squelettes Blazor.
#
# Fonctionnalités :
#   - Parcourt un répertoire et traite tous les fichiers *.wdw
#   - Conserve l'encodage d'origine
#   - Étape 1: suppression des internal_properties
#   - Étape 2: traitement des properties :
#       * si properties contient des sous-phrases simples (indentation attendue) -> aplatir en une ligne
#       * sinon (listes '-', blocs complexes) -> conserver intégralement le bloc
#   - Étape 3: traitement des p_codes (controls et window):
#       * détecte les événements ('-') ; supprime ceux sans code
#       * si événement contient du code (code : |1+ ou |1-), on annotera les 'type : N' événementiels
#         en utilisant correspondance_evenements.txt (fallback "(Type d’événement à préciser)")
#   - Étape 4: suppression des phrases vides exactes :
#       style : {}, controls : [], options : [], popup_menus : [], procedure_templates : [], property_templates : []
#   - Étape 5: mapping des types des controls et des columns :
#       * pour chaque 'name' ayant un 'identifier' sibling au même niveau, on cherche un sibling 'type'
#         au même indent ; si trouvé, on remplace "type : N" par "type : N (Libellé)"
#       * mapping dans correspondance_controls.txt ; fallback "(Control inconnu)"
#   - Analyse des anomalies (types non mappés) : écrit dans les journaux FR_... et EN_...
#   - Chaque .clair commence par entête (source, date FR, date EN, nb anomalies)
#
# Journaux :
#   - FR_clarification_windev.log et EN_clarification_windev.log
#   - Les nouvelles lignes sont ajoutées en tête du fichier (nouveautés antéchronologiques)
#   - Les anomalies consignées avec numéros de ligne 1-based et parent + name si disponibles
#
# Exemple PowerShell :
#   python .\clarification_windev.py --dir "D:\WDW" --lang fr
#
# -----------------------------------------------------------------------------
# [EN]
# Script name         : clarification_windev.py
# Creator             : Christophe Charron (CCN)
# Assistant (AI)      : GPT-5 Thinking mini (assistant)
# Creation date       : 2025-11-14
#
# Purpose:
#   Clarify WinDev .wdw text files representing windows to produce "clarified"
#   files suitable to bootstrap Blazor windows. Preserves source file encoding.
#
# Features:
#   - Walk a directory and process all .wdw files
#   - Preserve file encoding
#   - Step 1: remove internal_properties
#   - Step 2: handle properties:
#       * flatten simple phrase children into one comma-separated line
#       * otherwise preserve the full properties block (lists, nested structures, code)
#   - Step 3: process p_codes (under controls and window):
#       * events marked by '-' ; drop events without code
#       * annotate event-level 'type : N' using correspondance_evenements.txt
#   - Step 4: delete exact empty phrases: style : {}, controls : [], options : [], popup_menus : [], procedure_templates : [], property_templates : []
#   - Step 5: map control and column types by matching sibling 'type' at same indentation as 'name' and 'identifier'
#   - Anomaly analysis and bilingual logs, .clair header with counts
#
# Logs:
#   - FR_clarification_windev.log and EN_clarification_windev.log
#   - New entries are written at the top of the files (most recent first)
#   - Anomalies include 1-based line numbers and parent info
#
# PowerShell example :
#   python clarification_windev.py --dir "/path/to/wdws" --lang en
#
# -----------------------------------------------------------------------------

from __future__ import annotations

import argparse
import os
import re
import sys
import traceback
from typing import List, Tuple, Optional, Dict

# Optional dependency: chardet for encoding detection
try:
    import chardet  # type: ignore
    _HAS_CHARDET = True
except Exception:
    chardet = None  # type: ignore
    _HAS_CHARDET = False

SCRIPT_NAME = "clarification_windev.py"
FR_LOG = f"FR_{os.path.splitext(SCRIPT_NAME)[0]}.log"
EN_LOG = f"EN_{os.path.splitext(SCRIPT_NAME)[0]}.log"

DATE_FMT_FR = "%d/%m/%Y %H:%M:%S"
DATE_FMT_EN = "%Y-%m-%d %H:%M:%S"

PHRASE_RE = re.compile(r'^(\s*)([A-Za-z0-9_\-]+)\s*:\s*(.*)$')

# ----------------------------- Utilities: logging & time ---------------------

def _now_str(fr: bool) -> str:
    import datetime as _dt
    return _dt.datetime.now().strftime(DATE_FMT_FR if fr else DATE_FMT_EN)

def _prepend_line(filepath: str, line: str) -> None:
    """
    Prepend a line to a file (newest entries first). If prepend fails, append as fallback.
    """
    try:
        existing = ""
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                existing = f.read()
        with open(filepath, "w", encoding="utf-8", errors="replace") as f:
            f.write(line.rstrip("\n") + "\n")
            if existing:
                f.write(existing)
    except Exception:
        with open(filepath, "a", encoding="utf-8", errors="replace") as f:
            f.write(line.rstrip("\n") + "\n")

def log_event(fr_msg: str, en_msg: str, level: str = "INFO") -> None:
    ts_fr = _now_str(fr=True)
    ts_en = _now_str(fr=False)
    _prepend_line(FR_LOG, f"{ts_fr} [{level}] {fr_msg}")
    _prepend_line(EN_LOG, f"{ts_en} [{level}] {en_msg}")

def print_bilingual(fr: str, en: str, lang: str = "fr", level: str = "INFO") -> None:
    log_event(fr, en, level=level)
    # Print localized to chosen language only; caller passes lang param for that
    print(f"{'[EN]' if lang=='en' else '[FR]'} {en if lang=='en' else fr}")

# ----------------------------- Encoding helpers ------------------------------

def detect_encoding(path: str) -> str:
    if _HAS_CHARDET:
        try:
            with open(path, "rb") as f:
                raw = f.read()
            res = chardet.detect(raw)  # type: ignore
            enc = (res.get("encoding") or "utf-8").lower()
            if enc in ("ascii",):
                enc = "utf-8"
            return enc
        except Exception:
            return "utf-8"
    else:
        log_event(
            "chardet non disponible : encodage supposé UTF-8.",
            "chardet not available: assuming UTF-8 encoding.",
            level="WARNING",
        )
        return "utf-8"

def read_text(path: str, encoding: Optional[str] = None) -> str:
    enc = encoding or detect_encoding(path)
    with open(path, "r", encoding=enc, errors="replace") as f:
        return f.read()

def write_text(path: str, content: str, encoding: str = "utf-8") -> None:
    with open(path, "w", encoding=encoding, errors="strict") as f:
        f.write(content)

# ----------------------------- Parsing helpers --------------------------------

def parse_lines_to_phrases(lines: List[str]) -> List[Tuple[int, str, str]]:
    """
    Parse file lines into a list of phrases:
      (indent, key, value_text)
    where value_text preserves internal newlines belonging to that phrase.
    """
    phrases: List[Tuple[int, str, str]] = []
    current_key = None
    current_indent = 0
    current_val_lines: List[str] = []

    def flush():
        nonlocal phrases, current_key, current_indent, current_val_lines
        if current_key is not None:
            value = "\n".join(current_val_lines).rstrip("\n")
            phrases.append((current_indent, current_key, value))
        current_key = None
        current_indent = 0
        current_val_lines = []

    for line in lines:
        m = PHRASE_RE.match(line)
        if m:
            flush()
            indent_spaces = m.group(1)
            key = m.group(2)
            rest = m.group(3)
            current_key = key
            current_indent = len(indent_spaces)
            current_val_lines = [rest]
        else:
            if current_key is None:
                continue
            current_val_lines.append(line.rstrip("\n"))
    flush()
    return phrases

def rebuild_phrases_to_text(phrases: List[Tuple[int, str, str]]) -> str:
    out_lines: List[str] = []
    for indent, key, val in phrases:
        out_lines.append(f"{' ' * indent}{key} : {val.splitlines()[0] if val else ''}".rstrip())
        extra = val.splitlines()[1:] if val else []
        for e in extra:
            out_lines.append(e.rstrip())
    return "\n".join(out_lines) + "\n"

# ----------------------------- Step 1,2,4: cleanup ---------------------------

def rebuild_step12_and_cleanup(phrases: List[Tuple[int, str, str]]) -> str:
    """
    Combine Steps:
     - Step 1: remove internal_properties
     - Step 2: process properties (flatten or preserve)
     - Step 4: remove exact empty phrases
    """
    out_lines: List[str] = []
    i = 0
    n = len(phrases)
    while i < n:
        indent, key, value = phrases[i]
        low = key.lower().strip()

        # Step 1: remove internal_properties entirely
        if low == "internal_properties":
            i += 1
            continue

        # Step 4: remove exact empty phrases
        if (low == "style" and value.strip() == "{}") or \
           (low in ("controls", "options", "popup_menus", "procedure_templates", "property_templates") and value.strip() == "[]"):
            i += 1
            continue

        # Step 2: handle properties blocks
        if low == "properties":
            props_indent = indent
            expected_child_indent = props_indent + 1
            j = i + 1
            subparts: List[str] = []
            found_simple_children = False

            # Scan children while deeper than properties indent
            while j < n:
                ind_j, key_j, val_j = phrases[j]
                if ind_j == expected_child_indent:
                    # Treat as simple phrase child to be flattened
                    found_simple_children = True
                    one_line = " ".join([s.strip() for s in val_j.splitlines() if s.strip()])
                    subparts.append(f"{key_j} : {one_line}".strip())
                    j += 1
                elif ind_j <= props_indent:
                    break
                else:
                    # child deeper than expected - not simple phrase child (could be '-' lists, nested blocks)
                    j += 1

            if found_simple_children and subparts:
                out_lines.append(f"{' ' * props_indent}properties : {', '.join(subparts)}".rstrip())
                i = j
                continue
            else:
                # No simple phrase children => preserve full original properties block as-is.
                # The original phrase value may contain subsequent lines already included in 'value'.
                out_lines.append(f"{' ' * indent}properties : {value.splitlines()[0] if value else ''}".rstrip())
                extra = value.splitlines()[1:] if value else []
                for e in extra:
                    out_lines.append(e.rstrip())
                i += 1
                continue

        # Default case: retain phrase and its internal lines
        out_lines.append(f"{' ' * indent}{key} : {value.splitlines()[0] if value else ''}".rstrip())
        extra = value.splitlines()[1:] if value else []
        for e in extra:
            out_lines.append(e.rstrip())
        i += 1

    return "\n".join(out_lines) + "\n"

# ----------------------------- Step 3: p_codes processing --------------------

def load_event_mapping(mapping_file: str) -> Dict[int, str]:
    mapping: Dict[int, str] = {}
    if not os.path.exists(mapping_file):
        log_event(
            "Fichier de correspondance des événements introuvable : correspondance_evenements.txt (aucun libellé ajouté).",
            "Event mapping file not found: correspondance_evenements.txt (no labels added).",
            level="WARNING"
        )
        return mapping
    try:
        with open(mapping_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r'^\s*type\s*:\s*(\d+)\s*\((.*?)\)\s*$', line, re.IGNORECASE)
                if m:
                    mapping[int(m.group(1))] = m.group(2)
    except Exception as ex:
        log_event(f"Erreur lecture fichier correspondance_evenements: {ex}", f"Failed reading event mapping: {ex}", level="ERROR")
    return mapping

def process_p_codes_blocks(clarified_text: str, mapping: Dict[int, str]) -> str:
    """
    Process p_codes blocks:
     - identify p_codes : blocks
     - inside, identify '-' event entries and collect their lines
     - drop events that do not have code (code : |1+ or |1-)
     - annotate event-level 'type : N' (indent == ev_indent + 2) using mapping
     - preserve code content and any 'type :' inside code if indentation differs
    """
    lines = clarified_text.splitlines()
    out: List[str] = []
    i = 0

    def is_phrase_at_or_above(idx: int, p_indent: int) -> bool:
        if idx >= len(lines):
            return True
        mm = PHRASE_RE.match(lines[idx])
        if mm and len(mm.group(1)) <= p_indent:
            return True
        dm = re.match(r'^(\s*)-\s*$', lines[idx])
        if dm and len(dm.group(1)) <= p_indent:
            return True
        return False

    DEFAULT_LABEL = "Type d’événement à préciser"

    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s*)p_codes\s*:\s*$', line)
        if not m:
            out.append(line)
            i += 1
            continue

        # p_codes block start
        out.append(line)
        p_indent = len(m.group(1))
        i += 1

        # iterate until we find a phrase at or above p_indent (end of p_codes)
        while i < len(lines) and not is_phrase_at_or_above(i, p_indent):
            if re.match(r'^\s*$', lines[i]):
                out.append(lines[i]); i += 1; continue

            ev_start = re.match(r'^(\s*)-\s*$', lines[i])
            if not ev_start:
                out.append(lines[i]); i += 1; continue

            ev_indent = len(ev_start.group(1))
            if ev_indent <= p_indent:
                break

            # collect event lines
            ev_lines: List[str] = [lines[i]]
            i += 1
            while i < len(lines):
                # next event or end of p_codes
                if re.match(rf'^\s{{{ev_indent}}}-\s*$', lines[i]) or is_phrase_at_or_above(i, p_indent):
                    break
                ev_lines.append(lines[i]); i += 1

            # check for code presence in the event
            has_code = any(re.match(r'^\s*code\s*:\s*\|1[+-]\s*$', l) for l in ev_lines)
            if not has_code:
                # drop event entirely
                continue

            # annotate event-level 'type :' if present at indent ev_indent + 2
            mapped_ev: List[str] = []
            for el in ev_lines:
                mm = re.match(r'^(\s*)type\s*:\s*(\d+)\s*(.*)$', el)
                if mm:
                    indent_len = len(mm.group(1))
                    num = int(mm.group(2))
                    tail = mm.group(3).strip()
                    if indent_len == ev_indent + 2:
                        label = mapping.get(num, DEFAULT_LABEL)
                        el = f"{mm.group(1)}type : {num} ({label})" + (f" {tail}" if tail else "")
                mapped_ev.append(el)
            out.extend(mapped_ev)

    return "\n".join(out) + "\n"

# ----------------------------- Step 5: controls/columns mapping --------------

def load_controls_mapping(mapping_file: str) -> Dict[int, str]:
    mapping: Dict[int, str] = {}
    if not os.path.exists(mapping_file):
        log_event("Fichier de correspondance des contrôles introuvable : correspondance_controls.txt (aucun libellé ajouté).",
                  "Controls mapping file not found: correspondance_controls.txt (no labels added).", level="WARNING")
        return mapping
    try:
        with open(mapping_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r'^\s*type\s*:\s*(\d+)\s*\((.*?)\)\s*$', line, re.IGNORECASE)
                if m:
                    mapping[int(m.group(1))] = m.group(2)
    except Exception as ex:
        log_event(f"Erreur lecture fichier correspondance_controls: {ex}", f"Failed reading controls mapping: {ex}", level="ERROR")
    return mapping

def step5_map_control_types(text: str, controls_map: Dict[int, str]) -> str:
    """
    For each 'name' phrase (controls or columns), find sibling 'identifier' and 'type' at same indent
    within the same block (until a phrase with smaller indent). Replace 'type : N' by 'type : N (Label)'.
    If label unknown, append '(Control inconnu)'.
    """
    phrases = parse_lines_to_phrases(text.splitlines())
    new_phrases = list(phrases)
    n = len(phrases)
    for idx, (indent, key, val) in enumerate(phrases):
        if key == 'name':
            name_indent = indent
            # find parent key (nearest previous phrase with indent < name_indent)
            parent_key = None
            for p in range(idx - 1, -1, -1):
                if phrases[p][0] < name_indent:
                    parent_key = phrases[p][1]
                    break
            # determine block range until we find a phrase with smaller indent
            j = idx + 1
            end = n
            while j < n:
                if phrases[j][0] < name_indent:
                    end = j
                    break
                j += 1
            # find identifier sibling at same indent
            has_identifier = any((phrases[k][1] == 'identifier' and phrases[k][0] == name_indent) for k in range(idx + 1, end))
            if not has_identifier:
                continue
            # find 'type' sibling at same indent and map it
            for k in range(idx + 1, end):
                ind_k, key_k, val_k = phrases[k]
                if key_k == 'type' and ind_k == name_indent:
                    first_line = val_k.splitlines()[0].strip()
                    m = re.match(r'^(\d+)', first_line)
                    if m:
                        num = int(m.group(1))
                        label = controls_map.get(num)
                        if label is None:
                            label = "Control inconnu"
                        tail = first_line[len(m.group(1)):].strip()
                        new_val = f"{num} ({label})" + (f" {tail}" if tail else "")
                        rest = "\n".join(val_k.splitlines()[1:])
                        if rest:
                            new_val = new_val + "\n" + rest
                        new_phrases[k] = (phrases[k][0], phrases[k][1], new_val)
                    break
    return rebuild_phrases_to_text(new_phrases)

# ----------------------------- Anomaly detection helpers ----------------------

def find_phrases_with_lineno(text: str) -> List[Tuple[int, str, str, int]]:
    """
    Return list of tuples (indent, key, value, start_line_index) where start_line_index is 0-based.
    """
    lines = text.splitlines()
    phrases = []
    current_key = None
    current_indent = 0
    current_val_lines = []
    current_start = 0
    for idx, line in enumerate(lines):
        m = PHRASE_RE.match(line)
        if m:
            if current_key is not None:
                phrases.append((current_indent, current_key, "\n".join(current_val_lines).rstrip("\n"), current_start))
            current_indent = len(m.group(1))
            current_key = m.group(2)
            current_val_lines = [m.group(3)]
            current_start = idx
        else:
            if current_key is not None:
                current_val_lines.append(line.rstrip("\n"))
    if current_key is not None:
        phrases.append((current_indent, current_key, "\n".join(current_val_lines).rstrip("\n"), current_start))
    return phrases

def analyze_anomalies_in_source(src_text: str, events_map: Dict[int, str], controls_map: Dict[int, str]):
    """
    Identify anomalies (types not found in mappings) in source file.
    Returns list of dicts with keys:
      kind: 'control' or 'event'
      type_num: int
      type_line: 0-based line index for the type phrase start
      parent_line: 0-based line index for parent (name or p_codes) start
      parent_name: optional parent name value
    """
    anomalies = []
    lines = src_text.splitlines()
    phrases = find_phrases_with_lineno(src_text)

    # Controls/columns: look for name siblings and type siblings at same indent
    for i, (indent, key, val, start_line) in enumerate(phrases):
        if key == 'name':
            name_indent = indent
            # find parent key just for context
            parent_key = None
            for p in range(i - 1, -1, -1):
                if phrases[p][0] < name_indent:
                    parent_key = phrases[p][1]
                    break
            # range of block until indent less than name_indent
            j = i + 1
            end = len(phrases)
            while j < len(phrases) and phrases[j][0] >= name_indent:
                j += 1
            # require identifier sibling
            has_identifier = any((phrases[k][1] == 'identifier' and phrases[k][0] == name_indent) for k in range(i+1, end))
            if not has_identifier:
                continue
            # find type sibling
            for k in range(i+1, end):
                ind_k, key_k, val_k, start_k = phrases[k]
                if key_k == 'type' and ind_k == name_indent:
                    m = re.match(r'^\s*(\d+)', val_k.splitlines()[0])
                    if m:
                        num = int(m.group(1))
                        if num not in controls_map:
                            anomalies.append({
                                'kind': 'control',
                                'type_num': num,
                                'type_line': start_k,
                                'parent_line': start_line,
                                'parent_name': val.strip() if val else None
                            })
                    break

    # Events: find p_codes blocks and event-level types
    for idx, line in enumerate(lines):
        m = re.match(r'^(\s*)p_codes\s*:\s*$', line)
        if not m:
            continue
        p_indent = len(m.group(1))
        i = idx + 1
        while i < len(lines):
            if re.match(r'^\s*$', lines[i]):
                i += 1; continue
            mm = PHRASE_RE.match(lines[i])
            if mm and len(mm.group(1)) <= p_indent:
                break
            ev_start = re.match(r'^(\s*)-\s*$', lines[i])
            if not ev_start:
                i += 1; continue
            ev_indent = len(ev_start.group(1))
            ev_lines = [(i, lines[i])]
            i += 1
            while i < len(lines):
                if re.match(rf'^\s{{{ev_indent}}}-\s*$', lines[i]):
                    break
                mm = PHRASE_RE.match(lines[i])
                if mm and len(mm.group(1)) <= p_indent:
                    break
                ev_lines.append((i, lines[i])); i += 1
            # check for code presence
            has_code = any(re.match(r'^\s*code\s*:\s*\|1[+-]\s*$', l) for (_, l) in ev_lines)
            if not has_code:
                continue
            for ln, l in ev_lines:
                mtype = re.match(r'^(\s*)type\s*:\s*(\d+)\s*(.*)$', l)
                if mtype:
                    indent_len = len(mtype.group(1))
                    if indent_len == ev_indent + 2:
                        num = int(mtype.group(2))
                        if num not in events_map:
                            anomalies.append({
                                'kind': 'event',
                                'type_num': num,
                                'type_line': ln,
                                'parent_line': idx,
                                'parent_name': None
                            })
    return anomalies

# ----------------------------- File processing pipeline ----------------------

def process_file(src: str, events_map: Dict[int, str], controls_map: Dict[int, str], lang: str = "fr") -> Tuple[bool, Optional[str]]:
    """
    Process a single .wdw file and write the clarified file in the clarifications folder.
    Adds header to the output and logs anomalies.
    """
    try:
        enc = detect_encoding(src)
        src_text = read_text(src, encoding=enc)

        # analyze anomalies on original source (to get correct line numbers)
        anomalies = analyze_anomalies_in_source(src_text, events_map, controls_map)

        # steps 1,2,4 cleanup
        phrases = parse_lines_to_phrases(src_text.splitlines())
        clarified_step12 = rebuild_step12_and_cleanup(phrases)

        # step 3: p_codes processing
        clarified_step3 = process_p_codes_blocks(clarified_step12, events_map)

        # step 5: map control/column types
        clarified_step5 = step5_map_control_types(clarified_step3, controls_map)

        # header for .clair
        now_fr = _now_str(fr=True)
        now_en = _now_str(fr=False)
        header_lines = [
            f"# Source: {os.path.basename(src)}",
            f"# Traitement (FR): {now_fr}",
            f"# Processing (EN): {now_en}",
            f"# Anomalies détectées: {len(anomalies)}",
            ""
        ]
        clarified_with_header = "\n".join(header_lines) + clarified_step5

        # write clarified file with same encoding as source
        base, _ = os.path.splitext(os.path.basename(src))
        out_dir = os.path.join(os.path.dirname(src), "clarifications")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{base}_wdw.clair")
        write_text(out_path, clarified_with_header, encoding=enc)

        # log anomalies
        for a in anomalies:
            if a['kind'] == 'control':
                fr_msg = f"Anomalie contrôle: type {a['type_num']} non trouvé. Ligne type: {a['type_line']+1}, ligne parent (name): {a['parent_line']+1}, name: {a.get('parent_name')}"
                en_msg = f"Control anomaly: type {a['type_num']} not found. Type line: {a['type_line']+1}, parent line (name): {a['parent_line']+1}, name: {a.get('parent_name')}"
                log_event(fr_msg, en_msg, level="WARNING")
            else:
                fr_msg = f"Anomalie événement: type {a['type_num']} non trouvé. Ligne type: {a['type_line']+1}, ligne parent (p_codes): {a['parent_line']+1}"
                en_msg = f"Event anomaly: type {a['type_num']} not found. Type line: {a['type_line']+1}, parent line (p_codes): {a['parent_line']+1}"
                log_event(fr_msg, en_msg, level="WARNING")

        print_bilingual(f"Fichier traité : {os.path.basename(src)} -> clarifications\\{base}_wdw.clair (encodage: {enc})",
                        f"Processed file: {os.path.basename(src)} -> clarifications\\{base}_wdw.clair (encoding: {enc})",
                        lang=lang, level="INFO")

        return True, None
    except Exception as ex:
        tb = traceback.format_exc()
        print_bilingual(f"Erreur lors du traitement de '{os.path.basename(src)}' : {ex}",
                        f"Error while processing '{os.path.basename(src)}' : {ex}",
                        lang=lang, level="ERROR")
        log_event(f"Traceback (FR) pour '{src}':\n{tb}", f"Traceback (EN) for '{src}':\n{tb}", level="ERROR")
        return False, str(ex)

def process_directory(dir_path: str, lang: str = "fr") -> int:
    if not os.path.isdir(dir_path):
        raise Exception(f"Le répertoire spécifié n'existe pas : {dir_path} / The specified directory does not exist: {dir_path}")

    root = os.path.dirname(os.path.abspath(__file__))
    mapping_events = os.path.join(root, "correspondance_evenements.txt")
    mapping_controls = os.path.join(root, "correspondance_controls.txt")

    events_map = load_event_mapping(mapping_events)
    controls_map = load_controls_mapping(mapping_controls)

    total = 0
    for name in os.listdir(dir_path):
        if not name.lower().endswith(".wdw"):
            continue
        src = os.path.join(dir_path, name)
        if not os.path.isfile(src):
            continue
        success, error = process_file(src, events_map, controls_map, lang=lang)
        if success:
            total += 1
    return total

# ----------------------------- CLI & argument parsing -----------------------

def check_dependencies(lang: str = "fr") -> None:
    if not _HAS_CHARDET:
        print_bilingual(
            "Dépendance optionnelle manquante: 'chardet' (détection d'encodage). Le script utilisera UTF-8 par défaut. Pour l'installer : python -m pip install chardet",
            "Optional dependency missing: 'chardet' (encoding detection). The script will default to UTF-8. To install: python -m pip install chardet",
            lang=lang, level="WARNING"
        )

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Clarify WinDev .wdw files and produce clarified outputs.")
    p.add_argument("--dir", required=True, help="Directory containing .wdw files")
    p.add_argument("--lang", choices=["fr", "en"], default="fr", help="Message language (fr/en)")
    p.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Log level")
    return p.parse_args(argv)

def main(argv: List[str]) -> int:
    start_fr = _now_str(fr=True)
    start_en = _now_str(fr=False)
    cmdline = " ".join([sys.executable] + [os.path.abspath(__file__)] + argv)
    _prepend_line(FR_LOG, f"{start_fr} [START] Commande : {cmdline}")
    _prepend_line(EN_LOG, f"{start_en} [START] Command : {cmdline}")

    try:
        args = parse_args(argv)
        lang = args.lang

        print_bilingual(f"Niveau de journalisation : {args.log_level}", f"Log level: {args.log_level}", lang=lang, level=args.log_level)

        if not args.dir:
            raise Exception("Paramètre --dir manquant. / Missing --dir")

        check_dependencies(lang=lang)

        print_bilingual(f"Début du traitement du répertoire : {args.dir}", f"Starting processing of directory: {args.dir}", lang=lang, level="INFO")
        count = process_directory(args.dir, lang=lang)

        print_bilingual(f"Terminé. Fichiers .wdw traités avec succès : {count}", f"Done. Successfully processed .wdw files: {count}", lang=lang, level="INFO")
        return 0
    except Exception as ex:
        tb = traceback.format_exc()
        print_bilingual(f"Erreur inattendue : {ex}", f"Unexpected error: {ex}", lang="fr", level="ERROR")
        log_event(f"Traceback (FR):\n{tb}", f"Traceback (EN):\n{tb}", level="ERROR")
        return 3
    finally:
        end_fr = _now_str(fr=True)
        end_en = _now_str(fr=False)
        _prepend_line(FR_LOG, f"{end_fr} [END] Fin d'exécution.")
        _prepend_line(EN_LOG, f"{end_en} [END] Execution finished.")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
