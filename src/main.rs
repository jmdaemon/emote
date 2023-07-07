use phf::phf_map;
use tracing::{debug, error, info, span, warn, Level, subscriber};
use tracing_subscriber::FmtSubscriber;
use emote::{app::{CLI, Modes, CliCommands, TextformType}};
use clap::Parser;
use indexmap::IndexMap;
use serde_json::Value;

// Include resources
include!(concat!(env!("OUT_DIR"), "/resources.rs"));

// Types
type DataStore = phf::Map<&'static str, &'static str>;

// Constants
const NO_MAP: DataStore = phf_map!{};

fn get_json_store(textform_type: TextformType) -> &'static DataStore {
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

fn json_to_hashmap(json: &str) -> Result<IndexMap<String, Value>, serde_json::Error> {
    Ok(serde_json::from_str(json).unwrap())
}

fn main() {
    let cli = CLI::parse();

    if cli.verbose {
        let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::TRACE)
        .finish();

        tracing::subscriber::set_global_default(subscriber)
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
                    let hmap = get_json_store(textform_type);

                    let mut output: String = String::with_capacity(text.len());
                    
                    for char in text.chars() {
                        let string_char = String::from(char);
                        if let Some(val) = hmap.get(&string_char).cloned() {
                            output += val;
                        }
                    }

                    println!("{}", output);
                }
                Some(CliCommands::Nato {  }) => {}
                Some(CliCommands::Morse {  }) => {}
                _ => {}
            }

        }
        Some(Modes::Gui { }) => {}
        Some(Modes::File { }) => {}
        _ => {}
    }
}
