import librosa
import numpy as np
import sys

def mp3_to_qsr(mp3_path, qsr_path):
    print(f"Wczytywanie {mp3_path}...")
    # 1. Wczytanie pliku MP3 i sprowadzenie go do mono
    y, sr = librosa.load(mp3_path, sr=22050, mono=True)

    hop_length = 512
    # Czas trwania jednej klatki analizy w ms (~23 ms)
    frame_time_ms = int((hop_length / sr) * 1000)

    print("Analizowanie częstotliwości (Pitch Tracking)...")
    # 2. Wykrywanie nuty wiodącej za pomocą algorytmu pYIN
    f0, voiced_flag, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'), # ~65 Hz
        fmax=librosa.note_to_hz('C7'), # ~2093 Hz
        sr=sr,
        hop_length=hop_length
    )

    # 3. Obliczenie głośności (RMS)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    max_rms = np.max(rms) if np.max(rms) > 0 else 1.0

    notes = []
    current_freq = 0
    current_dur = 0
    current_vol = 0

    # 4. Łączenie klatek w dłuższą sekwencję nut
    for i in range(len(f0)):
        # Jeśli nuta została wykryta, bierzemy jej Hz, w przeciwnym razie 0 (cisza)
        freq = int(f0[i]) if (not np.isnan(f0[i]) and voiced_flag[i]) else 0
        vol = int((rms[i] / max_rms) * 255) if freq > 0 else 0

        # Zaokrąglenie do 5 Hz, żeby drobne wahania głosu nie cięły nuty
        freq = round(freq / 5) * 5 if freq > 0 else 0

        if i == 0:
            current_freq = freq
            current_dur = frame_time_ms
            current_vol = vol
        else:
            # Jeśli nuta i głośność są podobne do poprzedniej -> wydłużamy czas trwania
            if freq == current_freq and abs(vol - current_vol) <= 25:
                current_dur += frame_time_ms
            else:
                if current_dur > 0:
                    notes.append((current_freq, current_dur, current_vol))
                current_freq = freq
                current_dur = frame_time_ms
                current_vol = vol

    if current_dur > 0:
        notes.append((current_freq, current_dur, current_vol))

    # 5. Zapis do pliku .qsr w Twoim formacie
    with open(qsr_path, 'w') as f:
        for freq, dur, vol in notes:
            freq = min(max(freq, 0), 22050)
            dur = min(max(dur, 0), 65535)
            vol = min(max(vol, 0), 255)
            # Format: 00440.00100.255
            f.write(f"{freq:05d}.{dur:05d}.{vol:03d}\n")

    print(f"Sukces! Wygenerowano {len(notes)} nut w pliku {qsr_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Użycie: python mp3_to_qsr.py plik_wejscia.mp3 wyjscie.qsr")
    else:
        mp3_to_qsr(sys.argv[1], sys.argv[2])
