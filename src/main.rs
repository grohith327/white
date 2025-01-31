use clap::Parser;
use rand::Rng;
use std::fs;
use std::process;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    file: Option<String>,

    #[clap(short, long)]
    dir: Option<String>,
}

fn add_random_spacing(input: &str) -> String {
    let mut rng = rand::rng();
    let mut result = String::new();
    let mut inside_parantheses = false;
    let chars: Vec<char> = input.chars().collect();

    for i in 0..chars.len() {
        let c = chars[i];
        if c == '(' {
            inside_parantheses = true;
            result.push(c);
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
        } else if c == ')' {
            inside_parantheses = false;
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
            result.push(c);
        } else if (i < chars.len() - 1 && c == '=' && chars[i + 1] == '=')
            || (i < chars.len() - 1 && c == '<' && chars[i + 1] == '=')
            || (i < chars.len() - 1 && c == '>' && chars[i + 1] == '=')
        {
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
            result.push(c);
        } else if (c == '=' && chars[i - 1] == '=')
            || (c == '=' && chars[i - 1] == '>')
            || (c == '=' && chars[i - 1] == '<')
        {
            result.push(c);
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
        } else if inside_parantheses && c == ',' || c == '=' || c == '<' || c == '>' {
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
            result.push(c);
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
        } else {
            result.push(c);
        }
    }

    result
}

fn update_spacing(input: &str) -> String {
    let space_count = input.chars().take_while(|&c| c.is_whitespace()).count();
    let updated_whitespace = " ".repeat(space_count / 2);
    format!("{}{}", updated_whitespace, input.trim_start())
}

fn format_lines(input: &str) -> String {
    let mut inside_docstring = false;

    input
        .lines()
        .filter(|line| !line.is_empty())
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
        .map(|line| add_random_spacing(line))
        .map(|line| update_spacing(&line))
        .collect::<Vec<_>>()
        .join("\n")
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();

    if args.dir.is_none() && args.file.is_none() {
        eprint!("❌ Error: provide a file or directory to proceed");
        process::exit(1);
    }

    if !args.dir.is_none() && !args.file.is_none() {
        eprint!("❌ Error: provide either a directory or a file. Not both.");
        process::exit(1);
    }

    match args.file {
        Some(ref value) => {
            println!("Formating file...");

            let mut file_contents = match fs::read_to_string(&value) {
                Ok(contents) => contents,
                Err(err) => {
                    eprint!("Error reading file {}: {}", value, err);
                    process::exit(1);
                }
            };

            file_contents = format_lines(&file_contents);
            file_contents = file_contents.trim().to_string();
            fs::write(value, file_contents)?;
        }
        None => {}
    }

    println!("✅ Success");
    Ok(())
}
