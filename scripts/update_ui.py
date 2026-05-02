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

def expand_leading_whitespace(line: str, tab_width: int = 4) -> str:
    """Expand leading tabs to spaces (tab_width spaces per tab) and strip
    trailing whitespace.  Lines that consist entirely of whitespace become
    empty strings.  Internal (non-leading) tabs are left untouched."""
    stripped = line.lstrip('\t')
    n_tabs = len(line) - len(stripped)
    return (' ' * (n_tabs * tab_width) + stripped).rstrip()


def convert_leading_tabs(text: str) -> str:
    """Process every line: expand leading tabs and strip trailing whitespace."""
    out = []
    for part in re.split(r'(\r\n|\r|\n)', text):
        if re.fullmatch(r'\r\n|\r|\n', part):
            out.append(part)
        else:
            out.append(expand_leading_whitespace(part))
    return ''.join(out)


def safe_replace(text: str, old: str, new: str, label: str) -> str:
    """Apply str.replace and warn if the anchor wasn't found."""
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

def apply_changes(text: str) -> str:
    NL = '\r\n'     # file uses Windows line-endings

    # ── Change 2 ─────────────────────────────────────────────────────────────
    # Shift printer button x-positions and append two new systemcraft entries.
    # The whole block is replaced as a unit so only one str.replace() call is
    # needed and the anchor is unambiguous (planet_bulking_x is unique).
    old_printer_block = (
            '                    effectButtonType = { name = "planet_bulking_x"\t\t\t\tspriteType = "GFX_giga_menu_planet_bulking_disabled"\tposition = { x = 290 y = 5 } no_clicksound = yes\t\teffect = "planet_bulking_x" }' + NL
            + '                    effectButtonType = { name = "planet_bulking_x_disabled"\t\tspriteType = "GFX_giga_menu_planet_bulking_enabled"\t\tposition = { x = 290 y = 5 } clicksound = interface\t\teffect = "planet_bulking_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "bulk_matter_x"\t\t\t\t\tspriteType = "GFX_giga_menu_bulk_matter_disabled"\tposition = { x = 320 y = 5 } no_clicksound = yes\t\teffect = "bulk_matter_x" }' + NL
            + '                    effectButtonType = { name = "bulk_matter_x_disabled"\t\tspriteType = "GFX_giga_menu_bulk_matter_enabled"\tposition = { x = 320 y = 5 } clicksound = interface\t\teffect = "bulk_matter_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_x"\t\t\tspriteType = "GFX_giga_menu_moon_printing_disabled"\tposition = { x = 350 y = 5 } no_clicksound = yes\t\teffect = "celestial_printing_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_x_disabled"\tspriteType = "GFX_giga_menu_moon_printing_enabled"\tposition = { x = 350 y = 5 } clicksound = interface\t\teffect = "celestial_printing_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x"\t\t\tspriteType = "GFX_giga_menu_planet_printing_disabled"\tposition = { x = 380 y = 5 } no_clicksound = yes\t\teffect = "celestial_printing_planet_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x_disabled"\tspriteType = "GFX_giga_menu_planet_printing_enabled"\tposition = { x = 380 y = 5 } clicksound = interface\t\teffect = "celestial_printing_planet_x_disabled" }' + NL
            + '                }'
    )
    new_printer_block = (
            '                    effectButtonType = { name = "planet_bulking_x"\t\t\t\tspriteType = "GFX_giga_menu_planet_bulking_disabled"\tposition = { x = 260 y = 5 } no_clicksound = yes\t\teffect = "planet_bulking_x" }' + NL
            + '                    effectButtonType = { name = "planet_bulking_x_disabled"\t\tspriteType = "GFX_giga_menu_planet_bulking_enabled"\t\tposition = { x = 260 y = 5 } clicksound = interface\t\teffect = "planet_bulking_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "bulk_matter_x"\t\t\t\t\tspriteType = "GFX_giga_menu_bulk_matter_disabled"\tposition = { x = 290 y = 5 } no_clicksound = yes\t\teffect = "bulk_matter_x" }' + NL
            + '                    effectButtonType = { name = "bulk_matter_x_disabled"\t\tspriteType = "GFX_giga_menu_bulk_matter_enabled"\tposition = { x = 290 y = 5 } clicksound = interface\t\teffect = "bulk_matter_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_x"\t\t\tspriteType = "GFX_giga_menu_moon_printing_disabled"\tposition = { x = 320 y = 5 } no_clicksound = yes\t\teffect = "celestial_printing_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_x_disabled"\tspriteType = "GFX_giga_menu_moon_printing_enabled"\tposition = { x = 320 y = 5 } clicksound = interface\t\teffect = "celestial_printing_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x"\t\t\tspriteType = "GFX_giga_menu_planet_printing_disabled"\tposition = { x = 350 y = 5 } no_clicksound = yes\t\teffect = "celestial_printing_planet_x" }' + NL
            + '                    effectButtonType = { name = "celestial_printing_planet_x_disabled"\tspriteType = "GFX_giga_menu_planet_printing_enabled"\tposition = { x = 350 y = 5 } clicksound = interface\t\teffect = "celestial_printing_planet_x_disabled" }' + NL
            + NL
            + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_enabled"\t\tspriteType = "GFX_giga_menu_systemcraft_printing_disabled"\tposition = { x = 380 y = 5 } no_clicksound = yes\t\teffect = "celestial_printing_system_x" }' + NL
            + '                    effectButtonType = { name = "stellar_manip_systemcraft_printer_disabled"\tspriteType = "GFX_giga_menu_systemcraft_printing_enabled"\tposition = { x = 380 y = 5 } clicksound = interface\teffect = "celestial_printing_system_x_disabled" }' + NL
            + '                }'
    )
    text = safe_replace(text, old_printer_block, new_printer_block,
                        'printer button x-positions + new systemcraft entries')

    # ── Change 3 ─────────────────────────────────────────────────────────────
    # Insert the "o_systemcraft_options" containerWindowType block.
    # Anchor: the closing "}" of the systemcraft_1/_2 button container,
    # followed by the blank line before "effectButtonType { name = header_terraformers".
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
            + '                    effectButtonType = { name = "stellar_manip_o_systemcraft_enabled" spriteType = "GFX_giga_menu_enabled" position = { x = 380 y = 5 } no_clicksound = yes effect = "stellar_manip_o_systemcraft_enabled" }' + NL
            + '                    effectButtonType = { name = "stellar_manip_o_systemcraft_disabled" spriteType = "GFX_giga_menu_disabled" position = { x = 380 y = 5 } clicksound = interface effect = "stellar_manip_o_systemcraft_disabled" }' + NL
            + NL
            + '                }' + NL
            + NL
    )

    # Anchor: unique pair of lines at the end of the systemcraft button container
    systemcraft_anchor_old = (
            '                    effectButtonType = { name = "systemcraft_1_disabled" spriteType = "GFX_giga_menu_1_disabled" position = { x = 230 y = 5 } clicksound = interface effect = "giga_systemcraft_1_disabled" }' + NL
            + '                }' + NL
            + NL
            + '                effectButtonType = {'
    )
    systemcraft_anchor_new = (
            '                    effectButtonType = { name = "systemcraft_1_disabled" spriteType = "GFX_giga_menu_1_disabled" position = { x = 230 y = 5 } clicksound = interface effect = "giga_systemcraft_1_disabled" }' + NL
            + '                }' + NL
            + o_systemcraft_block
            + '                effectButtonType = {'
    )
    text = safe_replace(text, systemcraft_anchor_old, systemcraft_anchor_new,
                        'insert o_systemcraft_options block')

    # ── Change 4 ─────────────────────────────────────────────────────────────
    # Shift y-positions of the six containers that follow the new insertion
    # by +80 px.  Each is identified by its unique "name" line.

    y_shifts = [
        # (unique name in file,  old y,   new y,   type)
        ('header_terraformers',         -175,   -95,  'effectButtonType',     432),
        ('terraform_toxic_options',      -55,    25,  'containerWindowType',  450),
        ('terraform_barren_options',     -15,    65,  'containerWindowType',  450),
        ('geothermal_options',            25,   105,  'containerWindowType',  450),
        ('glue_options',                  65,   145,  'containerWindowType',  450),
        ('terraform_gasgiant_options',   105,   185,  'containerWindowType',  450),
        ('compressor_options',           145,   225,  'containerWindowType',  450),
    ]

    for name, old_y, new_y, _, x in y_shifts:
        old_pos = f'name = "{name}"' + NL + f'                    position = {{ x = {x} y = {old_y} }}'
        new_pos = f'name = "{name}"' + NL + f'                    position = {{ x = {x} y = {new_y} }}'
        text = safe_replace(text, old_pos, new_pos,
                            f'y-shift for {name} ({old_y} → {new_y})')

    # ── Change 5 ─────────────────────────────────────────────────────────────
    # Insert the "giga_menu_stellar_manipulator" containerWindowType block
    # after the closing "}" of the compressor_options container.
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
            + '                    effectButtonType = { name = "stellar_manipulator_enabled" spriteType = "GFX_giga_menu_enabled" position = { x = 380 y = 5 } no_clicksound = yes effect = "stellar_manip_manipulator_enabled" }' + NL
            + '                    effectButtonType = { name = "stellar_manipulator_disabled" spriteType = "GFX_giga_menu_disabled" position = { x = 380 y = 5 } clicksound = interface effect = "stellar_manip_manipulator_disabled" }' + NL
            + NL
            + '                }' + NL
    )

    # Anchor: unique closing sequence of the compressor_options container
    compressor_anchor_old = (
            '                    effectButtonType = { name = "compressor_1_disabled" spriteType = "GFX_giga_menu_1_disabled" position = { x = 230 y = 5 } clicksound = interface effect = "giga_compressor_1_disabled" }' + NL
            + '                }' + NL
            + '            }' + NL
            + NL
            + '            instantTextBoxType={'
    )
    compressor_anchor_new = (
            '                    effectButtonType = { name = "compressor_1_disabled" spriteType = "GFX_giga_menu_1_disabled" position = { x = 230 y = 5 } clicksound = interface effect = "giga_compressor_1_disabled" }' + NL
            + '                }' + NL
            + stellar_manip_block
            + '            }' + NL
            + NL
            + '            instantTextBoxType={'
    )
    text = safe_replace(text, compressor_anchor_old, compressor_anchor_new,
                        'insert giga_menu_stellar_manipulator block')

    return text


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    gigas_folder = Path.cwd().parent / "Gigastructures-Live-Branch"
    gigas_ui = gigas_folder / "interface" / "giga_gui_main_menu.gui"
    stellar_manip_ui = Path.cwd() / "Gigas-Stellar-Manipulation" / "interface" / "z_giga_gui_main_menu.gui"

    src = sys.argv[1] if len(sys.argv) > 1 else gigas_ui
    dst = sys.argv[2] if len(sys.argv) > 2 else stellar_manip_ui

    print(f"Reading source: {src}")
    with open(src, 'r', newline='', encoding='utf-8') as f:
        text = f.read()

    print("Converting leading tabs to spaces ...")
    text = convert_leading_tabs(text)

    print("Applying changes ...")
    text = apply_changes(text)

    print(f"Writing output: {dst}")
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        f.write(text)

    print("Done.")


if __name__ == '__main__':
    main()