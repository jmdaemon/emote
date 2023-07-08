# Emote

All in one application for expressing yourself via unicode text, emojis and text emoticons.

## Table of Contents

1. [Build](#build)
2. [Usage](#usage)
3. [Todo](#todo)

## Build

``` bash
cargo build
```

## Usage

``` bash
# Using the command-line interface
emote cli textform bold "Your text"

# Copy to clipboard
emote -clip cli textform bold "Your text"

# View debug information
emote -v cli textform bold "Your text"

# Using the gui
emote gui

# Using a file prompt
emote file "prompt.txt"
```

## Todo

- Find all missing unicode characters for the current resource files.
- Add unicode character maps for:
    - zalgo
    - strikethrough
    - emoji
- Add mapping for nato phonetic alphabet
- Add mapping for morse?
    - It might be better to create a separate binary for morse instead.
- Implement zalgo with additional settings to adjust

- Create library modules

- Implement file parsing with valid bbcode attributes.
- Implement one window GUI for windows & linux with gtk & native_windows_gui
