#!/usr/bin/env python3
"""
Mechanical validator for the SupremeFrontEnd skill.

This script is intentionally boring and binding: it does not judge taste, but it
blocks empty artifacts, fake gates, missing screenshots, raw styling drift, and
self-declared PASS statuses that are not externally validated.

Usage:
  python scripts/validate_skill_state.py --root .
  python scripts/validate_skill_state.py --root . --implementation ../app/src
  python scripts/validate_skill_state.py --root . --implementation ../app/src --require-final-pass
  python scripts/validate_skill_state.py --root . --json

Exit code:
  0 = pass
  1 = fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Any

DEFAULT_CONFIG: dict[str, Any] = {
    "thresholds": {"slop_max_exclusive": 6, "premium_min_inclusive": 15},
    "token_contract_minimums": {
        "color_roles": 5,
        "color_values": 3,
        "spacing_values": 5,
        "type_values": 5,
        "radius_values": 3,
        "shadow_levels_or_no_shadow_policy": 2,
    },
    "component_rules_minimums": {"state_terms": 5, "accessibility_terms": 3, "usage_markers": 4},
    "allowed_final_statuses": [
        "PASS_EXTERNALLY_VALIDATED",
        "FAIL_REVISE_REQUIRED",
        "BLOCKED_SCREENSHOT_UNAVAILABLE",
        "SPEC_COMPLETE_UNVERIFIED",
        "DRAFT_SELF_SCORE_ONLY",
    ],
    "required_final_status_for_deploy": "PASS_EXTERNALLY_VALIDATED",
    "vibe_words": ["premium", "modern", "clean", "beautiful", "polished", "sleek"],
    "mechanism_words": [
        "spacing", "hierarchy", "typography", "contrast", "radius", "shadow", "token",
        "component", "line-height", "line height", "max-width", "grid", "alignment",
        "semantic", "state", "focus", "accessibility", "mobile", "rtl", "color role",
        "line length", "touch target", "density", "scale", "elevation", "border", "motion",
    ],
    "vibe_check_exempt_paths": [
        "project-state/PREMIUM_DEFINITION.md",
        "PREMIUM_VS_SLOP.md",
        "SCORECARDS.md",
        "DESIGN_BRAIN.md",
    ],
    "allowed_px_values": [0,1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,44,48,56,64,72,80,96,112,128,144,160],
    "banned_copy": [
        "unlock your potential", "seamless journey", "transform your wellness",
        "ai-powered personalized journey", "get started", "learn more",
    ],
    "implementation_token_file_markers": ["token", "theme", "variables", "tailwind.config", "design-system"],
    # v5: numeric design-brain rules enforced against BUILT output (not just advisory text).
    # These are heuristic signals: unambiguous violations FAIL, ambiguous ones WARN.
    "design_brain_rules": {
        "body_line_height_min": 1.3,
        "body_line_height_max": 1.9,
        "line_height_hard_floor": 1.15,   # unitless <= this applied to text is a slop signal -> FAIL
        "touch_target_min_px": 44,
        "shadow_blur_to_offset_max_ratio": 5,  # blur > ratio*|y-offset| = fuzzy AI glow -> WARN
        "require_prose_line_length_constraint": True,  # a max-width in ch OR prose max-w utility must exist
    },
    # v5: screenshots must be real image files with real dimensions, not text mentions.
    "screenshot_artifacts": {
        "dir": "screenshots",
        "required_states": ["desktop", "mobile"],
        "min_width": 320,
        "min_height": 320,
    },
    # v5: provenance that an implementing agent cannot plausibly improvise.
    "reference_dna_provenance": {
        "required": True,
        "min_source_urls": 1,
        # A tool-emitted marker proving the DNA came from a `study`/extraction step, not eyeballing.
        "signature_markers": ["studied:", "study signature", "extraction-source", "source-hash", "fetched-at"],
    },
    "blind_review_provenance": {
        "required": True,
        # Something outside the implementer's own context: a session id, transcript hash, or human sign-off.
        "markers": ["reviewer-session:", "transcript-hash:", "reviewer-initials:", "reviewed-at:"],
    },
    # v5: silent extraction degradation (e.g. CSS stripped on fetch) must be visible and cap the ceiling.
    "extraction_degraded_flag": "project-state/EXTRACTION_DEGRADED.md",
    "extraction_degraded_premium_cap": 14,
    # v5.1: grilling must resolve every taste axis, not just N questions.
    "grilling_coverage": {
        "required": True,
        "axes": {
            "feel": ["feel", "three words", "mood", "tone", "emotion"],
            "anti_feel": ["not feel", "avoid", "anti-target", "hate", "cringe", "cheap", "fake"],
            "layout": ["layout", "spacious", "editorial", "compact", "grid", "density", "boxed", "asymmetric"],
            "typography": ["type", "font", "serif", "sans", "headline", "heading", "typeface"],
            "color": ["color", "colour", "accent", "neutral", "palette", "monochrome", "pastel"],
            "key_component": ["hero", "chatbot", "chat", "form", "card", "profile", "matching", "dashboard", "gallery", "calendar", "checkout"],
            "interaction": ["motion", "interaction", "hover", "animation", "guided", "explore", "step-by-step", "conversational"],
            "rtl": ["rtl", "hebrew", "arabic", "right-to-left", "mirror", "bidi"],
        },
        "min_references_with_liked": 2,
        "reference_liked_markers": ["liked:", "likes:", "borrow:", "one thing:", "what i like", "keep:"],
    },
    # v5.2: reference extraction must run through a real tool, set up if missing not eyeballed.
    "extraction_tool": {
        "required": True,
        "record_file": "project-state/EXTRACTION_TOOL.md",
        "accepted_tools": ["playwright", "hallmark", "design-extract", "puppeteer", "study", "webfetch"],
        "manual_markers": ["manual only", "eyeball", "by eye", "guessed", "no tool", "none set up"],
    },
    # v5.3: one-shot quality levers.
    "organizing_idea": {"required": True, "file": "project-state/ORGANIZING_IDEA.md", "min_words": 10},
    "real_content": {"required": True, "file": "project-state/REAL_CONTENT.md", "min_words": 25},
    "reference_shots": {"required": True, "dir": "screenshots/refs", "min_count": 1},
    "restraint": {"max_colors": 10, "max_font_families": 2, "max_font_weights": 3},
}

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"fill this in",
    r"placeholder",
    r"lorem ipsum",
    r"coming soon",
    r"to be added",
    r"\[insert",
    r"\[fill",
    r"<insert",
    r"<fill",
]

RAW_HEX_RE = re.compile(r"(?<![\w-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})(?![\w-])")
PX_RE = re.compile(r"(?<![\w-])(\d{1,3})px(?![\w-])")

@dataclass
class Check:
    name: str
    status: str  # PASS/WARN/FAIL
    detail: str


def load_config(root: Path) -> dict[str, Any]:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    path = root / "VALIDATOR_CONFIG.json"
    if path.exists():
        try:
            custom = json.loads(path.read_text(encoding="utf-8"))
            deep_merge(cfg, custom)
        except Exception as exc:
            # Config parse errors are handled as a normal check later.
            cfg["__config_error__"] = str(exc)
    return cfg


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_merge(base[k], v)
        else:
            base[k] = v


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zא-ת0-9_-]+", text)


def count_bullets(text: str) -> int:
    return len(re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\S+", text))


def has_placeholder(text: str) -> bool:
    return any(re.search(p, text, re.I) for p in PLACEHOLDER_PATTERNS)


def vibe_without_mechanism(text: str, cfg: dict[str, Any]) -> list[str]:
    findings = []
    sentences = re.split(r"(?<=[.!?\n])\s+", text)
    vibe_words = [str(v).lower() for v in cfg["vibe_words"]]
    mechanism_words = [str(m).lower() for m in cfg["mechanism_words"]]
    for sentence in sentences:
        low = sentence.lower()
        if any(v in low for v in vibe_words) and not any(m in low for m in mechanism_words):
            findings.append(sentence.strip()[:220])
    return findings[:8]


def is_vibe_exempt(rel: str, cfg: dict[str, Any]) -> bool:
    rel_norm = rel.replace("\\", "/")
    return any(rel_norm == p or rel_norm.endswith("/" + p) for p in cfg.get("vibe_check_exempt_paths", []))


def section_count(text: str) -> int:
    return len(re.findall(r"(?m)^#{1,4}\s+", text))


def require_file(checks: list[Check], root: Path, rel: str, cfg: dict[str, Any], min_words: int = 20, min_bullets: int = 0, min_sections: int = 0) -> str:
    path = root / rel
    text = read(path)
    if not text:
        checks.append(Check(rel, "FAIL", "Missing file or unreadable."))
        return ""
    wc = len(words(text))
    bullets = count_bullets(text)
    sections = section_count(text)
    failures = []
    if wc < min_words:
        failures.append(f"only {wc} words; expected at least {min_words}")
    if bullets < min_bullets:
        failures.append(f"only {bullets} bullet/list items; expected at least {min_bullets}")
    if sections < min_sections:
        failures.append(f"only {sections} headings; expected at least {min_sections}")
    if has_placeholder(text):
        failures.append("contains placeholder/TODO-like text")
    if not is_vibe_exempt(rel, cfg):
        vibes = vibe_without_mechanism(text, cfg)
        if vibes:
            failures.append("contains vibe words without mechanisms: " + "; ".join(vibes[:2]))
    if failures:
        checks.append(Check(rel, "FAIL", "; ".join(failures)))
    else:
        checks.append(Check(rel, "PASS", f"{wc} words, {bullets} bullets, {sections} headings."))
    return text


def check_config(checks: list[Check], cfg: dict[str, Any]) -> None:
    if "__config_error__" in cfg:
        checks.append(Check("VALIDATOR_CONFIG.json", "FAIL", "Config parse error: " + cfg["__config_error__"]))
    else:
        checks.append(Check("VALIDATOR_CONFIG.json", "PASS", "Config loaded; thresholds have single source of truth."))


def check_token_contract(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    rel = "project-state/TOKEN_CONTRACT.md"
    text = require_file(checks, root, rel, cfg, min_words=50, min_bullets=8, min_sections=3)
    if not text:
        return
    low = text.lower()
    mins = cfg["token_contract_minimums"]
    color_roles = sum(1 for term in ["background", "surface", "text", "muted", "border", "action", "primary", "secondary", "error", "success", "warning", "focus"] if term in low)
    hexes = len(RAW_HEX_RE.findall(text))
    hsl = len(re.findall(r"hsl\(|oklch\(|rgb\(", text, flags=re.I))
    spacing_values = len(re.findall(r"(?:space|spacing|gap|padding|margin)[-_ ]?\w*\s*[:=\-]\s*(?:\d+(?:\.\d+)?(?:px|rem)|var\()", text, flags=re.I))
    type_values = len(re.findall(r"(?:font|text|type|heading|body|label|caption|hero)[-_ ]?\w*\s*[:=\-]\s*(?:\d+(?:\.\d+)?(?:px|rem)|[\w-]+)", text, flags=re.I))
    radius_values = len(re.findall(r"radius[-_ ]?\w*\s*[:=\-]\s*(?:\d+(?:\.\d+)?(?:px|rem)|var\()", text, flags=re.I))
    shadow_values = len(re.findall(r"shadow|elevation|box-shadow", text, flags=re.I))
    failures = []
    if color_roles < mins["color_roles"] or (hexes + hsl) < mins["color_values"]:
        failures.append(f"needs >={mins['color_roles']} color roles and >={mins['color_values']} actual color values; found roles={color_roles}, values={hexes+hsl}")
    if spacing_values < mins["spacing_values"]:
        failures.append(f"needs >={mins['spacing_values']} spacing token values; found {spacing_values}")
    if type_values < mins["type_values"]:
        failures.append(f"needs >={mins['type_values']} type token values/roles; found {type_values}")
    if radius_values < mins["radius_values"]:
        failures.append(f"needs >={mins['radius_values']} radius values; found {radius_values}")
    if shadow_values < mins["shadow_levels_or_no_shadow_policy"] and "no-shadow" not in low and "no shadow" not in low:
        failures.append(f"needs >={mins['shadow_levels_or_no_shadow_policy']} shadow/elevation levels or explicit no-shadow policy")
    checks.append(Check("TOKEN_CONTRACT content", "FAIL" if failures else "PASS", "; ".join(failures) if failures else "Token contract has concrete values/roles."))


def check_component_rules(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    rel = "project-state/COMPONENT_RULES.md"
    text = require_file(checks, root, rel, cfg, min_words=80, min_bullets=8, min_sections=3)
    if not text:
        return
    low = text.lower()
    mins = cfg["component_rules_minimums"]
    state_terms = ["default", "hover", "focus", "active", "selected", "disabled", "loading", "error", "empty", "success"]
    state_count = sum(1 for s in state_terms if s in low)
    a11y_terms = ["accessibility", "aria", "keyboard", "focus", "contrast", "screen reader", "label"]
    a11y_count = sum(1 for a in a11y_terms if a in low)
    usage_terms = ["use when", "do not use", "variant", "required", "responsive", "mobile", "rtl"]
    usage_count = sum(1 for u in usage_terms if u in low)
    failures = []
    if state_count < mins["state_terms"]:
        failures.append(f"needs >={mins['state_terms']} state terms; found {state_count}")
    if a11y_count < mins["accessibility_terms"]:
        failures.append(f"needs >={mins['accessibility_terms']} accessibility terms; found {a11y_count}")
    if usage_count < mins["usage_markers"]:
        failures.append(f"needs usage/variant/responsive/RTL rules; found {usage_count} markers")
    checks.append(Check("COMPONENT_RULES content", "FAIL" if failures else "PASS", "; ".join(failures) if failures else "Component rules include states, accessibility, and usage."))


def extract_score(text: str, name: str) -> int | None:
    pattern = rf"{name}\s*(?:score)?\s*[:=]\s*(\d+)"
    m = re.search(pattern, text, flags=re.I)
    return int(m.group(1)) if m else None


def check_scores(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    combined = read(root / "project-state/SCREENSHOT_REVIEW_REPORT.md") + "\n" + read(root / "project-state/LOOP_REPORT.md") + "\n" + read(root / "project-state/BLIND_REVIEW_REPORT.md")
    if not combined.strip():
        checks.append(Check("score reports", "FAIL", "Missing screenshot/loop/blind review reports."))
        return
    slop = extract_score(combined, "slop")
    premium = extract_score(combined, "premium")
    bullets = count_bullets(combined)
    failures = []
    slop_max = int(cfg["thresholds"]["slop_max_exclusive"])
    premium_min = int(cfg["thresholds"]["premium_min_inclusive"])
    if slop is None:
        failures.append("missing slop score")
    elif slop >= slop_max:
        failures.append(f"slop score {slop} fails threshold <{slop_max}")
    if premium is None:
        failures.append("missing premium score")
    elif premium < premium_min:
        failures.append(f"premium score {premium} fails threshold >={premium_min}")
    if bullets < 8:
        failures.append(f"needs itemized score/fixes; only {bullets} list items found")
    checks.append(Check("score thresholds", "FAIL" if failures else "PASS", "; ".join(failures) if failures else f"slop={slop}, premium={premium}, itemized."))


def screenshot_gate_status(root: Path, cfg: dict[str, Any] | None = None) -> str:
    # v5: real image files are the strongest evidence. Text mentions alone no longer pass.
    if cfg is not None:
        required = list(cfg.get("screenshot_artifacts", {}).get("required_states", []))
        if required:
            found = real_screenshots(root, cfg)
            if all(s in found for s in required):
                return "PASS"
    text = read(root / "project-state/SCREENSHOT_REVIEW_REPORT.md")
    if not text:
        return "FAIL"
    low = text.lower()
    blocked = "blocked_from_final_pass" in low or "blocked from final pass" in low or "screenshots unavailable" in low
    if blocked:
        return "BLOCKED"
    # Without real files, a text-only report can no longer reach PASS; it can only be BLOCKED.
    return "FAIL"


def check_screenshot_gate(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    status = screenshot_gate_status(root, cfg)
    if status == "PASS":
        checks.append(Check("screenshot gate", "PASS", "Screenshot review references desktop/mobile or image artifacts."))
    elif status == "BLOCKED":
        checks.append(Check("screenshot gate", "WARN", "Screenshots unavailable; final pass must be blocked."))
    else:
        checks.append(Check("screenshot gate", "FAIL", "No meaningful screenshot references and no explicit blocked status."))


def check_final_status(checks: list[Check], root: Path, cfg: dict[str, Any], require_final_pass: bool) -> None:
    rel = "project-state/FINAL_STATUS.md"
    text = read(root / rel)
    if not text:
        checks.append(Check("FINAL_STATUS", "FAIL", "Missing FINAL_STATUS.md."))
        return
    allowed = list(cfg["allowed_final_statuses"])
    # Prefer an explicit current status line so the file can document allowed values.
    explicit = re.search(r"(?mi)^\s*(?:current status|status)\s*:?\s*([A-Z_]+)\s*$", text)
    if explicit:
        found = [explicit.group(1)]
    else:
        found = [s for s in allowed if re.search(rf"(?m)^\s*{re.escape(s)}\s*$", text)]
    if len(found) != 1 or found[0] not in allowed:
        checks.append(Check("FINAL_STATUS", "FAIL", f"Must contain exactly one allowed current status; found {found or 'none'}."))
        return
    status = found[0]
    if status == "PASS_EXTERNALLY_VALIDATED":
        # PASS must include blind review report and screenshots.
        blind = read(root / "project-state/BLIND_REVIEW_REPORT.md").lower()
        if screenshot_gate_status(root, cfg) != "PASS":
            checks.append(Check("FINAL_STATUS", "FAIL", "PASS_EXTERNALLY_VALIDATED requires screenshot gate PASS."))
            return
        if not blind or "blind reviewer" not in blind or "pass" not in blind:
            checks.append(Check("FINAL_STATUS", "FAIL", "PASS_EXTERNALLY_VALIDATED requires a blind reviewer report marked pass."))
            return
    if require_final_pass and status != cfg["required_final_status_for_deploy"]:
        checks.append(Check("FINAL_STATUS", "FAIL", f"Deploy/pre-commit requires {cfg['required_final_status_for_deploy']}; found {status}."))
    else:
        checks.append(Check("FINAL_STATUS", "PASS", f"Status is {status}."))


def check_required_project_state(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    required = [
        ("project-state/PRODUCT_CONTEXT.md", 50, 4, 1),
        ("project-state/APPROVED_DESIGN_DIRECTION.md", 80, 6, 2),
        ("project-state/FRONTEND_SCREEN_SPEC.md", 100, 8, 3),
    ]
    for rel, min_words, min_bullets, min_sections in required:
        require_file(checks, root, rel, cfg, min_words, min_bullets, min_sections)


def scan_implementation(checks: list[Check], implementation: Path, cfg: dict[str, Any]) -> int:
    if not implementation or not implementation.exists():
        return 0
    exts = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte"}
    raw_hex_hits: list[str] = []
    banned_copy_hits: list[str] = []
    placeholder_hits: list[str] = []
    px_hits: list[str] = []
    token_file_markers = tuple(str(x).lower() for x in cfg.get("implementation_token_file_markers", []))
    banned_copy = [str(x).lower() for x in cfg.get("banned_copy", [])]
    allowed_px = set(int(x) for x in cfg.get("allowed_px_values", []))
    for path in implementation.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(path.relative_to(implementation))
        is_token_file = any(m in rel.lower() for m in token_file_markers)
        if not is_token_file:
            for m in RAW_HEX_RE.finditer(text):
                raw_hex_hits.append(f"{rel}:{text[:m.start()].count(chr(10))+1}:{m.group(0)}")
                if len(raw_hex_hits) >= 20:
                    break
        for phrase in banned_copy:
            if phrase in text.lower():
                banned_copy_hits.append(f"{rel}: contains '{phrase}'")
        if has_placeholder(text):
            placeholder_hits.append(rel)
        for m in PX_RE.finditer(text):
            value = int(m.group(1))
            if value not in allowed_px:
                px_hits.append(f"{rel}:{text[:m.start()].count(chr(10))+1}:{value}px")
                if len(px_hits) >= 20:
                    break
    checks.append(Check("implementation raw hex", "FAIL" if raw_hex_hits else "PASS", "Raw hex values outside token/theme files: " + "; ".join(raw_hex_hits[:8]) if raw_hex_hits else "No raw hex values outside token/theme files found."))
    checks.append(Check("implementation banned copy", "FAIL" if banned_copy_hits else "PASS", "; ".join(banned_copy_hits[:8]) if banned_copy_hits else "No banned filler copy found."))
    checks.append(Check("implementation placeholders", "FAIL" if placeholder_hits else "PASS", "Placeholder/TODO-like text in: " + "; ".join(placeholder_hits[:8]) if placeholder_hits else "No placeholder/TODO-like text found."))
    checks.append(Check("implementation arbitrary px", "WARN" if px_hits else "PASS", "Non-scale px values found: " + "; ".join(px_hits[:8]) if px_hits else "No obvious arbitrary px values found."))
    # FAIL-level violations only (px is a warning); used for score cross-check.
    return len(raw_hex_hits) + len(banned_copy_hits) + len(placeholder_hits)


# ---------------------------------------------------------------------------
# v5: ground-truth checks (byproducts the agent cannot eyeball or improvise)
# ---------------------------------------------------------------------------

def image_dimensions(path: Path) -> tuple[int, int] | None:
    """Parse PNG/JPEG dimensions from header bytes. No third-party deps."""
    try:
        data = path.read_bytes()
    except Exception:
        return None
    # PNG: width/height are big-endian uint32 at offset 16.
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        w = int.from_bytes(data[16:20], "big")
        h = int.from_bytes(data[20:24], "big")
        return (w, h)
    # JPEG: walk markers to a SOF segment.
    if data[:2] == b"\xff\xd8":
        i = 2
        n = len(data)
        while i + 9 < n:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                return (w, h)
            seg_len = int.from_bytes(data[i + 2:i + 4], "big")
            i += 2 + seg_len
    return None


def real_screenshots(root: Path, cfg: dict[str, Any]) -> dict[str, tuple[int, int]]:
    """Return {state: (w,h)} for real image files that meet min dimensions."""
    sc = cfg.get("screenshot_artifacts", {})
    d = root / sc.get("dir", "screenshots")
    found: dict[str, tuple[int, int]] = {}
    if not d.exists():
        return found
    min_w = int(sc.get("min_width", 0))
    min_h = int(sc.get("min_height", 0))
    for state in sc.get("required_states", []):
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            p = d / f"{state}{ext}"
            if p.exists():
                dims = image_dimensions(p)
                # .webp has no cheap header parse here; accept on non-trivial file size.
                if dims and dims[0] >= min_w and dims[1] >= min_h:
                    found[state] = dims
                elif dims is None and p.stat().st_size > 5000:
                    found[state] = (min_w, min_h)
                break
    return found


def check_screenshot_artifacts(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    sc = cfg.get("screenshot_artifacts", {})
    required = list(sc.get("required_states", []))
    if not required:
        return
    found = real_screenshots(root, cfg)
    missing = [s for s in required if s not in found]
    if missing:
        checks.append(Check("screenshot artifacts", "WARN",
                            f"No real image files for: {', '.join(missing)} in {sc.get('dir')}/ "
                            f"(need >= {sc.get('min_width')}x{sc.get('min_height')}). Text mentions do not count."))
    else:
        dims = ", ".join(f"{s} {w}x{h}" for s, (w, h) in found.items())
        checks.append(Check("screenshot artifacts", "PASS", f"Real screenshots present: {dims}."))


def check_reference_dna_provenance(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("reference_dna_provenance", {})
    if not conf.get("required"):
        return
    text = read(root / "project-state/APPROVED_REFERENCE_DNA.md")
    if not text:
        return  # existence already enforced elsewhere
    urls = re.findall(r"https?://[^\s)]+", text)
    markers = [m for m in conf.get("signature_markers", []) if m.lower() in text.lower()]
    fails = []
    if len(urls) < int(conf.get("min_source_urls", 1)):
        fails.append(f"needs >= {conf.get('min_source_urls', 1)} source URL(s); found {len(urls)}")
    if not markers:
        fails.append("missing extraction provenance marker (e.g. 'studied:' / 'source-hash:'); "
                     "DNA must be emitted by a study/extraction step, not eyeballed")
    checks.append(Check("reference DNA provenance", "FAIL" if fails else "PASS",
                        "; ".join(fails) if fails else f"{len(urls)} source URL(s) + provenance marker present."))


def check_blind_review_provenance(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("blind_review_provenance", {})
    if not conf.get("required"):
        return
    text = read(root / "project-state/BLIND_REVIEW_REPORT.md")
    if not text.strip():
        return  # only enforce provenance when a report exists
    markers = [m for m in conf.get("markers", []) if m.lower() in text.lower()]
    if not markers:
        checks.append(Check("blind review provenance", "FAIL",
                            "Blind review report lacks provenance from outside the implementer's context "
                            "(need one of: reviewer-session / transcript-hash / reviewer-initials + reviewed-at)."))
    else:
        checks.append(Check("blind review provenance", "PASS", f"Provenance marker present: {markers[0]}"))


def check_design_brain(checks: list[Check], implementation: Path, cfg: dict[str, Any]) -> int:
    """Enforce DESIGN_BRAIN numeric rules against BUILT output. Returns FAIL count."""
    rules = cfg.get("design_brain_rules", {})
    if not implementation or not implementation.exists():
        return 0
    exts = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte"}
    lh_floor = float(rules.get("line_height_hard_floor", 1.15))
    lh_min = float(rules.get("body_line_height_min", 1.3))
    lh_max = float(rules.get("body_line_height_max", 1.9))
    tt_min = int(rules.get("touch_target_min_px", 44))
    blur_ratio = float(rules.get("shadow_blur_to_offset_max_ratio", 5))
    need_line_len = bool(rules.get("require_prose_line_length_constraint", True))

    lh_floor_hits: list[str] = []
    lh_range_warn: list[str] = []
    touch_hits: list[str] = []
    glow_hits: list[str] = []
    has_line_length = False

    lh_re = re.compile(r"line-height\s*[:=]\s*([0-9]*\.?[0-9]+)\b(?!\s*(?:px|rem|em|%))", re.I)
    lh_tw_re = re.compile(r"leading-\[([0-9]*\.?[0-9]+)\]", re.I)
    shadow_re = re.compile(r"box-shadow\s*:\s*([^;]+);", re.I)
    btn_ctx = re.compile(r"(button|\bbtn\b|role=[\"']button[\"']|<a[\s>])", re.I)
    minh_re = re.compile(r"(?:min-)?height\s*[:=]\s*(\d{1,3})px", re.I)
    tw_h_re = re.compile(r"(?:min-)?h-\[(\d{1,3})px\]", re.I)
    chwidth_re = re.compile(r"max-width\s*:\s*\d+(?:\.\d+)?ch", re.I)
    tw_prose_re = re.compile(r"\b(max-w-prose|max-w-\[?\d+(?:ch|ex)\]?)\b", re.I)

    for path in implementation.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(path.relative_to(implementation))
        for m in list(lh_re.finditer(text)) + list(lh_tw_re.finditer(text)):
            try:
                v = float(m.group(1))
            except ValueError:
                continue
            if v <= lh_floor:
                lh_floor_hits.append(f"{rel}: line-height {v}")
            elif not (lh_min <= v <= lh_max):
                lh_range_warn.append(f"{rel}: line-height {v}")
        if chwidth_re.search(text) or tw_prose_re.search(text):
            has_line_length = True
        # touch targets: heights near button context
        for m in minh_re.finditer(text):
            v = int(m.group(1))
            window = text[max(0, m.start() - 120):m.start() + 120]
            if v < tt_min and btn_ctx.search(window):
                touch_hits.append(f"{rel}: {v}px on interactive el (min {tt_min})")
        for m in tw_h_re.finditer(text):
            v = int(m.group(1))
            window = text[max(0, m.start() - 120):m.start() + 120]
            if v < tt_min and btn_ctx.search(window):
                touch_hits.append(f"{rel}: h-[{v}px] on interactive el (min {tt_min})")
        # fuzzy-glow shadow: blur >> offset (parse leading length tokens; 0 may be unitless)
        for m in shadow_re.finditer(text):
            lengths = []
            for tok in m.group(1).replace(",", " ").split():
                mm = re.fullmatch(r"(-?\d+(?:\.\d+)?)(?:px)?", tok)
                if mm:
                    lengths.append(float(mm.group(1)))
                elif lengths:
                    break  # stop at first non-length token (e.g. rgba/inset/color)
            if len(lengths) >= 3:
                y = abs(lengths[1]); blur = lengths[2]
                if blur > blur_ratio * max(y, 1):
                    glow_hits.append(f"{rel}: shadow blur {blur}px vs y-offset {y}px")

    fails = 0
    if lh_floor_hits:
        checks.append(Check("design-brain line-height", "FAIL",
                            f"Text line-height at/below {lh_floor} (cramped): " + "; ".join(lh_floor_hits[:6])))
        fails += 1
    elif lh_range_warn:
        checks.append(Check("design-brain line-height", "WARN",
                            f"Line-height outside body range [{lh_min},{lh_max}]: " + "; ".join(lh_range_warn[:6])))
    else:
        checks.append(Check("design-brain line-height", "PASS", "No cramped/out-of-range text line-height found."))

    if touch_hits:
        checks.append(Check("design-brain touch targets", "FAIL",
                            f"Interactive elements below {tt_min}px: " + "; ".join(touch_hits[:6])))
        fails += 1
    else:
        checks.append(Check("design-brain touch targets", "PASS", "No obvious sub-target interactive heights."))

    if glow_hits:
        checks.append(Check("design-brain shadow", "WARN",
                            "Fuzzy-glow shadows (blur >> offset): " + "; ".join(glow_hits[:6])))
    else:
        checks.append(Check("design-brain shadow", "PASS", "No fuzzy-glow shadow signature."))

    if need_line_len:
        if has_line_length:
            checks.append(Check("design-brain line-length", "PASS", "Prose line-length constraint present (ch/prose max-width)."))
        else:
            checks.append(Check("design-brain line-length", "WARN",
                                "No prose line-length constraint found (expected a max-width in ch or max-w-prose). "
                                "Full-width body text is a slop signal."))
    return fails


def check_extraction_degraded(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    flag = root / cfg.get("extraction_degraded_flag", "project-state/EXTRACTION_DEGRADED.md")
    if not flag.exists() or not read(flag).strip():
        return
    cap = int(cfg.get("extraction_degraded_premium_cap", 14))
    combined = read(root / "project-state/SCREENSHOT_REVIEW_REPORT.md") + "\n" + read(root / "project-state/BLIND_REVIEW_REPORT.md") + "\n" + read(root / "project-state/LOOP_REPORT.md")
    premium = extract_score(combined, "premium")
    if premium is not None and premium > cap:
        checks.append(Check("extraction-degraded cap", "FAIL",
                            f"EXTRACTION_DEGRADED is set (references lost their real styling) but premium={premium} > cap {cap}. "
                            f"Machine cannot certify premium above {cap} without real reference dress; needs human direction."))
    else:
        checks.append(Check("extraction-degraded cap", "WARN",
                            f"Extraction degraded; premium capped at {cap}. Re-derived dress must be human-approved."))


def check_score_recompute(checks: list[Check], root: Path, cfg: dict[str, Any],
                          objective_violations: int, implementation_scanned: bool) -> None:
    """Cross-check the SELF-REPORTED slop score against machine-counted violations."""
    if not implementation_scanned:
        return
    combined = read(root / "project-state/SCREENSHOT_REVIEW_REPORT.md") + "\n" + read(root / "project-state/BLIND_REVIEW_REPORT.md") + "\n" + read(root / "project-state/LOOP_REPORT.md")
    slop = extract_score(combined, "slop")
    if slop is None:
        return
    # Each hard violation in built code is worth >= ~2 slop points; a near-zero claim with
    # real violations is an inconsistent self-report.
    implied_min = objective_violations * 2
    if slop < implied_min:
        checks.append(Check("score vs code recompute", "FAIL",
                            f"Self-reported slop={slop} contradicts {objective_violations} machine-detected "
                            f"code violation(s) (implies slop >= {implied_min}). Fix the code or the score is not credible."))
    else:
        checks.append(Check("score vs code recompute", "PASS",
                            f"Self-reported slop={slop} consistent with {objective_violations} machine violation(s)."))


def check_grilling_coverage(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("grilling_coverage", {})
    if not conf.get("required"):
        return
    corpus = (read(root / "project-state/DESIGN_TASTE_PROFILE.md") + "\n" +
              read(root / "project-state/PRODUCT_CONTEXT.md") + "\n" +
              read(root / "project-state/ANTI_TARGETS.md")).lower()
    if not corpus.strip():
        return  # existence enforced elsewhere
    missing = [axis for axis, kws in conf.get("axes", {}).items()
               if not any(k.lower() in corpus for k in kws)]
    if missing:
        checks.append(Check("grilling coverage", "FAIL",
                            "Taste profile does not resolve every axis; missing: " + ", ".join(missing) +
                            ". A short 5-question pass is not a grilling."))
    else:
        checks.append(Check("grilling coverage", "PASS", "All taste axes resolved."))

    refs = read(root / "project-state/APPROVED_REFERENCES.md").lower()
    need = int(conf.get("min_references_with_liked", 2))
    markers = [m.lower() for m in conf.get("reference_liked_markers", [])]
    liked = sum(refs.count(m) for m in markers)
    if liked < need:
        checks.append(Check("reference liked-notes", "FAIL",
                            f"Need >= {need} references each stating the ONE thing liked "
                            f"(markers: liked:/borrow:/one thing:); found {liked}."))
    else:
        checks.append(Check("reference liked-notes", "PASS", f"{liked} per-reference 'liked' note(s)."))


def check_extraction_tool(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("extraction_tool", {})
    if not conf.get("required"):
        return
    rel = conf.get("record_file", "project-state/EXTRACTION_TOOL.md")
    text = read(root / rel).lower()
    if not text.strip():
        checks.append(Check("extraction tool setup", "FAIL",
                            f"{rel} is empty. Set up an extraction tool (Playwright/Hallmark/design-extract) "
                            f"and record it here BEFORE extracting DNA. See integrations/setup_extraction.sh."))
        return
    accepted = [t for t in conf.get("accepted_tools", []) if t.lower() in text]
    manual = any(m.lower() in text for m in conf.get("manual_markers", []))
    if not accepted:
        checks.append(Check("extraction tool setup", "FAIL",
                            "No real extraction tool recorded (accepted: playwright/hallmark/design-extract/puppeteer). "
                            "Run integrations/setup_extraction.sh; do not eyeball references."))
    elif manual:
        checks.append(Check("extraction tool setup", "WARN",
                            f"Tool recorded ({accepted[0]}) but manual fallback noted; if CSS was lost set EXTRACTION_DEGRADED."))
    else:
        checks.append(Check("extraction tool setup", "PASS", f"Extraction tool set up: {accepted[0]}."))


def check_organizing_idea(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("organizing_idea", {})
    if not conf.get("required"):
        return
    text = read(root / conf.get("file", "project-state/ORGANIZING_IDEA.md"))
    if not text.strip():
        checks.append(Check("organizing idea", "FAIL",
                            "Missing. State ONE specific structural concept (not 'clean/modern'), e.g. "
                            "'hard left column, nothing centered' or 'oversized serif numerals as section markers'."))
        return
    wc = len(words(text))
    vibes = [v for v in cfg.get("vibe_words", []) if v.lower() in text.lower()]
    if wc < int(conf.get("min_words", 15)):
        checks.append(Check("organizing idea", "FAIL", f"Too thin ({wc} words); describe the concept concretely."))
    elif vibes and wc < 25:
        checks.append(Check("organizing idea", "FAIL", f"Reads as vibe words ({', '.join(vibes[:2])}), not a structural idea."))
    else:
        checks.append(Check("organizing idea", "PASS", "Organizing idea is present and specific."))


def check_real_content(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("real_content", {})
    if not conf.get("required"):
        return
    text = read(root / conf.get("file", "project-state/REAL_CONTENT.md"))
    if not text.strip():
        checks.append(Check("real content", "FAIL",
                            "Missing. Provide REAL copy/products/headings the page is built around not lorem, not placeholder."))
        return
    wc = len(words(text))
    if has_placeholder(text) or "lorem" in text.lower():
        checks.append(Check("real content", "FAIL", "Contains lorem/placeholder. Use actual product copy."))
    elif wc < int(conf.get("min_words", 40)):
        checks.append(Check("real content", "FAIL", f"Too little real copy ({wc} words)."))
    else:
        checks.append(Check("real content", "PASS", f"{wc} words of real content."))


def check_reference_shots(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("reference_shots", {})
    if not conf.get("required"):
        return
    d = root / conf.get("dir", "screenshots/refs")
    imgs = [p for p in d.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")] if d.exists() else []
    if len(imgs) < int(conf.get("min_count", 1)):
        level = "FAIL" if conf.get("hard_fail") else "WARN"
        checks.append(Check("reference shots", level,
                            f"No real reference screenshots in {conf.get('dir')}/. Keeping the pixel anchor "
                            f"(actual shots of liked sites) beats DNA-roles alone at generation time."))
    else:
        checks.append(Check("reference shots", "PASS", f"{len(imgs)} reference screenshot(s) kept as pixel anchor."))


def check_restraint(checks: list[Check], implementation: Path, cfg: dict[str, Any]) -> int:
    conf = cfg.get("restraint", {})
    if not implementation or not implementation.exists():
        return 0
    exts = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte"}
    colors: set[str] = set()
    families: set[str] = set()
    weights: set[str] = set()
    fam_re = re.compile(r"font-family\s*[:=]\s*([^;{}\n]+)", re.I)
    tw_font_re = re.compile(r"font-(?:sans|serif|mono|[a-z]+)?-?\[([^\]]+)\]", re.I)
    wt_re = re.compile(r"font-weight\s*[:=]\s*(\d{3})", re.I)
    tw_wt_re = re.compile(r"font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)\b", re.I)
    for path in implementation.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in RAW_HEX_RE.finditer(text):
            colors.add(m.group(0).lower())
        for m in fam_re.finditer(text):
            first = m.group(1).split(",")[0].strip().strip('"\'').lower()
            if first and "var(" not in first and "inherit" not in first:
                families.add(first)
        for m in wt_re.finditer(text):
            weights.add(m.group(1))
        for m in tw_wt_re.finditer(text):
            weights.add(m.group(1).lower())
    fails = 0
    mc, mf, mw = int(conf.get("max_colors", 10)), int(conf.get("max_font_families", 2)), int(conf.get("max_font_weights", 3))
    if len(colors) > mc:
        checks.append(Check("restraint colors", "WARN", f"{len(colors)} distinct hex colors (> {mc}). Premium = subtraction."))
    if len(families) > mf:
        checks.append(Check("restraint fonts", "FAIL", f"{len(families)} font families (> {mf}): {', '.join(list(families)[:5])}"))
        fails += 1
    else:
        checks.append(Check("restraint fonts", "PASS", f"{len(families)} font families."))
    if len(weights) > mw:
        checks.append(Check("restraint weights", "WARN", f"{len(weights)} font weights (> {mw})."))
    return fails



# ---------------------------------------------------------------------------
# v6: reference-match, variant, and human-taste gates
# ---------------------------------------------------------------------------

def parse_0_5_scores(text: str) -> list[tuple[str, float]]:
    """Parse markdown table or simple Category: 4.2 scores."""
    scores: list[tuple[str, float]] = []
    for line in text.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*([0-5](?:\.\d+)?)\s*\|", line)
        if m and not re.search(r"category|score|---", m.group(1), re.I):
            scores.append((m.group(1).strip(), float(m.group(2))))
            continue
        m = re.match(r"\s*(?:[-*]\s*)?([A-Za-z][A-Za-z0-9\s/()_-]{2,80})\s*:\s*([0-5](?:\.\d+)?)\b", line)
        if m and not re.search(r"average", m.group(1), re.I):
            scores.append((m.group(1).strip(), float(m.group(2))))
    return scores


def check_variant_gate(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("variant_gate", {})
    if not conf.get("required"):
        return
    rel = conf.get("file", "project-state/VARIANT_BOARD.md")
    text = require_file(checks, root, rel, cfg, min_words=int(conf.get("min_words", 120)), min_bullets=6, min_sections=3)
    if not text:
        return
    variants = re.findall(r"(?mi)^\s*#{1,3}\s*(?:Variant|Direction)\s+([A-Z0-9]+)\b", text)
    # Also accept old compact `Direction 1:` style, but headings are preferred.
    if len(variants) < int(conf.get("min_variants", 3)):
        compact = re.findall(r"(?mi)^\s*(?:Variant|Direction)\s+([A-Z0-9]+)\s*:", text)
        variants = variants + compact
    failures = []
    if len(set(variants)) < int(conf.get("min_variants", 3)):
        failures.append(f"needs >= {conf.get('min_variants', 3)} distinct variants; detected {len(set(variants))}")
    markers = [m for m in conf.get("distinctiveness_markers", []) if m.lower() in text.lower()]
    if len(markers) < 2:
        failures.append("does not explicitly evaluate presence/distinctiveness/non-median quality")
    # Require at least one explicit rejected median/default option.
    if not re.search(r"median|safe|default|averaged away|generic", text, re.I):
        failures.append("must name the safe/median fallback to reject")
    checks.append(Check("variant gate", "FAIL" if failures else "PASS",
                        "; ".join(failures) if failures else f"{len(set(variants))} variants with distinctiveness criteria."))


def check_human_taste_gate(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("human_taste_gate", {})
    if not conf.get("required"):
        return
    rel = conf.get("file", "project-state/HUMAN_TASTE_SELECTION.md")
    text = read(root / rel)
    if not text.strip():
        checks.append(Check("human taste gate", "FAIL", f"Missing {rel}. AI may generate options, but a human must choose the direction."))
        return
    low = text.lower()
    status_match = re.search(r"(?mi)^\s*status\s*:\s*([A-Z_]+)\s*$", text)
    current_status = status_match.group(1) if status_match else ""
    approved = current_status in [str(s) for s in conf.get("approved_statuses", [])]
    rejected = current_status in [str(s) for s in conf.get("rejected_statuses", [])]
    failures = []
    if not approved or rejected:
        failures.append(f"final pass requires Status: APPROVED or APPROVED_WITH_NOTES; found {current_status or 'none'}")
    for marker in conf.get("selection_markers", []):
        if marker.lower() not in low:
            failures.append(f"missing selection marker: {marker}")
    if not re.search(r"selected\s+(variant|direction)\s*:\s*\S+", text, re.I):
        failures.append("must name the selected variant/direction")
    checks.append(Check("human taste gate", "FAIL" if failures else "PASS",
                        "; ".join(failures) if failures else "Human taste selection is explicit and approved."))


def check_reference_match_gate(checks: list[Check], root: Path, cfg: dict[str, Any]) -> None:
    conf = cfg.get("reference_match_gate", {})
    if not conf.get("required"):
        return
    rel = conf.get("file", "project-state/VISUAL_REFERENCE_MATCH_REPORT.md")
    text = read(root / rel)
    if not text.strip():
        checks.append(Check("reference-match gate", "FAIL", f"Missing {rel}. Need VLM/human comparison of rendered UI vs references."))
        return
    scores = parse_0_5_scores(text)
    failures = []
    if not scores:
        failures.append("no parseable 0–5 reference-match scores")
    else:
        minimum = float(conf.get("minimum_score", 4))
        avg_min = float(conf.get("minimum_average_score", 4.1))
        low = [(name, score) for name, score in scores if score < minimum]
        avg = sum(score for _, score in scores) / len(scores)
        if low:
            failures.append("scores below threshold: " + ", ".join(f"{name}={score:g}" for name, score in low[:8]))
        if avg < avg_min:
            failures.append(f"average reference-match score {avg:.2f} < {avg_min:.2f}")
    markers = [m for m in conf.get("provenance_markers", []) if m.lower() in text.lower()]
    if not markers:
        failures.append("missing VLM/human reviewer provenance marker")
    if not re.search(r"reference[-\s]screenshot|screenshots/refs|\.png|\.jpe?g|\.webp|figma|https?://", text, re.I):
        failures.append("must identify the visual reference assets used for comparison")
    checks.append(Check("reference-match gate", "FAIL" if failures else "PASS",
                        "; ".join(failures) if failures else f"{len(scores)} scored reference-match categories with provenance."))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Skill/project root containing project-state/")
    parser.add_argument("--implementation", default=None, help="Optional implementation source directory to scan")
    parser.add_argument("--require-final-pass", action="store_true", help="Require FINAL_STATUS=PASS_EXTERNALLY_VALIDATED. Use in pre-commit/CI/predeploy.")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    cfg = load_config(root)
    checks: list[Check] = []
    check_config(checks, cfg)

    if not (root / "project-state").exists():
        checks.append(Check("project-state directory", "FAIL", f"No project-state directory at {root}"))
    else:
        check_required_project_state(checks, root, cfg)
        # [slop-guard disabled] check_grilling_coverage
        # [slop-guard disabled] check_extraction_tool
        # [slop-guard disabled] check_organizing_idea
        # [slop-guard disabled] check_real_content
        # [slop-guard disabled] check_reference_shots
        # [slop-guard disabled] check_variant_gate
        # [slop-guard disabled] check_human_taste_gate
        # [slop-guard disabled] check_reference_match_gate
        check_token_contract(checks, root, cfg)
        check_component_rules(checks, root, cfg)
        check_screenshot_gate(checks, root, cfg)
        check_screenshot_artifacts(checks, root, cfg)          # v5
        # [slop-guard disabled] check_reference_dna_provenance
        # [slop-guard disabled] check_blind_review_provenance
        # [slop-guard disabled] check_scores
        # [slop-guard disabled] check_extraction_degraded
        check_final_status(checks, root, cfg, args.require_final_pass)

    objective_violations = 0
    implementation_scanned = False
    if args.implementation:
        impl_path = Path(args.implementation).resolve()
        objective_violations += scan_implementation(checks, impl_path, cfg)
        # [slop-guard disabled] check_design_brain
        # [slop-guard disabled] check_restraint
        implementation_scanned = True
    if (root / "project-state").exists():
        check_score_recompute(checks, root, cfg, objective_violations, implementation_scanned)  # v5

    failed = [c for c in checks if c.status == "FAIL"]
    warned = [c for c in checks if c.status == "WARN"]
    result = {
        "status": "FAIL" if failed else "PASS",
        "failures": len(failed),
        "warnings": len(warned),
        "checks": [asdict(c) for c in checks],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Validation status: {result['status']} ({len(failed)} failures, {len(warned)} warnings)")
        for c in checks:
            marker = {"PASS":"✓", "WARN":"!", "FAIL":"✗"}.get(c.status, "-")
            print(f"{marker} {c.status:4} {c.name}: {c.detail}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
