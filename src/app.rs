use clap::{Parser, arg, Subcommand, ValueEnum};

const PROGRAM_DESCRIPTION: &str = "";

#[derive(Parser)]
#[command(author, version, about, long_about = PROGRAM_DESCRIPTION)]
pub struct CLI {
    #[arg(short, long, default_value_t = false, help = "Toggle verbose information")]
    pub verbose: bool,

    #[arg(short, long, default_value_t = false, help = "Copy to clipboard")]
    pub clip: bool,

    #[command(subcommand)]
    pub mode: Option<Modes>,
}

#[derive(Copy, Clone, Debug, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
pub enum TextformType {
    Zalgo,
    Strikethrough,
    BoldItalicSans,
    BoldItalic,
    BoldSans,
    Bold,
    ItalicSans,
    Italic,
    DoubleStruck,
    Medieval,
    Monospace,
    OldEnglish,
    Subscript,
    Superscript
}

#[derive(Subcommand)]
pub enum CliCommands {
    Tmote {},
    Emoji {},
    Textform {
        #[arg(value_enum)]
        textform_type: TextformType,

        #[arg(value_name = "TEXT")]
        text: String,
    },
    Nato {},
    Morse {},
}

#[derive(Subcommand)]
pub enum Modes {
    #[command(about = "Run in cli mode")]
    Cli {
        #[command(subcommand)]
        command: Option<CliCommands>,
    },
    #[command(about = "Run in file mode")]
    File {
    },
    #[command(about = "Run in gui mode")]
    Gui {
    },
}
