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
}
