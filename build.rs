//use const_format::formatcp;

//const EXTENSION: &str = "json";
//const RESOURCE_DIR: &str = "resources";
//const BOLD_ITALIC_SANS_PATH: &str = formatcp!("{}.{}", "bold-italic-sans", EXTENSION);

//const BOLD_ITALIC_SANS_PATH: &str = formatcp!("{}/{}.{}", RESOURCE_DIR, "bold-italic-sans", EXTENSION);

//const BOLD_ITALIC_SANS_CONTS: &str = include_str!("resources/bold-italic-sans.json");
//const BOLD_ITALIC_SANS_CONTS: &str = include_str!(BOLD_ITALIC_SANS_PATH);



//const BOLD_ITALIC_SANS_CONTS: &str = include_str!("resources/bold-italic-sans.json");
//const BOLD_ITALIC_CONTS: &str = include_str!("resources/italic-bold.json");
//const BOLD_SANS_CONTS: &str = include_str!("resources/bold-sans.json");
//const BOLD_CONTS: &str = include_str!("resources/bold.json");
//const ITALIC_SANS_CONTS: &str = include_str!("resources/italic-sans.json");
//const ITALIC_CONTS: &str = include_str!("resources/italic.json");
//const DOUBLESTRUCK_CONTS: &str = include_str!("resources/bold-italic-sans.json");
//const MEDIEVAL_CONTS: &str = include_str!("resources/med.json");
//const MONOSPACE_CONTS: &str = include_str!("resources/monospace.json");
//const OLD_ENGLISH_CONTS: &str = include_str!("resources/old-eng.json");
//const SUBSCRIPT_CONTS: &str = include_str!("resources/subscripts.json");
//const SUPERSCRIPT_CONTS: &str = include_str!("resources/superscripts.json");

use std::{fs::File, io::Write, env, path::Path};

use indexmap::IndexMap;
use serde_json::Value;
use phf::phf_map;

//const RESOURCES_CONTS: &[&str] = &[
    //include_str!("resources/bold-italic-sans.json"),
    //include_str!("resources/italic-bold.json"),
    //include_str!("resources/bold-sans.json"),
    //include_str!("resources/bold.json"),
    //include_str!("resources/italic-sans.json"),
    //include_str!("resources/italic.json"),
    //include_str!("resources/bold-italic-sans.json"),
    //include_str!("resources/med.json"),
    //include_str!("resources/monospace.json"),
    //include_str!("resources/old-eng.json"),
    //include_str!("resources/subscripts.json"),
    //include_str!("resources/superscripts.json"),
//];

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
const RESOURCE_FILE_OUTPUT: &str = "src/resources.rs";

fn main () {
    //let BOLD_ITALIC_SANS_CONTS: &str = include_str!(BOLD_ITALIC_SANS_PATH);
    let path = Path::new(&env::var("OUT_DIR").unwrap()).join(RESOURCE_FILE_NAME);

    let mut file = File::create(path)
        .expect("Error: File could not be created");
    
    file.write_all(b"#[rustfmt::skip]\n").unwrap();
    
    for (name, conts) in RESOURCES_CONTS.into_iter() {
        let hmap: IndexMap<String, Value> = serde_json::from_str(conts).unwrap();

        // Create the map
        //let line = format!("pub static {}: &[(&str, &[&str])] = &[\n", name);
        //file.write_all(line.as_bytes()).unwrap();

        //let line = format!("static {}: phf::Map<&'static str, &'static str> = {{}}", name);
        //let line = format!("static {}: phf::Map<&'static str, &'static str> = {}", name);
        //let line = format!("static {}: phf::Map<String, String> = ", name);
        //write!(file, "{}", line).unwrap();

        //let fmt: &'static str = "static {}: phf::Map<&'static str, &'static str> = {}";

        // Create hashmap
        let mut map = phf_codegen::Map::new();
        for (key, val) in hmap.into_iter() {
            let str = val.to_string();
            map.entry(key, &str);
        }
        write!(file,
            "static {}: phf::Map<&'static str, &'static str> = {}",
            name,
            map.build()).unwrap();


            
            //"{}", line).unwrap();

        //write!(file, map.build()).unwrap();
        write!(file, ";\n").unwrap();
    }

        /*
        for (key, val) in hmap.into_iter() {
            // Write key
            file.write_all(b"    (\"").unwrap();
            file.write_all(key.as_bytes()).unwrap();
            file.write_all(b"\", &[").unwrap();

            file.write_all(b", ").unwrap();
            // Write value
            //for v in val {
            //if ext != &exts[0] {
            //}

            file.write_all(b"\"").unwrap();
            file.write_all(val.as_str().unwrap().as_bytes()).unwrap();
            file.write_all(b"\"").unwrap();
            }
            //file.write_all("").unwrap();
        file.write_all(b"]),\n").unwrap();
    }
        */
}
