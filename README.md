# MIDI Archive Colab

This repo helps you organize, sort, and clean your MIDI files for use in AI training and creative production workflows. Whether you’re triaging thousands of .mid files or building curated datasets, this system gives you a sieve-like process to sort by quality, genre, and metadata tags.

## Features
- MIDI parsing, validation, and error filtering
- Multi-tiered quality sorting (like soil sifting)
- Genre/metadata enrichment using APIs
- JSON export for downstream machine learning

## How to Use

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Place your MIDI files into `data/input_midi`

3. Run the pipeline:

   ```bash
   python main.py --dedup       # deduplicate MIDI files
   python main.py --enrich      # enrich metadata (Spotify)
   python main.py --analyze     # analyze musical features
   python main.py --dedup --enrich --analyze   # run all steps
   ```

4. Results:

   - Duplicates moved to `data/input_midi/trash`, logs under `data/input_midi/logs`
   - Enriched metadata and analysis stored alongside JSON logs
