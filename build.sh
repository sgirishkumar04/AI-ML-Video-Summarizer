#!/bin/bash

# Exit on any error
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run a Python script to download the model
python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"