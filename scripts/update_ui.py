#!/usr/bin/env python3
"""
patch_giga_gui.py
─────────────────
Applies the hardcoded differences from z_giga_gui_main_menu.gui onto a
(possibly updated) giga_gui_main_menu.gui, writing the result to
z_giga_gui_main_menu.gui.

Usage:
    python patch_giga_gui.py [SOURCE] [OUTPUT]

Defaults:
    SOURCE  = giga_gui_main_menu.gui
    OUTPUT  = z_giga_gui_main_menu.gui

Changes encoded in this script
───────────────────────────────
1. Indentation: leading tabs → 4-space indentation throughout.

2. Stellar-manipulation button row — shift x-positions left by 30 px each
   to make room for the new systemcraft-printer entry, then add it:
     planet_bulking_x / _disabled        : x 290 → 260
     bulk_matter_x / _disabled           : x 320 → 290
     celestial_printing_x / _disabled    : x 350 → 320
     celestial_printing_planet_x / _dis  : x 380 → 350
     [NEW] stellar_manip_systemcraft_printer_enabled/_disabled at x 380

3. Insert new containerWindowType block "o_systemcraft_options"
   (position y -135) after the closing "}" of the existing
   systemcraft_1/_2 buttons container.

4. Shift y-positions of the six terraformer/geothermal/compressor
   container blocks that follow the new insertion by +80 px each:
     header_terraformers          : y -175 → -95
     terraform_toxic_options      : y  -55 →  25
     terraform_barren_options     : y  -15 →  65
     geothermal_options           : y   25 → 105
     glue_options                 : y   65 → 145
     terraform_gasgiant_options   : y  105 → 185
     compressor_options           : y  145 → 225

5. Insert new containerWindowType block "giga_menu_stellar_manipulator"
   (position y 265) after the closing "}" of the compressor_options
   container.
"""

import sys
import re
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def detect_line_ending(text: str) -> str:
    """Detect the dominant line ending in the file."""
    crlf = text.count('\r\n')
    lf   = text.count('\n') - crlf
    return '\r\n' if crlf >= lf else '\n'


def expand_leading_whitespace(line: str, tab_width: int = 4) -> str:
    stripped = line.lstrip('\t')
    n_tabs = len(line) - len(stripped)
    return (' ' * (n_tabs * tab_width) + stripped).rstrip()


def convert_leading_tabs(text: str) -> str:
    out = []
    for part in re.split(r'(\r\n|\r|\n)', text):
        if re.fullmatch(r'\r\n|\r|\n', part):
            out.append(part)
        else:
            out.append(expand_leading_whitespace(part))
    return ''.join(out)


def safe_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        print(f"  WARNING: anchor not found for change '{label}' – skipping.")
        return text
    if count > 1:
        print(f"  WARNING: anchor for '{label}' found {count} times – "
              f"replacing first occurrence only.")
        return text.replace(old, new, 1)
    return text.replace(old, new)


# ─────────────────────────────────────────────────────────────────────────────
# All hardcoded changes
# ─────────────────────────────────────────────────────────────────────────────

def apply_changes(text: str, NL: str) -> str:

    # ── Change 2 ─────────────────────────────────────────────────────────────
    old_printer_block = (
            '                    effectButtonType = { name = "planet_bulking_x"                     spriteType = "GFX_giga_menu_planet_bulking_disabled"  position = { x = 290 y = 5 } no_clicksound = yes      effect = "planet_bulking_x" }' + NL
            + '                    effectButtonType = { name = "planet_bulking_x_disabled"          spriteType = "GFX_giga_menu_planet_bulking_enabled"   position = { x = 290 y = 5 } clicksound = interface     effect = "planet_bulking_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "bulk_matter_x"                      spriteType = "GFX_giga_menu_bulk_matter_disabled"     position = { x = 320 y = 5 } no_clicksound = yes      effect = "bulk_matter_x" }' + NL
            + '                    effectButtonType = { name = "bulk_matter_x_disabled"             spriteType = "GFX_giga_menu_bulk_matter_enabled"      position = { x = 320 y = 5 } clicksound = interface     effect = "bulk_matter_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_x"               spriteType = "GFX_giga_menu_moon_printing_disabled"   position = { x = 350 y = 5 } no_clicksound = yes      effect = "celestial_printing_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_x_disabled"      spriteType = "GFX_giga_menu_moon_printing_enabled"    position = { x = 350 y = 5 } clicksound = interface     effect = "celestial_printing_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x"            spriteType = "GFX_giga_menu_planet_printing_disabled" position = { x = 380 y = 5 } no_clicksound = yes  effect = "celestial_printing_planet_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x_disabled"   spriteType = "GFX_giga_menu_planet_printing_enabled"  position = { x = 380 y = 5 } clicksound = interface effect = "celestial_printing_planet_x_disabled" }' + NL
            + '                }'
    )
    new_printer_block = (
            '                    effectButtonType = { name = "planet_bulking_x"                     spriteType = "GFX_giga_menu_planet_bulking_disabled"  position = { x = 260 y = 5 } no_clicksound = yes      effect = "planet_bulking_x" }' + NL
            + '                    effectButtonType = { name = "planet_bulking_x_disabled"          spriteType = "GFX_giga_menu_planet_bulking_enabled"   position = { x = 260 y = 5 } clicksound = interface     effect = "planet_bulking_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "bulk_matter_x"                      spriteType = "GFX_giga_menu_bulk_matter_disabled"     position = { x = 290 y = 5 } no_clicksound = yes      effect = "bulk_matter_x" }' + NL
            + '                    effectButtonType = { name = "bulk_matter_x_disabled"             spriteType = "GFX_giga_menu_bulk_matter_enabled"      position = { x = 290 y = 5 } clicksound = interface     effect = "bulk_matter_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_x"               spriteType = "GFX_giga_menu_moon_printing_disabled"   position = { x = 320 y = 5 } no_clicksound = yes      effect = "celestial_printing_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_x_disabled"      spriteType = "GFX_giga_menu_moon_printing_enabled"    position = { x = 320 y = 5 } clicksound = interface     effect = "celestial_printing_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x"            spriteType = "GFX_giga_menu_planet_printing_disabled" position = { x = 350 y = 5 } no_clicksound = yes  effect = "celestial_printing_planet_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x_disabled"   spriteType = "GFX_giga_menu_planet_printing_enabled"  position = { x = 350 y = 5 } clicksound = interface effect = "celestial_printing_planet_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_enabled"  spriteType = "GFX_giga_menu_systemcraft_printing_disabled" position = { x = 380 y = 5 } no_clicksound = yes  effect = "celestial_printing_system_x" }' + NL
            + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_disabled" spriteType = "GFX_giga_menu_systemcraft_printing_enabled"  position = { x = 380 y = 5 } clicksound = interface effect = "celestial_printing_system_x_disabled" }' + NL
            + '                }'
    )

    # ── Change 3 ─────────────────────────────────────────────────────────────
    o_systemcraft_block = (
            NL
            + '                ####################################' + NL
            + '                ### o class systemcraft ############' + NL
            + '                ####################################' + NL
            + NL
            + '                containerWindowType = {' + NL
            + '                    name = "o_systemcraft_options"' + NL
            + '                    position = { x = 450 y = -135 }' + NL
            + '                    size = { width = 410 height = 34 }' + NL
            + '                    orientation = upper_left' + NL
            + NL
            + '                    effectButtonType = {' + NL
            + '                        name = "background_o_systemcraft"' + NL
            + '                        spriteType = "GFX_giga_menu_button_bg"' + NL
            + '                        position = { x = 0 y = 0 }' + NL
            + '                        format = left' + NL
            + '                        no_clicksound = yes' + NL
            + '                        borderSize = { x = 10 y = 0 }' + NL
            + '                        font = "cg_16b"' + NL
            + '                        text = "giga_menu_name_o_systemcraft"' + NL
            + '                        effect = "stellar_manip_o_systemcraft_tt"' + NL
            + '                    }' + NL
            + NL
            + '                    effectButtonType = { name = "stellar_manip_o_systemcraft_enabled"  spriteType = "GFX_giga_menu_enabled"  position = { x = 380 y = 5 } no_clicksound = yes  effect = "stellar_manip_o_systemcraft_enabled" }' + NL
            + '                    effectButtonType = { name = "stellar_manip_o_systemcraft_disabled" spriteType = "GFX_giga_menu_disabled" position = { x = 380 y = 5 } clicksound = interface effect = "stellar_manip_o_systemcraft_disabled" }' + NL
            + NL
            + '                }' + NL
            + NL
    )

    # ── Change 5 ─────────────────────────────────────────────────────────────
    stellar_manip_block = (
            NL
            + '                ####################################' + NL
            + '                ### stellar manipulator ############' + NL
            + '                ####################################' + NL
            + '                containerWindowType = {' + NL
            + '                    name = "giga_menu_stellar_manipulator"' + NL
            + '                    position = { x = 450 y = 265 }' + NL
            + '                    size = { width = 410 height = 34 }' + NL
            + '                    orientation = upper_left' + NL
            + NL
            + '                    effectButtonType = {' + NL
            + '                        name = "background_stellar_manipulator"' + NL
            + '                        spriteType = "GFX_giga_menu_button_bg"' + NL
            + '                        position = { x = 0 y = 0 }' + NL
            + '                        format = left' + NL
            + '                        no_clicksound = yes' + NL
            + '                        borderSize = { x = 10 y = 0 }' + NL
            + '                        font = "cg_16b"' + NL
            + '                        text = "giga_menu_name_stellar_manipulator"' + NL
            + '                        effect = "stellar_manip_stellar_manipulator_tt"' + NL
            + '                    }' + NL
            + NL
            + '                    effectButtonType = { name = "stellar_manipulator_enabled"  spriteType = "GFX_giga_menu_enabled"  position = { x = 380 y = 5 } no_clicksound = yes  effect = "stellar_manip_manipulator_enabled" }' + NL
            + '                    effectButtonType = { name = "stellar_manipulator_disabled" spriteType = "GFX_giga_menu_disabled" position = { x = 380 y = 5 } clicksound = interface effect = "stellar_manip_manipulator_disabled" }' + NL
            + NL
            + '                }' + NL
    )

    # ── Apply Change 2 ───────────────────────────────────────────────────────
    # We use a regex approach here so we don't need to match exact whitespace
    # between tokens on each effectButtonType line — only the name= and x= values matter.

    def replace_printer_buttons(t):
        # Match the block of 8 effectButtonType lines for the printer buttons
        # by anchoring on the unique name strings and capturing the x= values to replace.
        pattern = re.compile(
            r'([ \t]+effectButtonType\s*=\s*\{[^}]*name\s*=\s*"planet_bulking_x"[^}]*x\s*=\s*)290(\s[^}]*\}' + NL + r')'
                                                                                                                    r'([ \t]+effectButtonType\s*=\s*\{[^}]*name\s*=\s*"planet_bulking_x_disabled"[^}]*x\s*=\s*)290(\s[^}]*\}' + NL + r')'
        )
        # Rather than a complex regex across 8 lines, do targeted per-name replacements:
        replacements = [
            ('"planet_bulking_x"',              'x = 290', 'x = 260'),
            ('"planet_bulking_x_disabled"',      'x = 290', 'x = 260'),
            ('"bulk_matter_x"',                  'x = 320', 'x = 290'),
            ('"bulk_matter_x_disabled"',         'x = 320', 'x = 290'),
            ('"celestial_printing_x"',           'x = 350', 'x = 320'),
            ('"celestial_printing_x_disabled"',  'x = 350', 'x = 320'),
            ('"celestial_printing_planet_x"',         'x = 380', 'x = 350'),
            ('"celestial_printing_planet_x_disabled"','x = 380', 'x = 350'),
        ]
        for name, old_x, new_x in replacements:
            # Find the line containing this name and replace only the first x= on that line
            line_pat = re.compile(r'([ \t]+effectButtonType\s*=\s*\{[^' + '\n' + r']*' + re.escape(name) + r'[^' + '\n' + r']*?)' + re.escape(old_x) + r'([^' + '\n' + r']*\})')
            new_t, n = line_pat.subn(r'\g<1>' + new_x + r'\g<2>', t, count=1)
            if n == 0:
                print(f"  WARNING: could not shift x for {name}")
            else:
                t = new_t

        # Now append the two new systemcraft printer buttons after celestial_printing_planet_x_disabled line
        insert_after = re.compile(
            r'([ \t]+effectButtonType\s*=\s*\{[^' + '\n' + r']*"celestial_printing_planet_x_disabled"[^' + '\n' + r']*\})'
        )
        new_buttons = (
                NL
                + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_enabled"  spriteType = "GFX_giga_menu_systemcraft_printing_disabled" position = { x = 380 y = 5 } no_clicksound = yes  effect = "celestial_printing_system_x" }'
                + NL
                + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_disabled" spriteType = "GFX_giga_menu_systemcraft_printing_enabled"  position = { x = 380 y = 5 } clicksound = interface effect = "celestial_printing_system_x_disabled" }'
        )
        new_t, n = insert_after.subn(r'\g<1>' + new_buttons, t, count=1)
        if n == 0:
            print("  WARNING: could not insert new systemcraft printer buttons")
        else:
            t = new_t
        return t

    text = replace_printer_buttons(text)

    # ── Apply Change 3 ───────────────────────────────────────────────────────
    # Insert o_systemcraft_options after the line containing "giga_systemcraft_1_disabled"
    # followed by the container closing brace.
    systemcraft_pat = re.compile(
        r'([ \t]+effectButtonType\s*=\s*\{[^' + '\n' + r']*"systemcraft_1_disabled"[^' + '\n' + r']*\}' + NL
        + r'[ \t]*\}' + NL + r')'
    )
    new_t, n = systemcraft_pat.subn(r'\g<1>' + o_systemcraft_block, text, count=1)
    if n == 0:
        print("  WARNING: anchor not found for 'insert o_systemcraft_options block' – skipping.")
    else:
        text = new_t
        print("  OK: inserted o_systemcraft_options block")

    # ── Apply Change 4 ───────────────────────────────────────────────────────
    y_shifts = [
        ('header_terraformers',         -175,  -95),
        ('terraform_toxic_options',      -55,   25),
        ('terraform_barren_options',     -15,   65),
        ('geothermal_options',            25,  105),
        ('glue_options',                  65,  145),
        ('terraform_gasgiant_options',   105,  185),
        ('compressor_options',           145,  225),
    ]
    for name, old_y, new_y in y_shifts:
        pat = re.compile(
            r'(name\s*=\s*"' + re.escape(name) + r'"[^' + '\n' + r']*' + NL
            + r'[^' + '\n' + r']*?y\s*=\s*)' + str(old_y) + r'(\s*\})'
        )
        new_t, n = pat.subn(r'\g<1>' + str(new_y) + r'\g<2>', text, count=1)
        if n == 0:
            print(f"  WARNING: anchor not found for y-shift '{name}' ({old_y} → {new_y}) – skipping.")
        else:
            text = new_t
            print(f"  OK: y-shift {name} ({old_y} → {new_y})")

    # ── Apply Change 5 ───────────────────────────────────────────────────────
    compressor_pat = re.compile(
        r'([ \t]+effectButtonType\s*=\s*\{[^' + '\n' + r']*"compressor_1_disabled"[^' + '\n' + r']*\}' + NL
        + r'[ \t]*\}' + NL + r')'
    )
    new_t, n = compressor_pat.subn(r'\g<1>' + stellar_manip_block, text, count=1)
    if n == 0:
        print("  WARNING: anchor not found for 'insert giga_menu_stellar_manipulator block' – skipping.")
    else:
        text = new_t
        print("  OK: inserted giga_menu_stellar_manipulator block")

    return text


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    gigas_folder = Path("/home/Tempest1273/.local/share/Paradox Interactive/Stellaris/mod/Gigastructures Dev/Gigastructures")
    gigas_ui = gigas_folder / "interface" / "giga_gui_main_menu.gui"
    stellar_manip_ui = Path.cwd().parent / "Gigas-Stellar-Manipulation" / "interface" / "z_giga_gui_main_menu.gui"

    src = Path(sys.argv[1]) if len(sys.argv) > 1 else gigas_ui
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else stellar_manip_ui

    print(f"Reading source: {src}")
    with open(src, 'r', newline='', encoding='utf-8') as f:
        text = f.read()

    NL = detect_line_ending(text)
    print(f"Detected line endings: {'CRLF' if NL == chr(13)+chr(10) else 'LF'}")

    print("Converting leading tabs to spaces ...")
    text = convert_leading_tabs(text)

    print("Applying changes ...")
    text = apply_changes(text, NL)

    print(f"Writing output: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        f.write(text)

    print("Done.")


if __name__ == '__main__':
    main()