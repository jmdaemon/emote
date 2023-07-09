use std::{fs::File, io::Write, env, path::Path};

use indexmap::IndexMap;
use serde_json::Value;
use phf::phf_map;

// TODO: Figure out how to const_format the json data path
const RESOURCES_CONTS: phf::Map<&'static str, &'static str> = phf_map! {
    "BOLD_ITALIC_SANS" => include_str!("resources/bold-italic-sans.json"),
    "BOLD_ITALIC" => include_str!("resources/italic-bold.json"),
    "BOLD_SANS" => include_str!("resources/bold-sans.json"),
    "BOLD" => include_str!("resources/bold.json"),
    "ITALIC_SANS" => include_str!("resources/italic-sans.json"),
    "ITALIC" => include_str!("resources/italic.json"),
    "DOUBLESTRUCK" => include_str!("resources/doublestruck.json"),
    "MEDIEVAL" => include_str!("resources/med.json"),
    "MONOSPACE" => include_str!("resources/monospace.json"),
    "OLD_ENGLISH" => include_str!("resources/old-eng.json"),
    "SUBSCRIPT" => include_str!("resources/subscripts.json"),
    "SUPERSCRIPT" => include_str!("resources/superscripts.json"),
};

const NATO_CONTS: &str = include_str!("resources/nato.json");

const RESOURCE_FILE_NAME: &str = "resources.rs";

fn main () {
    // Output to our src directory
    //env::set_var("OUT_DIR", "src");

    // Ensure the resources file can be written to
    let path = Path::new(&env::var("OUT_DIR").unwrap()).join(RESOURCE_FILE_NAME);
    let mut file = File::create(path)
        .expect("Error: File could not be created");
    
    // Disable rust formatting
    file.write_all(b"#[rustfmt::skip]\n").unwrap();

    // Generate textform resources
    for (name, conts) in RESOURCES_CONTS.into_iter() {
        let hmap: IndexMap<String, Value> = serde_json::from_str(conts).unwrap();

        // Create phfmap
        let mut map = phf_codegen::Map::new();
        for (key, val) in hmap.into_iter() {
            let str = val.to_string();
            map.entry(key, &str);
        }
        write!(file,
            "static {}: phf::Map<&'static str, &'static str> = {}",
            name,
            map.build()).unwrap();
        writeln!(file, ";").unwrap();
    }
    writeln!(file).unwrap();

    // Generate nato resource
    //let nato_map: IndexMap<String, String> = serde_json::from_str(NATO_CONTS).unwrap();
    let nato_map: IndexMap<String, Value> = serde_json::from_str(NATO_CONTS).unwrap();

    let mut map = phf_codegen::Map::new();
    for (key, val) in nato_map.iter() {
        let str = val.to_string();
        map.entry(key, &str);
    }
    write!(file,
        "static {}: phf::Map<&'static str, &'static str> = {}",
        "TO_NATO",
        map.build()).unwrap();
    writeln!(file, ";").unwrap();

    let nato_map: IndexMap<String, String> = serde_json::from_str(NATO_CONTS).unwrap();
    let mut map = phf_codegen::Map::new();
    for (key, val) in nato_map.into_iter() {
        //let str = key.to_string().make_ascii_uppercase;
        let str = format!("\"{}\"", key.to_string());
        map.entry(val, &str);

        //let key_str = val.to_string();
        //map.entry(&key_str, key.as_str());

        //let key_str = val.as_str().unwrap();
        //let val_str = key.to_owned();
        //map.entry(key_str, &val_str);

        //let val = val.as_str().unwrap();
        //map.entry(val, key.as_str());
        //map.entry(val.to_string(), key.as_str());
        //let str = val.to_string();
        //map.entry(str, key);
    }
    write!(file,
        "static {}: phf::Map<&'static str, &'static str> = {}",
        "FROM_NATO",
        map.build()).unwrap();
    writeln!(file, ";").unwrap();
}
