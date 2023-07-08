use phf::phf_map;
#[allow(unused_imports)]
use tracing::{debug, error, info, span, warn, Level, subscriber};
use tracing_subscriber::FmtSubscriber;
use emote::app::{CLI, Modes, CliCommands, TextformType};
use clap::Parser;
use clipboard::{ClipboardContext, ClipboardProvider};

// Include resources
include!(concat!(env!("OUT_DIR"), "/resources.rs"));
#[allow(unused)]

// Types
type DataStore = phf::Map<&'static str, &'static str>;

// Constants
const NO_MAP: DataStore = phf_map!{};

fn get_data_store(textform_type: TextformType) -> &'static DataStore {
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

fn copy_to_clipboard(conts: String) {
    let mut clipboard: ClipboardContext = ClipboardProvider::new().unwrap();
    clipboard.set_contents(conts).expect("Error: Could not copy to clipboard");
}

fn textform(textform_type: TextformType, text: String) -> String {
    let hmap = get_data_store(textform_type);
    let mut output: String = String::with_capacity(text.len());
    
    for char in text.chars() {
        let string_char = String::from(char);
        if let Some(val) = hmap.get(&string_char).cloned() {
            output += val;
        }
    }
    output
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
                    let output = textform(textform_type, text);
                    if (cli.clip) {
                        copy_to_clipboard(output);
                    } else {
                        println!("{}", output);
                    }
                }
                Some(CliCommands::Nato {  }) => {}
                Some(CliCommands::Morse {  }) => {}
                _ => {}
            }
        }
        Some(Modes::File { }) => {}
        Some(Modes::Gui { }) => {}
        _ => {}
    }
}
