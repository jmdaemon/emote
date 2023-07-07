use std::{process::exit, fs};

use emote::app::{CLI, Modes, CliCommands, TextformType};
use clap::Parser;
use indexmap::IndexMap;
use serde_json::Value;

fn get_json_store(textform_type: TextformType) -> String {
    let basename = match textform_type {
        TextformType::Zalgo => "",
        TextformType::Strikethrough => "",
        TextformType::BoldItalicSans => "bold-italic-sans",
        TextformType::BoldItalic => "italic-bold",
        TextformType::BoldSans => "bold-sans",
        TextformType::Bold => "bold",
        TextformType::ItalicSans => "italic-sans",
        TextformType::Italic => "italic",
        TextformType::DoubleStruck => "doublestruck",
        TextformType::Medieval => "medieval",
        TextformType::Monospace => "monospace",
        TextformType::OldEnglish => "old-eng",
        TextformType::Subscript => "subscripts",
        TextformType::Superscript => "superscript"
    };
    basename.to_string() + ".json"
}

fn json_to_hashmap(json: &str) -> Result<IndexMap<String, Value>, serde_json::Error> {
    Ok(serde_json::from_str(json).unwrap())
}

fn main() {
    let cli = CLI::parse();

    if cli.verbose {
        // TODO: Enable logging
    }
    match cli.mode {
        Some(Modes::Cli { command }) => {
            match command {
                Some(CliCommands::Tmote {  }) => {}
                Some(CliCommands::Emoji {  }) => {}
                Some(CliCommands::Textform { textform_type, text } ) => {

                    //let tuple = if let Some(tuple) = command {
                        //tuple
                    //} else {
                        //eprintln!("Error: No command was given.");
                        //// TODO: Show usage
                        //exit(1);
                    //};
                    //let (cmd, text) = tuple;

                    let json_store = get_json_store(textform_type);
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
