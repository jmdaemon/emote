use std::{fs, path::Path};

use indexmap::IndexMap;
use phf::phf_map;
#[allow(unused_imports)]
use tracing::{debug, error, info, span, warn, Level, subscriber};
use tracing_subscriber::FmtSubscriber;
use emote::app::{CLI, Modes, CliCommands, TextformType};
use clap::Parser;
use clipboard::ClipboardProvider;
use clipboard_ext::x11_fork::ClipboardContext;
use serde_json::Value;

// Include resources
include!(concat!(env!("OUT_DIR"), "/resources.rs"));
#[allow(unused)]

// Types
type DataStore = phf::Map<&'static str, &'static str>;
type CustomStore = IndexMap<String, Value>;

// Constants
const NO_MAP: DataStore = phf_map!{};
const BY_CHAR: &str = "";
const BY_WORD: &str = " ";

fn get_data_store<'a>(textform_type: TextformType) -> &'a DataStore {
    match textform_type {
        TextformType::Zalgo => &NO_MAP,
        TextformType::Strikethrough => &NO_MAP,
        TextformType::BoldItalicSans => &BOLD_ITALIC_SANS,
        TextformType::BoldItalic => &BOLD_ITALIC,
        TextformType::BoldSans => &BOLD_SANS,
        TextformType::Bold => &BOLD,
        TextformType::ItalicSans => &ITALIC_SANS,
        TextformType::Italic => &ITALIC,
        TextformType::DoubleStruck => &DOUBLESTRUCK,
        TextformType::Medieval => &MEDIEVAL,
        TextformType::Monospace => &MONOSPACE,
        TextformType::OldEnglish => &OLD_ENGLISH,
        TextformType::Subscript => &SUBSCRIPT,
        TextformType::Superscript => &SUPERSCRIPT,
    }
}

// NOTE: When we copy the contents to our clipboard, we need to fork our process and keep it running
// in the background so we can actually paste the contents of the clipboard
fn copy_to_clipboard(conts: &str) {
    ClipboardContext::new().unwrap()
        .set_contents(conts.into()).unwrap();
}

fn convert(hmap: &DataStore, text: String, split: &str, spacer: &str) -> String {
    let mut output = String::with_capacity(text.len());
    let text_array = text.split(split);

    for character in text_array {
        if let Some(val) = hmap.get(character) {
            output += val;
            output += spacer;
        }
    }
    output
}

/// Parse a custom json file at runtime
fn parse_json_file(fpath: &Path) -> CustomStore {
    let conts = fs::read_to_string(fpath)
        .expect("Error: File could not be found");
    let hmap: CustomStore = serde_json::from_str(&conts)
        .expect("Error: Could not parse json file");
    hmap
}

fn show_output(clip: bool, output: &str) {
    if clip {
        copy_to_clipboard(output);
    } else {
        println!("{}", output);
    }
}

fn main() {
    let cli = CLI::parse();

    if cli.verbose {
        let subscriber = FmtSubscriber::builder()
            .with_max_level(Level::TRACE)
            .finish();

        subscriber::set_global_default(subscriber)
            .expect("Setting global default subscriber failed");
    }
    info!("Settings: ");
    info!("\tVerbose: {}", cli.verbose);
    match cli.mode {
        Some(Modes::Cli { command }) => {
            match command {
                Some(CliCommands::Tmote {  }) => {}
                Some(CliCommands::Emoji {  }) => {}
                Some(CliCommands::Textform { textform_type, text } ) => {
                    let hmap = get_data_store(textform_type);
                    let output = convert(hmap, text, BY_CHAR, "");
                    show_output(cli.clip, &output);
                }
                Some(CliCommands::Nato { text, from }) => {
                    
                    let (hmap, split, spacer) = if !from {
                        (&TO_NATO, BY_CHAR, " ")  // From ASCII -> NATO
                    } else {
                        (&FROM_NATO, BY_WORD, " ")// From NATO -> ASCII
                    };
                    let output = convert(hmap, text, split, spacer);
                    let output = output.trim().to_string();
                    show_output(cli.clip, &output);
                }
                Some(CliCommands::Morse {  }) => {}
                Some(CliCommands::Custom { fpath, text, word}) => {
                    let hmap = parse_json_file(&fpath);
                    let mut output: String = String::with_capacity(text.len());
                    
                    // Separate by whole words
                    let text_array = if word { text.split(" ") } else { text.split("") };
                    for character in text_array {
                        if let Some(val) = hmap.get(character) {
                            output += val.as_str().unwrap();
                        }
                    }
                    show_output(cli.clip, &output);
                }
                _ => {}
            }
        }
        Some(Modes::File { }) => {}
        Some(Modes::Gui { }) => {}
        _ => {}
    }
}
