use std::{fs, path::Path, ops::Deref};

use indexmap::IndexMap;
use phf::{phf_map, PhfHash};
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
//type DataStore = phf::Map<&'static str, &'static str>;
//type CustomStore = IndexMap<String, String>;
//type CustomStore<'a> = IndexMap<String, &'a str>;
//type DataStore<'a> = phf::Map<&'a str, &'a str>;
//type CustomStore<'a> = IndexMap<&'a str, &'a str>;
type DataStore = phf::Map<&'static str, &'static str>;
//type CustomStore = IndexMap<String, Value>;
type CustomStore<'a> = IndexMap<&'a str, Value>;

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

//pub trait DataMap<K, V: Clone> {
pub trait DataMap<'a, K> {
    //fn get_val(&self, key: K) -> Option<V>;
    //fn get_val(&self, key: K) -> Option<&'static str>;
    fn get_val(&'a self, key: K) -> Option<&'a str>;
}

//impl DataMap<&str, &'static str> for DataStore {
//impl DataMap<&str> for DataStore {
impl<'a> DataMap<'a, &str> for DataStore {
//impl DataMap<&str, &'static str> for DataStore<'static> {
    fn get_val(&self, key: &str) -> Option<&'a str> {
        //Some(self.get(key).unwrap().deref())
        if let Some(val) = self.get(key) {
            return Some(val);
            //return Some(val.deref());
        } else {
            return Some("".as_ref());
        }
    }
}

//impl DataMap<&str, &'static str> for IndexMap<String, String> {
//impl DataMap<&str, &'static str> for IndexMap<&str, &'static str> {
//impl DataMap<String, &'static str> for IndexMap<String, &'static str> {
//impl DataMap<&str, &'static str> for IndexMap<&str, &'static str> {
//impl DataMap<String> for CustomStore {
impl<'a> DataMap<'a, &str> for CustomStore<'a> {
    //fn get_val(self, key: String) -> Option<&'static str> {
    //fn get_val(&self, key: &str) -> Option<&'static str> {
    //fn get_val(&self, key: String) -> Option<&'static str> {
    fn get_val(&'a self, key: &str) -> Option<&'a str> {
        //if let Some(val) = self.get(&key) {
        //if let Some(val) = self.get(&key) {
        if let Some(val) = self.get(key) {
            //return Some(val.as_ref());
            //return Some(val.deref());
            //return Some(val);
            return val.as_str();
        } else {
            return Some("".as_ref());
        }
    }
}

//impl DataMap<&str, &'static str> for IndexMap<String, String> {
/*
impl DataMap<&str, &'static str> for IndexMap<&str, &'static str> {
    fn get_val(self, key: &str) -> Option<&'static str> {
        if let Some(val) = self.get(key) {
            //return Some(val.as_ref());
            //return Some(val.deref());
            return Some(val);
        } else {
            return Some("".as_ref());
        }
    }
}

impl DataMap<String, &'static str> for IndexMap<String, &'static str> {
    fn get_val(self, key: String) -> Option<&'static str> {
        if let Some(val) = self.get(&key) {
            //return Some(val.as_ref());
            //return Some(val.deref());
            return Some(val);
        } else {
            return Some("".as_ref());
        }
    }
}
*/

//fn convert(hmap: &DataStore, text: String, split: &str, spacer: &str) -> String {
//fn convert<'a, S>(store: &S, text: &'a str, split: &str, spacer: &str) -> String
//where S: DataMap<&'a str, &'a str>

//fn convert<'a, S, K>(store: &S, text: &'a str, split: &str, spacer: &str) -> String
//where S: DataMap<K>

//fn convert<'a, S>(store: &S, text: &'a str, split: &str, spacer: &str) -> String
//where S: DataMap<_>
fn convert<'a>(store: &'a impl DataMap<'a, &'a str>, text: &'a str, split: &str, spacer: &str) -> String
{
    let mut output = String::with_capacity(text.len());
    let text_array = text.split(split);

    for character in text_array {
        //if let Some(val) = store.get_val(character) {
        if let Some(val) = store.get_val(character) {
            output += val;
            output += spacer;
        }
    }
    output
}

/// Parse a custom json file at runtime
fn parse_json_file(conts: &str) -> CustomStore {
    //let hmap: CustomStore = serde_json::from_str(&conts)
    let hmap: CustomStore = serde_json::from_str(conts)
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
                    let output = convert(hmap, &text, BY_CHAR, "");
                    show_output(cli.clip, &output);
                }
                Some(CliCommands::Nato { text, from }) => {
                    
                    let (hmap, split, spacer) = if !from {
                        (&TO_NATO, BY_CHAR, " ")  // From ASCII -> NATO
                    } else {
                        (&FROM_NATO, BY_WORD, " ")// From NATO -> ASCII
                    };
                    let output = convert(hmap, &text, split, spacer);
                    let output = output.trim().to_string();
                    show_output(cli.clip, &output);
                }
                Some(CliCommands::Morse {  }) => {}
                Some(CliCommands::Custom { fpath, text, word}) => {
                    let conts = fs::read_to_string(fpath)
                        .expect("Error: File could not be found");
                    let hmap = parse_json_file(&conts);
                    let split = if word { BY_WORD } else { BY_CHAR };
                    let spacer = "";
                    let output = convert(&hmap, &text, split, spacer);
                    show_output(cli.clip, &output);

                    //let output = convert(&hmap as DataStore, text, BY_CHAR, "");

                    //let mut output: String = String::with_capacity(text.len());
                    
                    //// Separate by whole words
                    //let text_array = if word { text.split(" ") } else { text.split("") };
                    //for character in text_array {
                        //if let Some(val) = hmap.get(character) {
                            //output += val;
                        //}
                    //}
                    //show_output(cli.clip, &output);
                }
                _ => {}
            }
        }
        Some(Modes::File { }) => {}
        Some(Modes::Gui { }) => {}
        _ => {}
    }
}
