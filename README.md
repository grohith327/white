## White - A Python Formatter

<p style="color: gray;">Like black but does the opposite</p>

A simple python code formatter. By using it, you retain control over the smallest formatting details. In exchange, it may introduce unpredictability and can subject you to constant reminders and warnings about style issues. You may find yourself spending more time adjusting formatting preferences instead of focusing on other tasks. White increases the complexity of code reviews by generating larger diffs that may distract from the primary logic and require more review time to account for formatting changes.

> Yep, I just negated the readme on [Black](https://github.com/psf/black). Also, if you want to get a glimpse of the formatter result, check file [bst.py](samples/ds/bst.py)

### Features

- Strip all comments and docstrings - who reads that anyway!
- Add random spacing throughout the code - if you add this to your commit hook, you can generate large diffs for each PR

What's coming:

- Compress mulitple lines of code into a single line

## Installation

For now, you can only build from source. Please ensure you have `cargo` installed and run the following command:

```bash
cargo install --path .
```

## Usage

Format a single file

```bash
white -f samples/avl_tree.py
```

Format all files in a package

```bash
white -d samples/ds
```
