#!/usr/bin/env bash
# exit on error
set -o errexit
pip install -r requirements.txt

python parse_all_words_link.py
python main.py