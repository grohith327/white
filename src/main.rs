use clap::Parser;
use std::fs;
use std::process;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    file: String,
}

fn remove_comments(input: &str) -> String {
    let mut inside_docstring = false;

    input
        .lines()
        .filter(|line| {
            let trimmed = line.trim();
            if trimmed.starts_with("\"\"\"") {
                if trimmed.ends_with("\"\"\"") && trimmed != "\"\"\"" {
                    return false;
                }
                inside_docstring = !inside_docstring;
                return false;
            }
            !inside_docstring && !trimmed.starts_with("#")
        })
        .map(|line| {
            line.split_once("#")
                .map_or(line, |(before, _)| before)
                .trim_end()
        })
        .collect::<Vec<_>>()
        .join("\n")
}

fn main() {
    let args = Args::parse();

    let mut file_contents = match fs::read_to_string(&args.file) {
        Ok(contents) => {
            println!("Succesfully loaded file contents");
            contents
        }
        Err(err) => {
            eprint!("Error reading file {}: {}", args.file, err);
            process::exit(1);
        }
    };

    file_contents = remove_comments(&file_contents);
    println!("File contents:\n{}", file_contents.trim());
}
