import os
import json
import hashlib
from pathlib import Path
from mido import MidiFile
from tqdm import tqdm
from shutil import move

def get_midi_hash(file_path):
    """Generate a hash based on MIDI note events (ignores file name)."""
    try:
        mid = MidiFile(file_path)
        note_data = []
        for track in mid.tracks:
            for msg in track:
                if msg.type in ['note_on', 'note_off']:
                    note_data.append((msg.type, msg.note, msg.velocity, msg.time))
        note_str = str(note_data).encode('utf-8')
        return hashlib.md5(note_str).hexdigest()
    except Exception as e:
        print(f"[ERROR] Skipping {file_path}: {e}")
        return None

def deduplicate_midi_keep_unique(midi_root_path):
    """Scan directory, deduplicate MIDI/KAR files by content hash, move duplicates to trash, and log JSON metadata."""
    midi_root = Path(midi_root_path)
    trash_dir = midi_root / "trash"
    trash_dir.mkdir(exist_ok=True)

    json_output_dir = midi_root / "logs"
    json_output_dir.mkdir(exist_ok=True)

    seen_hashes = {}
    duplicate_log = []

    # Match .mid and .kar files
    all_midi_files = list(midi_root.rglob("*.mid")) + list(midi_root.rglob("*.kar"))

    for midi_path in tqdm(all_midi_files, desc="Scanning MIDI and KAR files"):
        if trash_dir in midi_path.parents or json_output_dir in midi_path.parents:
            continue  # Skip trash or logs

        midi_hash = get_midi_hash(midi_path)
        if not midi_hash:
            continue

        if midi_hash not in seen_hashes:
            seen_hashes[midi_hash] = {
                "hash": midi_hash,
                "original_filenames": [midi_path.name],
                "status": "unique",
                "source_folder": str(midi_path.parent)
            }

            json_path = json_output_dir / f"{midi_path.stem}.json"
            with open(json_path, 'w') as f:
                json.dump(seen_hashes[midi_hash], f, indent=2)

        else:
            seen_hashes[midi_hash]["original_filenames"].append(midi_path.name)
            duplicate_log.append({
                "duplicate": midi_path.name,
                "original": seen_hashes[midi_hash]["original_filenames"][0],
                "folder": str(midi_path.parent)
            })

            move(str(midi_path), trash_dir / midi_path.name)
            print(f"[MOVED TO TRASH] {midi_path.name}")

    # Write summary duplicate log
    dup_log_path = json_output_dir / "duplicate_log.json"
    with open(dup_log_path, 'w') as f:
        json.dump(duplicate_log, f, indent=2)

    print(f"\nDone. Scanned: {len(all_midi_files)} files")
    print(f"Unique: {len(seen_hashes)} | Duplicates moved: {len(duplicate_log)}")
    print(f"Logs stored in: {json_output_dir}")
