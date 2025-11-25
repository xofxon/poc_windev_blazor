#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FR :
Script : creation_de_squelette_balzor_a_partir_de_fenetre_windev.py
Créateur : <Christophe Charron>
Assistant : GPT (IA)
Date de création : 2025-11-18
Dépendances Python :
    - Aucun package externe requis pour l'exécution de base.
    - (Optionnel) pour écrire ODS : odfpy
Procédure d'installation (si nécessaire) :
    pip install odfpy
Consigne de création :
    - Générer des squelettes Blazor (.razor + .razor.cs) à partir des fichiers clarifiés
      Windev situés dans le sous-répertoire "clarifications".
Modificateur(s) : <à renseigner>
Date(s) de modification :
    - 2025-11-18 : Extraction précise des procédures, filtrage noms contrôles / procédures, préservation properties.
    - 2025-11-19 : Ajout du traitement des codes strictement rattachés à la fenêtre (p_codes au niveau fenêtre).
Modifications apportées :
    - Les blocs p_codes situés au même niveau que 'procedures :' sont maintenant extraits
      et générés en tant que méthodes séparées dans le .razor.cs.
    - Les commentaires contiennent le code WLang original (toujours).
    - Traduction heuristique en C# placée dans le corps de la méthode (préfixe // TODO translate:).
Exemples de lancement (PowerShell) :
    python .\\creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "C:\\Mes Projets\\Mon_Projet_texte" --lang fr
    python .\\creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "C:\\Mes Projets\\Mon_Projet_texte" --lang en
Exemples de lancement (Docker) :
    docker run --rm -v C:\\MesProjets\\Mon_Projet_texte:/data python:3.11 python /path/to/creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "/data" --lang fr

EN:
Script: creation_de_squelette_balzor_a_partir_de_fenetre_windev.py
Author: <Christophe Charron>
Assistant: GPT (AI)
Creation date: 2025-11-18
Python dependencies:
    - None required for base execution.
    - (Optional) to write ODS: odfpy
Install instructions:
    pip install odfpy
Design requirement:
    - Generate Blazor skeletons (.razor + .razor.cs) from the clarified Windev files
      located in a "clarifications" subfolder.
Modifier(s): <to fill>
Modification dates:
    - 2025-11-18: Fixed procedure extraction, preserved properties, filter control names as procedures.
    - 2025-11-19: Added handling of window-attached code blocks (p_codes at window level).
Changes:
    - Window-attached p_codes are now extracted into separate methods.
    - Comments always contain the original WLang code.
    - Heuristic C# translation placed in method bodies as TODOs.
Command-line examples (Powershell):
    python .\\creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "C:\\MyProjects\\MyTextProject" --lang en
Docker examples:
    docker run --rm -v C:\\MyProjects\\MyTextProject:/data python:3.11 python /path/to/creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "/data" --lang en
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import traceback
from typing import List, Dict, Optional, Tuple

# ---------------- Configuration ----------------
SCRIPT_NAME = "creation_de_squelette_balzor_a_partir_de_fenetre_windev.py"
FR_LOG = f"FR_{os.path.splitext(SCRIPT_NAME)[0]}.log"
EN_LOG = f"EN_{os.path.splitext(SCRIPT_NAME)[0]}.log"
DATE_FMT_FR = "%d/%m/%Y %H:%M:%S"
DATE_FMT_EN = "%Y-%m-%d %H:%M:%S"
EVENTS_MAPPING_FILE = "correspondance_evenements.txt"
CONTROLS_MAPPING_FILE = "correspondance_controls.txt"

# phrase matcher: indent + key : content
PHRASE_RE = re.compile(r'^(\s*)([A-Za-z0-9_\-]+)\s*:\s*(.*)$')

# defaults for mapping
DEFAULT_CONTROL_TO_BLAZOR = {
    2: "InputText", 3: "label", 4: "button", 5: "input[type=checkbox]",
    6: "select", 7: "select", 9: "table", 10: "progress", 14: "select",
    16: "tabs", 30: "repeater", 40: "div",
}

EVENT_TYPE_VERB = {15: "focus", 16: "blur", 17: "input", 18: "click", 14: "init"}

# ---------------- Utilities ----------------
def _now_str(fr: bool) -> str:
    import datetime as _dt
    return _dt.datetime.now().strftime(DATE_FMT_FR if fr else DATE_FMT_EN)

def _prepend_line(filepath: str, line: str) -> None:
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
    _prepend_line(FR_LOG, f"{_now_str(True)} [{level}] {fr_msg}")
    _prepend_line(EN_LOG, f"{_now_str(False)} [{level}] {en_msg}")

def print_bilingual(fr_msg: str, en_msg: str, lang: str = "fr") -> None:
    log_event(fr_msg, en_msg, "INFO")
    print(fr_msg if lang == "fr" else en_msg)

# ---------------- Load mappings ----------------
def load_events_mapping(script_dir: str) -> Dict[int, str]:
    mapping: Dict[int, str] = {}
    path = os.path.join(script_dir, EVENTS_MAPPING_FILE)
    if not os.path.exists(path):
        log_event("Fichier correspondance_evenements introuvable.", "Events mapping file not found.", "WARNING")
        return mapping
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                r = line.strip()
                if not r or r.startswith("#"):
                    continue
                m = re.match(r'^\s*type\s*:\s*(\d+)\s*\((.*?)\)\s*$', r, re.IGNORECASE)
                if m:
                    mapping[int(m.group(1))] = m.group(2).strip()
    except Exception as e:
        log_event(f"Erreur lecture mapping événements: {e}", f"Events mapping read error: {e}", "ERROR")
    return mapping

def load_controls_mapping(script_dir: str) -> Dict[int, str]:
    mapping: Dict[int, str] = {}
    path = os.path.join(script_dir, CONTROLS_MAPPING_FILE)
    if not os.path.exists(path):
        log_event("Fichier correspondance_controls introuvable; fallback.", "Controls mapping not found; fallback.", "WARNING")
        return mapping
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                m = re.match(r'^\s*type\s*[:\s]?\s*(\d+)\s*\((.*?)\)\s*$', raw, re.IGNORECASE)
                if m:
                    mapping[int(m.group(1))] = m.group(2).strip()
    except Exception as e:
        log_event(f"Erreur lecture mapping controls: {e}", f"Controls mapping read error: {e}", "ERROR")
    return mapping

# ---------------- Parsing helpers ----------------
def parse_phrases_from_block(block_lines: List[str], start_line_no:int):
    phrases = []
    cur_key = None
    cur_indent = 0
    cur_lines = []
    cur_start = start_line_no
    for idx, line in enumerate(block_lines):
        m = PHRASE_RE.match(line)
        if m:
            if cur_key is not None:
                phrases.append((cur_indent, cur_key, "\n".join(cur_lines).rstrip("\n"), cur_start))
            cur_indent = len(m.group(1))
            cur_key = m.group(2)
            cur_lines = [m.group(3)]
            cur_start = start_line_no + idx
        else:
            if cur_key is not None:
                cur_lines.append(line.rstrip("\n"))
    if cur_key is not None:
        phrases.append((cur_indent, cur_key, "\n".join(cur_lines).rstrip("\n"), cur_start))
    return phrases

def find_section_bounds(lines: List[str], section_name: str) -> Tuple[Optional[int], Optional[int]]:
    n = len(lines)
    for i, l in enumerate(lines):
        m = re.match(r'^\s*' + re.escape(section_name) + r'\s*:\s*$', l)
        if m:
            sec_indent = len(m.group(0)) - len(m.group(0).lstrip())
            j = i + 1
            while j < n:
                mm = PHRASE_RE.match(lines[j])
                if mm and len(mm.group(1)) <= sec_indent:
                    break
                j += 1
            return i, j
    return None, None

def collect_blocks_from_text(text: str) -> dict:
    """
    Collect controls, columns and procedure candidates.
    """
    lines = text.splitlines()
    n = len(lines)
    result = {"phrases_raw": lines, "controls": [], "columns": [], "procedures": []}

    # Controls
    start, end = find_section_bounds(lines, "controls")
    if start is not None:
        ctrl_lines = lines[start+1:end]
        i = 0
        while i < len(ctrl_lines):
            if re.match(r'^\s*$', ctrl_lines[i]):
                i += 1
                continue
            m_dash = re.match(r'^(\s*)-\s*$', ctrl_lines[i])
            if m_dash:
                dash_indent = len(m_dash.group(1))
                j = i + 1
                block = []
                while j < len(ctrl_lines):
                    m_next = re.match(r'^(\s*)-\s*$', ctrl_lines[j])
                    if m_next and len(m_next.group(1)) == dash_indent:
                        break
                    block.append(ctrl_lines[j])
                    j += 1
                phrases = parse_phrases_from_block(block, start+1+i+1)
                ctrl = {"raw_lines": block, "phrases": phrases, "phrases_map": {}}
                for (ind, key, val, ln) in phrases:
                    if key == "name" and "name" not in ctrl:
                        ctrl["name"] = val.splitlines()[0].strip()
                    if key == "identifier" and "identifier" not in ctrl:
                        ctrl["identifier"] = val.splitlines()[0].strip()
                    if key == "type" and "type" not in ctrl:
                        ctrl["type"] = val.splitlines()[0].strip()
                    if key == "properties" and "properties" not in ctrl:
                        ctrl["properties"] = val
                    ctrl["phrases_map"][key] = val
                result["controls"].append(ctrl)
                i = j
            else:
                m_name = PHRASE_RE.match(ctrl_lines[i])
                if m_name:
                    b_indent = len(m_name.group(1))
                    j = i
                    block = []
                    while j < len(ctrl_lines):
                        mm = PHRASE_RE.match(ctrl_lines[j])
                        if mm and len(mm.group(1)) <= b_indent and j != i:
                            break
                        if re.match(r'^(\s*)-\s*$', ctrl_lines[j]) and len(re.match(r'^(\s*)-\s*$', ctrl_lines[j]).group(1)) <= b_indent:
                            break
                        block.append(ctrl_lines[j])
                        j += 1
                    phrases = parse_phrases_from_block(block, start+1+i)
                    ctrl = {"raw_lines": block, "phrases": phrases, "phrases_map": {}}
                    for (ind, key, val, ln) in phrases:
                        if key == "name" and "name" not in ctrl:
                            ctrl["name"] = val.splitlines()[0].strip()
                        if key == "identifier" and "identifier" not in ctrl:
                            ctrl["identifier"] = val.splitlines()[0].strip()
                        if key == "type" and "type" not in ctrl:
                            ctrl["type"] = val.splitlines()[0].strip()
                        if key == "properties" and "properties" not in ctrl:
                            ctrl["properties"] = val
                        ctrl["phrases_map"][key] = val
                    result["controls"].append(ctrl)
                    i = j
                else:
                    i += 1

    # Columns
    start, end = find_section_bounds(lines, "columns")
    if start is not None:
        col_lines = lines[start+1:end]
        i = 0
        while i < len(col_lines):
            if re.match(r'^\s*$', col_lines[i]):
                i += 1
                continue
            m_dash = re.match(r'^(\s*)-\s*$', col_lines[i])
            if m_dash:
                dash_indent = len(m_dash.group(1))
                j = i + 1
                block = []
                while j < len(col_lines):
                    m_next = re.match(r'^(\s*)-\s*$', col_lines[j])
                    if m_next and len(m_next.group(1)) == dash_indent:
                        break
                    block.append(col_lines[j])
                    j += 1
                phrases = parse_phrases_from_block(block, start+1+i+1)
                col = {"raw_lines": block, "phrases": phrases, "phrases_map": {}}
                for (ind, key, val, ln) in phrases:
                    if key == "name" and "name" not in col:
                        col["name"] = val.splitlines()[0].strip()
                    if key == "identifier" and "identifier" not in col:
                        col["identifier"] = val.splitlines()[0].strip()
                    if key == "type" and "type" not in col:
                        col["type"] = val.splitlines()[0].strip()
                    if key == "properties" and "properties" not in col:
                        col["properties"] = val
                    col["phrases_map"][key] = val
                result["columns"].append(col)
                i = j
            else:
                m_name = PHRASE_RE.match(col_lines[i])
                if m_name:
                    b_indent = len(m_name.group(1))
                    j = i
                    block = []
                    while j < len(col_lines):
                        mm = PHRASE_RE.match(col_lines[j])
                        if mm and len(mm.group(1)) <= b_indent and j != i:
                            break
                        block.append(col_lines[j])
                        j += 1
                    phrases = parse_phrases_from_block(block, start+1+i)
                    col = {"raw_lines": block, "phrases": phrases, "phrases_map": {}}
                    for (ind, key, val, ln) in phrases:
                        if key == "name" and "name" not in col:
                            col["name"] = val.splitlines()[0].strip()
                        if key == "identifier" and "identifier" not in col:
                            col["identifier"] = val.splitlines()[0].strip()
                        if key == "type" and "type" not in col:
                            col["type"] = val.splitlines()[0].strip()
                        if key == "properties" and "properties" not in col:
                            col["properties"] = val
                        col["phrases_map"][key] = val
                    result["columns"].append(col)
                    i = j
                else:
                    i += 1

    # Procedures: candidates from 'procedure :' and 'name :' with nearby code
    proc_candidates = []
    for idx, line in enumerate(lines):
        mproc = re.match(r'^\s*procedure\s*:\s*(\S+)\s*$', line, re.IGNORECASE)
        if mproc:
            nm = mproc.group(1).strip()
            tail = "\n".join(lines[idx: idx + 200])
            if re.search(r'\bcode\s*:\s*\|1[+\-]|\bp_codes\b|\bcode_elements\b', tail, re.IGNORECASE):
                proc_candidates.append({"name": nm, "pos": idx, "raw_tail": tail})

    for idx, line in enumerate(lines):
        m = PHRASE_RE.match(line)
        if m:
            key = m.group(2); val = m.group(3).strip()
            if key.lower() == "name" and val:
                look_ahead = "\n".join(lines[idx: idx + 200])
                if re.search(r'\bcode\s*:\s*\|1[+\-]|\bp_codes\b|\bcode_elements\b', look_ahead, re.IGNORECASE):
                    proc_candidates.append({"name": val.splitlines()[0].strip(), "pos": idx, "raw_tail": look_ahead})

    seen = set()
    procedures = []
    for c in proc_candidates:
        nm = c.get("name", "").strip()
        if nm and nm not in seen:
            seen.add(nm)
            procedures.append(c)
    result["procedures"] = procedures
    return result

# ---------------- Safe naming & translation heuristics ----------------
def _safe_name(s: str) -> str:
    if not s:
        return "unnamed"
    name = re.sub(r'\W+', '_', s, flags=re.UNICODE)
    if not re.match(r'^[A-Za-z_]', name):
        name = "_" + name
    return name

def translate_wlang_to_csharp(wcode: str) -> str:
    out = []
    for ln in wcode.splitlines():
        s = ln.rstrip("\n")
        stripped = s.lstrip()
        indent = s[:len(s) - len(stripped)]
        stripped = re.sub(r'\bVrai\b', 'true', stripped, flags=re.IGNORECASE)
        stripped = re.sub(r'\bFaux\b', 'false', stripped, flags=re.IGNORECASE)
        stripped = re.sub(r'\bET\b', '&&', stripped, flags=re.IGNORECASE)
        stripped = re.sub(r'\bOU\b', '||', stripped, flags=re.IGNORECASE)
        stripped = stripped.replace(':=', '=')
        if stripped.strip().lower().startswith('local'):
            out.append(f"{indent}// local variables declaration (WLang): {stripped}")
        elif stripped.strip().startswith('//') or stripped.strip().startswith('/*'):
            out.append(f"{indent}{stripped}")
        else:
            out.append(f"{indent}// TODO translate: {stripped}")
    return "\n".join(out)

# ---------------- Code extraction helpers ----------------
def extract_code_from_raw(raw_text: str) -> str:
    m = re.search(r'code\s*:\s*\|1[+\-]\s*[\r\n]+', raw_text, re.IGNORECASE)
    if not m:
        return ""
    start = m.end()
    rest = raw_text[start:]
    lines = rest.splitlines()
    collected = []
    for line in lines:
        if PHRASE_RE.match(line):
            break
        collected.append(line)
    while collected and collected[0].strip() == "":
        collected.pop(0)
    while collected and collected[-1].strip() == "":
        collected.pop()
    if not collected:
        return ""
    indents = [len(ln) - len(ln.lstrip(' ')) for ln in collected if ln.strip()]
    min_indent = min(indents) if indents else 0
    dedented = [ln[min_indent:] if len(ln) >= min_indent else ln for ln in collected]
    return "\n".join(dedented)

def extract_proc_code_from_fulltext(full_text: str, proc_name: str, start_pos: Optional[int] = None) -> str:
    """
    Recherche locale prioritaire à partir de start_pos si fourni, sinon recherche globale.
    """
    lines = full_text.splitlines()
    n = len(lines)

    def _extract_from_line_index(idx):
        tail = "\n".join(lines[idx: min(idx + 2000, n)])
        return extract_code_from_raw(tail)

    # 1) local search if start_pos is known
    if isinstance(start_pos, int) and 0 <= start_pos < n:
        window_end = min(n, start_pos + 500)
        # look for 'code : |1' after start_pos
        for idx in range(start_pos, window_end):
            if re.search(r'^\s*code\s*:\s*\|1[+\-]\s*$', lines[idx], flags=re.IGNORECASE):
                context = "\n".join(lines[max(0, start_pos-5): idx+1])
                if re.search(r'\b' + re.escape(proc_name) + r'\b', context, flags=re.IGNORECASE) or \
                   re.search(r'(?i)^\s*procedure\s*:\s*' + re.escape(proc_name) + r'\b', context, flags=re.MULTILINE):
                    code = _extract_from_line_index(idx)
                    if code:
                        return code
                else:
                    code = _extract_from_line_index(idx)
                    non_comment = [ln for ln in code.splitlines() if ln.strip() and not ln.strip().startswith('//')]
                    if non_comment:
                        return code
        # not found locally -> continue to global

    # 2) explicit 'procedure : name' search
    proc_pattern = re.compile(r'^\s*procedure\s*:\s*' + re.escape(proc_name) + r'\b', flags=re.IGNORECASE | re.MULTILINE)
    m = proc_pattern.search(full_text)
    if m:
        start_idx = m.end()
        line_index = full_text[:start_idx].count('\n')
        for idx in range(line_index, min(line_index + 2000, n)):
            if re.search(r'^\s*code\s*:\s*\|1[+\-]\s*$', lines[idx], flags=re.IGNORECASE):
                return _extract_from_line_index(idx)

    # 3) fallback: search for all 'code : |1' where proc_name appears before
    for m in re.finditer(r'code\s*:\s*\|1[+\-]\s*', full_text, flags=re.IGNORECASE):
        idx_char = m.start()
        line_idx = full_text[:idx_char].count('\n')
        before = full_text[max(0, idx_char - 2000): idx_char]
        if re.search(r'\b' + re.escape(proc_name) + r'\b', before, flags=re.IGNORECASE):
            return _extract_from_line_index(line_idx)
    return ""

# ---------------- New: window-level p_codes extraction ----------------
def extract_window_level_p_codes(full_text: str, events_map: Dict[int,str]) -> List[Tuple[str,str,str]]:
    """
    Extracts p_codes blocks located at the same level as 'procedures :' (window-level).
    Returns a list of tuples: (method_name, wlang_code, comment_label)
    - method_name: suggested C# method name (Window_Declaration, On_Window_Event_<type>, Window_Code_<n>)
    - wlang_code: the extracted WLang code (raw)
    - comment_label: human-readable label (type number + mapping)
    """
    lines = full_text.splitlines()
    n = len(lines)
    results = []
    # find procedures section start
    proc_idx = None
    for i, l in enumerate(lines):
        if re.match(r'^\s*procedures\s*:\s*$', l, flags=re.IGNORECASE):
            proc_idx = i
            break
    if proc_idx is None:
        return results

    # search backward up to 200 lines for a 'p_codes :' that is at top level (or close)
    p_codes_idx = None
    search_start = max(0, proc_idx - 200)
    for i in range(proc_idx - 1, search_start - 1, -1):
        if re.match(r'^\s*p_codes\s*:\s*$', lines[i], flags=re.IGNORECASE):
            p_codes_idx = i
            break
    if p_codes_idx is None:
        # nothing to do
        return results

    # from p_codes_idx, gather hyphen blocks until we reach the 'procedures' line (proc_idx)
    i = p_codes_idx + 1
    block_num = 0
    while i < proc_idx:
        # skip blanks
        if re.match(r'^\s*$', lines[i]):
            i += 1
            continue
        m_dash = re.match(r'^(\s*)-\s*$', lines[i])
        if m_dash:
            dash_indent = len(m_dash.group(1))
            j = i + 1
            block_lines = []
            while j < proc_idx:
                # stop at next '-' at same indent (new block) or at proc_idx
                m_next = re.match(r'^(\s*)-\s*$', lines[j])
                if m_next and len(m_next.group(1)) == dash_indent:
                    break
                block_lines.append(lines[j])
                j += 1
            # process this block: extract code and type
            raw_block = "\n".join(block_lines)
            wlang_code = extract_code_from_raw(raw_block)
            # find type in block
            type_num = None
            mtype = re.search(r'^\s*type\s*:\s*(\d+)', raw_block, flags=re.MULTILINE)
            if mtype:
                try:
                    type_num = int(mtype.group(1))
                except Exception:
                    type_num = None
            # determine method name and label
            label = None
            if type_num is not None:
                label = events_map.get(type_num, None)
            # special-case: first block may contain 'procedure <name>' (window declaration)
            if block_num == 0:
                # try detect 'procedure <name>' in the WLang (raw_block)
                mprocdecl = re.search(r'^\s*procedure\s+([A-Za-z0-9_]+)\s*\(.*\)', raw_block, flags=re.IGNORECASE | re.MULTILINE)
                if mprocdecl:
                    procname = mprocdecl.group(1)
                    method_name = "Window_Declaration"
                    comment_label = f"procedure declaration: {procname}"
                else:
                    method_name = f"Window_Code_{block_num}"
                    comment_label = f"type: {type_num or '?'}"
            else:
                if type_num is not None:
                    method_name = f"On_Window_Event_{type_num}"
                    comment_label = f"type: {type_num} ({label or 'unknown'})"
                else:
                    method_name = f"Window_Code_{block_num}"
                    comment_label = f"type: {type_num or '?'}"
            # ensure unique method_name
            existing_names = {r[0] for r in results}
            unique_name = method_name
            suffix = 1
            while unique_name in existing_names:
                suffix += 1
                unique_name = f"{method_name}_{suffix}"
            results.append((unique_name, wlang_code or "", comment_label))
            block_num += 1
            i = j
        else:
            # not a block start; skip
            i += 1
    return results

# ---------------- Render helpers ----------------
def render_event_method(control_name: Optional[str], event_label: Optional[str], event_type_num: Optional[int],
                        code_lines: List[str], occurrence_index: int = 0) -> Tuple[str, str]:
    verb = EVENT_TYPE_VERB.get(event_type_num)
    if not verb:
        if event_label:
            verb = re.sub(r'\W+', '_', event_label.split()[0]).lower()
        else:
            verb = f"type{event_type_num or 'unk'}"
    safe_control = _safe_name(control_name) if control_name else "window"
    method_name = f"On_{verb}_{safe_control}"
    if occurrence_index:
        method_name = f"{method_name}_{occurrence_index}"
    raw_code = "\n".join([l.rstrip("\n") for l in code_lines]).rstrip("\n")
    translated = translate_wlang_to_csharp(raw_code)
    body_lines = []
    body_lines.append("/* Original WLang:")
    for l in raw_code.splitlines():
        body_lines.append("   " + l)
    body_lines.append("*/")
    if translated.strip():
        body_lines.append("")
        body_lines.append("// Translated (heuristic):")
        for l in translated.splitlines():
            body_lines.append(l)
    else:
        body_lines.append("")
        body_lines.append("// No translation available")
    return method_name, "\n".join(body_lines)

# ---------------- Main generator ----------------
def generate_skeleton_from_clair(clair_path: str, out_dir: str, events_map: Dict[int,str], controls_map: Dict[int,str], lang: str = "fr"):
    anomalies: List[str] = []
    try:
        with open(clair_path, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except Exception as e:
        log_event(f"Impossible de lire {clair_path}: {e}", f"Unable to read {clair_path}: {e}", "ERROR")
        return

    model = collect_blocks_from_text(txt)

    # filter procedures: don't treat control names as procedures unless explicit 'procedure : name'
    control_names = { (c.get('name') or '').splitlines()[0].strip()
                      for c in model.get('controls', []) if c.get('name') }
    filtered_procs = []
    for p in model.get('procedures', []):
        pname = (p.get('name') or '').strip()
        explicit_proc = False
        pos = p.get('pos')
        if isinstance(pos, int):
            try:
                line_at_pos = txt.splitlines()[pos].strip()
                if re.match(r'(?i)^procedure\s*:', line_at_pos):
                    explicit_proc = True
            except Exception:
                explicit_proc = False
        if explicit_proc or (pname and pname not in control_names):
            filtered_procs.append(p)
        else:
            log_event(f"Suppression candidat procédure '{pname}' car nom identique à un contrôle.",
                      f"Skipping procedure candidate '{pname}' because it matches a control name.",
                      "INFO")
    model['procedures'] = filtered_procs

    # Extract window-level p_codes (new)
    window_code_blocks = extract_window_level_p_codes(txt, events_map)  # list of (method_name, wlang_code, label)
    # We'll convert them into code_methods entries (method_name, method_body)
    window_code_methods: List[Tuple[str,str]] = []
    for (mname, wcode, label) in window_code_blocks:
        # Build the comment and translation
        comment_lines = []
        comment_lines.append(f"/* Code attaché à la fenêtre : {label} */")
        # keep original WLang inside comment block as required
        if wcode and wcode.strip():
            comment = "/* Original WLang:\n"
            for l in wcode.splitlines():
                comment += "   " + l + "\n"
            comment += "*/\n"
        else:
            comment = "/* (aucun code WLang explicite trouvé) */\n"
        translated = translate_wlang_to_csharp(wcode or "")
        body = comment
        if translated.strip():
            body += "\n// Translated (heuristic):\n" + translated + "\n"
        else:
            body += "\n// No translation available\n"
        window_code_methods.append((mname, body))

    # continue building razor + cs as before
    base = os.path.splitext(os.path.basename(clair_path))[0].replace("_wdw","")
    razor_lines: List[str] = []
    code_methods: List[Tuple[str,str]] = []  # will include control event handlers + window_code_methods + procedures' methods

    razor_lines.append(f"@* Generated from {os.path.basename(clair_path)} at {_now_str(fr=(lang=='fr'))} *@")
    razor_lines.append("")
    razor_lines.append(f'@page "/fen_{_safe_name(base).lower()}"')
    razor_lines.append("")
    razor_lines.append(f'<div class="windev-window" data-source="{os.path.basename(clair_path)}">')

    # Controls -> markup + event handlers
    for ctrl in model.get("controls", []):
        name = ctrl.get("name", "unnamed").splitlines()[0].strip()
        type_raw = ctrl.get("type", "").splitlines()[0].strip() if ctrl.get("type") else ""
        try:
            type_num = int(re.match(r'^(\d+)', type_raw).group(1))
        except Exception:
            type_num = None
        phrases_map = ctrl.get("phrases_map", {}) or {}
        props_raw = ctrl.get("properties", "") or ""

        # build prop_attrs safely (preserve properties)
        prop_attrs = ""
        if props_raw:
            parts = [p.strip() for p in props_raw.split(',') if p.strip()]
            attrs = []
            for p in parts:
                if ':' in p:
                    k, v = p.split(':', 1)
                    key_attr = 'data-' + k.strip().replace(" ", "-")
                    val_attr = v.strip().replace('"', "'")
                    attrs.append(f'{key_attr}="{val_attr}"')
            if attrs:
                prop_attrs = " " + " ".join(attrs)

        label = None
        if type_num is not None and type_num in controls_map:
            label = controls_map[type_num]
        if label is None and type_num is not None and type_num in DEFAULT_CONTROL_TO_BLAZOR:
            label = DEFAULT_CONTROL_TO_BLAZOR[type_num]

        is_calendar = False
        if type_num == 2:
            for k, v in phrases_map.items():
                if k.strip().lower() == "calendar" and (not v or v.strip().lower() in ("vrai", "true", "1")):
                    is_calendar = True
                    break
            if not is_calendar:
                for rl in ctrl.get("raw_lines", []):
                    if re.match(r'^\s*calendar\s*[:]*\s*', rl, re.IGNORECASE):
                        is_calendar = True
                        break

        event_attrs: Dict[str, str] = {}
        if label is None:
            anomalies.append(f"Control unknown type {type_raw} for control '{name}'")
            markup = f'<div class="windev-unknown" data-windev-type="{type_raw}" data-name="{name}"{prop_attrs}>/* {name} */</div>'
        else:
            l = label.lower()
            if is_calendar:
                markup = f'<InputDate id="{name}" @bind-Value="{name}Model"{prop_attrs} />'
                event_attrs["@onchange"] = ""
            elif "champ" in l or "saisie" in l or "inputtext" in l or "texte" in l:
                markup = f'<InputText id="{name}" @bind-Value="{name}Model"{prop_attrs} />'
                event_attrs["@oninput"] = ""; event_attrs["@onchange"] = ""
            elif "bouton" in l or "button" in l:
                markup = f'<button id="{name}"{prop_attrs}>{name}</button>'
                event_attrs["@onclick"] = ""
            elif "libell" in l or "label" in l:
                markup = f'<label id="{name}">{name}</label>'
            elif "select" in l or "combo" in l or "liste" in l:
                markup = f'<select id="{name}"{prop_attrs}></select>'
                event_attrs["@onchange"] = ""
            elif "table" in l or "tcd" in l:
                markup = f'<table id="{name}"{prop_attrs}><thead></thead><tbody></tbody></table>'
            else:
                safe_class = re.sub(r'\s+', '-', label).lower()
                markup = f'<div id="{name}" class="windev-{safe_class}"{prop_attrs}>{name}</div>'

        # extract p_codes of the control -> event handlers
        raw = ctrl.get("raw_lines", []) or []
        if raw:
            local_lines = list(raw)
            li = 0
            occurrence_counters = {}
            while li < len(local_lines):
                if re.match(r'^\s*p_codes\s*:\s*$', local_lines[li]):
                    p_indent = len(re.match(r'^(\s*)', local_lines[li]).group(1))
                    li += 1
                    while li < len(local_lines):
                        if re.match(r'^\s*$', local_lines[li]):
                            li += 1
                            continue
                        mm = PHRASE_RE.match(local_lines[li])
                        if mm and len(mm.group(1)) <= p_indent:
                            break
                        ev_start = re.match(r'^(\s*)-\s*$', local_lines[li])
                        if not ev_start:
                            li += 1
                            continue
                        ev_indent = len(ev_start.group(1))
                        ev_lines = []
                        li += 1
                        while li < len(local_lines):
                            if re.match(rf'^\s{{{ev_indent}}}-\s*$', local_lines[li]):
                                break
                            mm = PHRASE_RE.match(local_lines[li])
                            if mm and len(mm.group(1)) <= p_indent:
                                break
                            ev_lines.append(local_lines[li])
                            li += 1
                        if any(re.match(r'^\s*code\s*:\s*\|1[+\-]\s*$', l.strip()) for l in ev_lines):
                            type_num_ev = None
                            for el in ev_lines:
                                mt = re.match(r'^\s*type\s*:\s*(\d+)', el.strip())
                                if mt:
                                    type_num_ev = int(mt.group(1)); break
                            codeblock = []
                            in_code = False
                            for el in ev_lines:
                                if re.match(r'^\s*code\s*:\s*\|1[+\-]\s*$', el.strip()):
                                    in_code = True
                                    continue
                                if in_code:
                                    codeblock.append(el.rstrip("\n"))
                            occ_key = str(type_num_ev)
                            occurrence_counters[occ_key] = occurrence_counters.get(occ_key, 0) + 1
                            occ_idx = occurrence_counters[occ_key] - 1
                            ev_label = None
                            if type_num_ev is not None:
                                ev_label = events_map.get(type_num_ev)
                            mname, mbody = render_event_method(name, ev_label, type_num_ev, codeblock, occ_idx)
                            code_methods.append((mname, mbody))
                            verb = EVENT_TYPE_VERB.get(type_num_ev)
                            if verb == "input":
                                if "@oninput" in event_attrs:
                                    event_attrs["@oninput"] = mname
                                else:
                                    event_attrs["@onchange"] = mname
                            elif verb == "focus":
                                event_attrs["@onfocus"] = mname
                            elif verb == "blur":
                                event_attrs["@onblur"] = mname
                            elif verb == "click":
                                event_attrs["@onclick"] = mname
                            else:
                                if "@onchange" in event_attrs:
                                    event_attrs["@onchange"] = mname
                                else:
                                    event_attrs[f"data-handler-type-{type_num_ev}"] = mname
                else:
                    li += 1

        # inject event attributes if methods assigned (non-empty)
        attr_str = ""
        for k, v in event_attrs.items():
            if v:
                attr_str += f' {k}="{v}"'
        if attr_str:
            if "/>" in markup:
                markup = markup.replace("/>", f'{attr_str} />')
            else:
                pos = markup.find('>')
                if pos != -1:
                    markup = markup[:pos] + attr_str + markup[pos:]

        razor_lines.append("  " + markup)

    razor_lines.append("</div>")
    razor_lines.append("")

    # Build .razor.cs
    code_lines: List[str] = []
    code_lines.append("using System;")
    code_lines.append("using Microsoft.AspNetCore.Components;")
    code_lines.append("")
    code_lines.append("namespace Generated")
    code_lines.append("{")
    safe_classname = re.sub(r'\W+', '_', base).strip('_') or "GeneratedWindow"
    code_lines.append(f"    public partial class {safe_classname} : ComponentBase")
    code_lines.append("    {")

    # models for inputs
    for ctrl in model.get("controls", []):
        name = ctrl.get("name", "unnamed").splitlines()[0].strip()
        type_val = ctrl.get("type", "").splitlines()[0].strip() if ctrl.get("type") else ""
        try:
            typ = int(re.match(r'^(\d+)', type_val).group(1))
        except Exception:
            typ = None
        phrases_map = ctrl.get("phrases_map", {}) or {}
        is_calendar = False
        if typ == 2:
            for k in phrases_map:
                if k.strip().lower() == "calendar":
                    is_calendar = True; break
        if typ in DEFAULT_CONTROL_TO_BLAZOR and "input" in DEFAULT_CONTROL_TO_BLAZOR[typ] and not is_calendar:
            code_lines.append(f"        public string {name}Model {{ get; set; }} = string.Empty;")
        if is_calendar:
            code_lines.append(f"        public DateTime? {name}Model {{ get; set; }} = null;")

    code_lines.append("")

    # Insert window-level code methods first (so they appear near top)
    for mname, mbody in window_code_methods:
        code_lines.append(f"        public void {mname}()")
        code_lines.append("        {")
        for bl in mbody.splitlines():
            code_lines.append("            " + bl)
        code_lines.append("        }")
        code_lines.append("")

    # event methods (from controls)
    for mname, mbody in code_methods:
        code_lines.append(f"        public void {mname}()")
        code_lines.append("        {")
        for bl in mbody.splitlines():
            code_lines.append("            " + bl)
        code_lines.append("        }")
        code_lines.append("")

    # PROCEDURES: only those retained in model['procedures']
    proc_name_counts: Dict[str, int] = {}
    for proc in model.get("procedures", []):
        original_name = proc.get("name", "").strip()
        if not original_name:
            continue
        start_pos = proc.get("pos") if isinstance(proc.get("pos"), int) else None
        wlang_code = extract_proc_code_from_fulltext(txt, original_name, start_pos=start_pos)
        safe_proc_name = _safe_name(original_name)
        count = proc_name_counts.get(safe_proc_name, 0)
        proc_name_counts[safe_proc_name] = count + 1
        if count > 0:
            safe_proc_name = f"{safe_proc_name}_{count}"

        # Write original WLang as comment (always)
        code_lines.append(f"        // Procédure originale : {original_name}")
        code_lines.append("        /*")
        if wlang_code and wlang_code.strip():
            for line in wlang_code.splitlines():
                code_lines.append("        " + line)
        else:
            raw_tail = proc.get("raw_tail", "") if isinstance(proc, dict) else ""
            if raw_tail:
                excerpt_lines = raw_tail.splitlines()[:60]
                for line in excerpt_lines:
                    code_lines.append("        " + line)
            else:
                code_lines.append("        (aucun code WLang explicite trouvé pour cette procédure)")
        code_lines.append("        */")
        # method declaration
        code_lines.append(f"        public void {safe_proc_name}()")
        code_lines.append("        {")
        if wlang_code and wlang_code.strip():
            translated = translate_wlang_to_csharp(wlang_code)
            if translated and translated.strip():
                for line in translated.splitlines():
                    code_lines.append("            " + line)
            else:
                code_lines.append("            // TODO translate WLang code to C#")
        else:
            code_lines.append("            // TODO implement: no explicit code extracted for this procedure")
        code_lines.append("        }")
        code_lines.append("")

    code_lines.append("    }")
    code_lines.append("}")

    # write files
    try:
        os.makedirs(out_dir, exist_ok=True)
        razor_path = os.path.join(out_dir, f"{base}.razor")
        cs_path = os.path.join(out_dir, f"{base}.razor.cs")
        with open(razor_path, "w", encoding="utf-8") as f:
            f.write("\n".join(razor_lines))
        with open(cs_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines))
        print_bilingual(f"Généré : {razor_path} (+ {cs_path})", f"Generated: {razor_path} (+ {cs_path})", lang=lang)
    except Exception as e:
        log_event(f"Erreur écriture fichiers : {e}", f"Error writing output files: {e}", "ERROR")

    for a in anomalies:
        log_event(f"Anomalie: {a}", f"Anomaly: {a}", "WARNING")

# ---------------- Directory processing & CLI ----------------
def process_directory(dir_path: str, lang: str = "fr") -> int:
    if not os.path.isdir(dir_path):
        raise Exception(f"Répertoire introuvable: {dir_path}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    events_map = load_events_mapping(script_dir)
    controls_map = load_controls_mapping(script_dir)
    clarif_dir = os.path.join(dir_path, "clarifications")
    if not os.path.isdir(clarif_dir):
        print_bilingual(f"Pas de dossier 'clarifications' dans {dir_path}", f"No 'clarifications' in {dir_path}", lang=lang)
        return 0
    out_dir = os.path.join(dir_path, "squelettes")
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for name in os.listdir(clarif_dir):
        if not name.lower().endswith(".clair"):
            continue
        clair_path = os.path.join(clarif_dir, name)
        try:
            generate_skeleton_from_clair(clair_path, out_dir, events_map, controls_map, lang=lang)
            count += 1
        except Exception as e:
            log_event(f"Erreur generation {name}: {e}", f"Failed generating {name}: {e}", "ERROR")
            log_event(traceback.format_exc(), traceback.format_exc(), "ERROR")
    return count

def parse_args(argv: List[str]):
    p = argparse.ArgumentParser(description="Génère des squelettes Blazor .razor à partir de fichiers clarifiés Windev.")
    p.add_argument("--dir", required=True, help="Répertoire racine contenant 'clarifications'")
    p.add_argument("--lang", choices=["fr", "en"], default="fr", help="Langue des messages")
    return p.parse_args(argv)

def main(argv: List[str]) -> int:
    cmd = " ".join([sys.executable] + [os.path.abspath(__file__)] + argv)
    _prepend_line(FR_LOG, f"{_now_str(True)} [START] Commande : {cmd}")
    _prepend_line(EN_LOG, f"{_now_str(False)} [START] Command : {cmd}")
    try:
        args = parse_args(argv)
        print_bilingual(f"Début génération squelettes dans {args.dir}", f"Start generating skeletons in {args.dir}", lang=args.lang)
        c = process_directory(args.dir, lang=args.lang)
        print_bilingual(f"Terminé. Squelettes générés : {c}", f"Done. Skeletons generated: {c}", lang=args.lang)
        return 0
    except Exception as e:
        log_event(f"Erreur inattendue: {e}", f"Unexpected error: {e}", "ERROR")
        log_event(traceback.format_exc(), traceback.format_exc(), "ERROR")
        return 2
    finally:
        _prepend_line(FR_LOG, f"{_now_str(True)} [END] Fin")
        _prepend_line(EN_LOG, f"{_now_str(False)} [END] End")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
