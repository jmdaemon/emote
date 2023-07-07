use std::{process::exit, fs};

use emote::app::{CLI, Modes, CliCommands, TextformCommands};
use clap::Parser;
use indexmap::IndexMap;
use serde_json::Value;

fn get_json_store(cmd: TextformCommands) -> String {
    let str = match cmd {
        TextformCommands::Zalgo {  } => "",
        TextformCommands::Strikethrough {  } => "",
        TextformCommands::BoldItalicSans {  } => "bold-italic-sans",
        TextformCommands::BoldItalic {  } => "italic-bold",
        TextformCommands::BoldSans {  } => "bold-sans",
        TextformCommands::Bold {  } => "bold",
        TextformCommands::ItalicSans {  } => "italic-sans",
        TextformCommands::Italic {  } => "italic",
        TextformCommands::DoubleStruck {  } => "doublestruck",
        TextformCommands::Medieval {  } => "medieval",
        TextformCommands::Monospace {  } => "monospace",
        TextformCommands::OldEnglish {  } => "old-eng",
        TextformCommands::Subscript {  } => "subscripts",
        TextformCommands::Superscript {  } => "superscript"
    };
    str.to_string() + ".json"
}

//fn json_to_hashmap(json: &str, keys: Vec<&str>) -> Result<IndexMap<String, Value>, serde_json::Error> {
fn json_to_hashmap(json: &str) -> Result<IndexMap<String, Value>, serde_json::Error> {
    Ok(serde_json::from_str(json).unwrap())
    //let mut lookup: IndexMap<String, Value> = serde_json::from_str(json).unwrap();
    //let mut map = IndexMap::new();
    //for key in keys {
        //let (k, v) = lookup.remove_entry (key).unwrap();
        //map.insert(k, v);
    //}
    
    //Ok(map)
}

fn main() {
    let cli = CLI::parse();

    if cli.verbose {
        // Enable logging
    }
    match cli.mode {
        Some(Modes::Cli { command }) => {
            match command {
                Some(CliCommands::Tmote {  }) => {}
                Some(CliCommands::Emoji {  }) => {}
                Some(CliCommands::Textform { command, text }) => {
                    let cmd = if let Some(command) = command {
                        command
                    } else {
                        eprintln!("Error: No command was given.");
                        // TODO: Show usage
                        exit(1);
                    };
                    /*
                    match command {
                        Some(TextformCommands::Zalgo {  }) => {}
                        Some(TextformCommands::Strikethrough {  }) => {}
                        Some(TextformCommands::BoldItalicSans {  }) => {}
                        Some(TextformCommands::BoldItalic {  }) => {}
                        Some(TextformCommands::BoldSans {  }) => {}
                        Some(TextformCommands::Bold {  }) => {}
                        Some(TextformCommands::ItalicSans {  }) => {}
                        Some(TextformCommands::Italic {  }) => {}
                        Some(TextformCommands::DoubleStruck {  }) => {}
                        Some(TextformCommands::Medieval {  }) => {}
                        Some(TextformCommands::Monospace {  }) => {}
                        Some(TextformCommands::OldEnglish {  }) => {}
                        Some(TextformCommands::Subscript {  }) => {}
                        Some(TextformCommands::Superscript {  }) => {}
                        _ => {}
                    }
                    */
                    let json_store = get_json_store(cmd);
                    let json_file = format!("resources/{}", json_store);
                    let json_file_conts = fs::read_to_string(json_file).expect("Error: File could not be found");
                    let hmap = json_to_hashmap(&json_file_conts).expect("Error: Could not parse json file");

                    let mut output: String = String::with_capacity(text.len());
                    
                    for char in text.chars() {
                        let string_char = String::from(char);
                        if let Some(val) = hmap.get(&string_char) {
                            output += val.as_str().unwrap();
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
