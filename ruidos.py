import os
import random
import numpy as np
import soundfile as sf
import pyroomacoustics as pra
import resampy


# Caminhos
noise_dir = "data/ruidos"
output_dir = "data/corrupted_dataset"

# Lista de SNRs que queremos gerar
snr_list = [0, 5, 10]

# Coleta arquivos de ruído
noise_files = [os.path.join(dp, f) for dp, _, fn in os.walk(noise_dir) for f in fn if f.endswith('.wav')]

# Função para normalizar RMS
def adjust_noise_snr(clean, noise, snr_db):
    """Ajusta o ruído para que tenha a SNR desejada em relação ao áudio limpo"""
    rms_clean = np.sqrt(np.mean(clean**2))
    rms_noise = np.sqrt(np.mean(noise**2))
    if rms_noise == 0:
        return np.zeros_like(clean)

    desired_rms_noise = rms_clean / (10**(snr_db / 20))
    scaling_factor = desired_rms_noise / rms_noise
    return noise * scaling_factor

# Percorre todos os arquivos de ruído
for noise_path in noise_files:
    rel_path = os.path.relpath(noise_path, noise_dir)

    # Carrega o áudio limpo
    clean_audio, fs = sf.read("data/audio_limpo.wav")
    if clean_audio.ndim > 1:
        clean_audio = clean_audio[:, 0]  # Usa um canal se for estéreo
    if fs != 16000:
        clean_audio = resampy.resample(clean_audio, fs, 16000)
        fs = 16000

    # Carrega o ruído
    noise_audio, fs_noise = sf.read(noise_path)
    if noise_audio.ndim > 1:
        noise_audio = noise_audio[:, 0]
    if fs_noise != 16000:
        noise_audio = resampy.resample(noise_audio, fs_noise, 16000)
        fs_noise = 16000

    # Ajusta tamanho do ruído
    if len(noise_audio) < len(clean_audio):
        factor = (len(clean_audio) // len(noise_audio)) + 1
        noise_audio = np.tile(noise_audio, factor)
    noise_audio = noise_audio[:len(clean_audio)]

    # Para cada valor de SNR, gera uma versão
    for snr_db in snr_list:
        noise_adj = adjust_noise_snr(clean_audio, noise_audio, snr_db)

        # ---------- (1) Mix seco ----------
        mixed_linear = clean_audio + noise_adj
        out_linear = os.path.join(output_dir, f"SNR_{snr_db}dB", "linear", rel_path)
        os.makedirs(os.path.dirname(out_linear), exist_ok=True)
        sf.write(out_linear, mixed_linear, samplerate=fs)
        print(f"Arquivo seco salvo: {out_linear}")

        # ---------- (2) Mix reverberado ----------
        width = random.randint(5, 15)
        depth = random.randint(5, 15)
        height = random.randint(2, 5)
        room_dim = [width, depth, height]
        absorption = random.uniform(0.1, 0.6)

        room = pra.ShoeBox(
            room_dim,
            fs=fs,
            absorption=absorption,
            max_order=15
        )

        # Posição do locutor
        speaker_pos = np.array([
            random.uniform(1, width - 1),
            random.uniform(1, depth - 1),
            random.uniform(1, height - 1)
        ])
        room.add_source(speaker_pos, signal=clean_audio)

        # Posição do ruído
        noise_pos = np.array([
            random.uniform(1, width - 1),
            random.uniform(1, depth - 1),
            random.uniform(1, height - 1)
        ])
        room.add_source(noise_pos, signal=noise_adj)

        # Microfone no centro
        mic_pos = np.array([[width/2], [depth/2], [height/2]])
        room.add_microphone_array(pra.MicrophoneArray(mic_pos, room.fs))
        
        # Simula reverberação
        room.simulate()
        mixed_reverb = room.mic_array.signals[0]

        out_reverb = os.path.join(output_dir, f"SNR_{snr_db}dB", "reverb", rel_path)
        os.makedirs(os.path.dirname(out_reverb), exist_ok=True)
        sf.write(out_reverb, mixed_reverb, samplerate=fs)
        print(f"Arquivo reverberado salvo: {out_reverb}")

