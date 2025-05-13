#!/usr/bin/env python3
"""
CLI entrypoint for MIDI Archive processing.
"""
import argparse
from scripts.dedup import deduplicate_midi_keep_unique

# Optional imports; ensure these modules exist or implement them.
try:
    from scripts.spotify_enrichment import enrich_with_spotify
except ImportError:
    enrich_with_spotify = None

try:
    from scripts.midi_analysis import analyze_midi
except ImportError:
    analyze_midi = None


def main():
    parser = argparse.ArgumentParser(
        description="MIDI Archive Colab CLI: deduplicate, enrich, and analyze MIDI files."
    )
    parser.add_argument(
        "--input", "-i",
        default="data/input_midi",
        help="Path to the root MIDI folder"
    )
    parser.add_argument(
        "--dedup", action="store_true", help="Deduplicate MIDI files"
    )
    parser.add_argument(
        "--enrich", action="store_true", help="Enrich metadata via Spotify"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze musical features"
    )
    args = parser.parse_args()

    if args.dedup:
        deduplicate_midi_keep_unique(args.input)
    if args.enrich:
        if enrich_with_spotify:
            enrich_with_spotify(args.input)
        else:
            print("[WARN] spotify_enrichment module not found.")
    if args.analyze:
        if analyze_midi:
            analyze_midi(args.input)
        else:
            print("[WARN] midi_analysis module not found.")

    if not any([args.dedup, args.enrich, args.analyze]):
        parser.print_help()


if __name__ == "__main__":
    main()
