# Plagiarism Checker

This app shows how similar is a specified docx file to other docx files in a specified directory.

## Overview

This tool converts docx files to txt format and assesses their similarity using Levenshtein distance, so it focuses solely on text content.
To speed up the process, the script also caches converted files; it does it by hashing docx files' metadata and storing corresponding txt content in a json file.

## Getting started

```bash
git clone https://github.com/atlantis-11/plagiarism-checker
```

## Installing dependencies

Ensure you have Python3.x installed, and install the required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Go to plagiarism-checker directory and run:
```bash
python3 main.py file_to_check.docx dir_to_check/
```
