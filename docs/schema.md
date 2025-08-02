# Schema for Terminal Style Tool Kit - TSTK

## Overview

The tstk file format is a json file that mirrors the colors
settings that Putty stores in the registry, with some additions.

It is essentially a color scheme/theme/palette.

## Example

See sample.tstk for an example.

sample.tstk is a minor modification to the default builtin Putty theme (which is a dark theme).


## Schema

JSON file.

### Metadata

Example content take from sample.tstk

    "scheme-name": "Default_fixed_blue-dark",
    "scheme-author": "Putty authors and Dag Wieers",
    "scheme-slug": "Default_fixed_blue-dark",
    "scheme-comment":  "Blue changes from Dag Wieers - see https://web.archive.org/web/20191231204120/http://dag.wiee.rs/blog/content/improving-putty-settings-on-windows",

Then `scheme-comment1-9` comment fields:

    "scheme-comment1": "",
    "scheme-comment2": "",
    "scheme-comment3": "",
    "scheme-comment4": "",
    "scheme-comment5": "",
    "scheme-comment6": "",
    "scheme-comment7": "",
    "scheme-comment8": "",
    "scheme-comment9": "",

### Colors / Colours

`Colour0-hex` to `Colour21-hex` - matching Putty color numbers. Colors are 24-bit RGB hex values, for example `ffffff` and `000000`.
If hex are missing, `Colour0` to `Colour21` are looked for used instead, colors are 24-bit decimal hex values, for example `255,255,255` and `0,0,0`.
When generating tstk files hex is recommended (and what Terminal Style Tool Kit will emit) but decimal support is present for easy copy/pasting of values.

Each color entry may optionally have:

  * comment
  * note
  * hex

I.e. may see:

    "Colour1-comment": "",
    "Colour1-note": "",
    "Colour1": "255,255,255",
    "Colour1-hex": "ffffff",

