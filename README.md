# ccwc tool

### Usage

```
$ ./ccwc --help
Usage: ccwc [OPTIONS] [FILE_PATH]...

  A Python version of the wc utility, which displays the number of lines,
  words, and bytes contained in each input text file, or standard input (if no
  file is specified) to the standard output. An Exception is raised if non-
  text files are provided.

Options:
  -c, --should-count-bytes  Count the number of bytes in a text file.
  -l, --should-count-lines  Count the number of lines in a text file.
  -w, --should-count-words  Count the number of words in a text file.
  -m, --should-count-chars  Count the number of characters in a text file.
  --help                    Show this message and exit

```

### System Requirements

`ccwc` requires Python, version 3.12

It also requires the `click` library to be installed. Install it using `pip install click`.

### Project Structure

```
.
├── ccwc                          - the wc implementation.
├── tester.py                     - tests comparing wc output with ccwc output
├── test.txt                      - the file used in ccwc tool assessment
└── test_big.txt                  - a larger copy of the file used in ccwc tool assessment.

```

### Testing

The test file can be run from the command line:

```
python3 tester.py
```

### Thanks

- Thanks to John Crickett for creating these [fun challenges](https://codingchallenges.fyi/challenges/intro).
- Thanks to Marek Jakub for a nice template of the [README](https://github.com/marek-jakub/ccwc_tool?tab=readme-ov-file#ccwc-tool).
