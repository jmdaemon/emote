#![feature(type_alias_impl_trait)]

use std::{fs::File, io::Write, env, path::Path, hash::{Hasher, BuildHasher}};

use indexmap::{IndexMap, map::{Iter, IntoIter}};
use serde_json::Value;
use phf::phf_map;

use itertools::*;

// Constants

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

// Types
type DataStore = IndexMap<String, String>;

// Functions
fn quote(s: impl Into<String>) -> String {
    format!("\"{}\"", s.into())
}

fn write_map(file: &mut File, name: impl Into<String>, map: &phf_codegen::Map<String>) {
    write!(file,
        "static {}: phf::Map<&'static str, &'static str> = {}",
        name.into(),
        map.build()).unwrap();
    writeln!(file, ";").unwrap();
}

fn generate_resource<'a, I>(file: &mut File, name: &str, it: I)
where
    I: Iterator<Item = (&'a String, &'a String)>
{
    let mut map = phf_codegen::Map::new();
    for (key, val) in it {
        map.entry(key.to_owned(), &quote(val));
    }
    write_map(file, name, &map);
}

pub trait HashMapReverseMapExt<K,V> {
    fn rev_map(self) -> Self;
}

impl HashMapReverseMapExt<String, String> for IndexMap<String, String> {
    fn rev_map(self) -> Self {
        self.into_iter()
            .map( |(key, val)| (val, key))
            .collect()
    }
}

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
        let hmap: DataStore = serde_json::from_str(conts).unwrap();
        generate_resource(&mut file, name, hmap.iter());
    }
    writeln!(file).unwrap();

    // Generate nato resource
    let nato_map: DataStore = serde_json::from_str(NATO_CONTS).unwrap();
    generate_resource(&mut file, "TO_NATO", nato_map.iter());
    generate_resource(&mut file, "FROM_NATO", nato_map.rev_map().iter());
}
