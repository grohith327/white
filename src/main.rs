use clap::Parser;
use crossbeam::scope;
use num_cpus;
use rand::Rng;
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use std::process;
use std::sync::{Arc, Mutex};
use walkdir::WalkDir;

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
            || (i < chars.len() - 1 && c == '+' && chars[i + 1] == '=')
        {
            result.push_str(&" ".repeat(rng.random_range(1..=5)));
            result.push(c);
        } else if (c == '=' && chars[i - 1] == '=')
            || (c == '=' && chars[i - 1] == '>')
            || (c == '=' && chars[i - 1] == '<')
            || (c == '=' && chars[i - 1] == '+')
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

fn format_file(path: &str) -> String {
    let mut file_contents = match fs::read_to_string(path) {
        Ok(contents) => contents,
        Err(err) => {
            eprint!("Error reading file {}: {}", path, err);
            process::exit(1);
        }
    };

    file_contents = format_lines(&file_contents);
    file_contents.trim().to_string()
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
            let formatted_content = format_file(&value);
            fs::write(value, formatted_content)?;
        }
        None => {}
    }

    match args.dir {
        Some(ref value) => {
            println!("Formatting files in directory...");
            let python_files: Vec<String> = WalkDir::new(value)
                .into_iter()
                .filter_map(|entry| entry.ok())
                .filter(|entry| entry.path().extension().map_or(false, |ext| ext == "py"))
                .map(|entry| entry.path().display().to_string())
                .collect();

            let num_threads = num_cpus::get();
            let paths = Arc::new(Mutex::new(python_files));

            scope(|s| {
                for _ in 0..num_threads {
                    let paths_clone = Arc::clone(&paths);

                    s.spawn(move |_| {
                        while let Some(s) = paths_clone.lock().unwrap().pop() {
                            let formatted_file = format_file(&s);
                            let path = Path::new(&s);
                            let mut output_file = OpenOptions::new()
                                .create(true)
                                .write(true)
                                .open(path)
                                .unwrap();

                            if let Err(e) = writeln!(output_file, "{}", formatted_file) {
                                eprintln!("Failed to format file: {}", e);
                            }
                        }
                    });
                }
            })
            .unwrap();
        }
        None => {}
    }

    println!("✅ Success");
    Ok(())
}
