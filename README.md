# RAK FAKTA AI Control Center — MVP v0.2

Dashboard Streamlit dengan integrasi **Ollama AI lokal** untuk membuat riset sejarah awal dan draft naskah dokumenter. Tidak memerlukan API key berbayar.

## 1. Persiapan
- Windows 10/11
- Python 3.10 atau lebih baru
- Ollama: https://ollama.com/download

## 2. Unduh model AI
Buka Command Prompt / PowerShell setelah Ollama terpasang, lalu jalankan:

```bash
ollama pull llama3.2
```

Model lain yang bisa dicoba: `qwen2.5` atau `gemma3`. Pastikan RAM dan ruang penyimpanan cukup.

## 3. Jalankan dashboard
Ekstrak folder proyek, buka terminal di folder tersebut, lalu jalankan:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Dashboard biasanya terbuka di `http://localhost:8501`.

## 4. Hubungkan AI
Ollama biasanya berjalan di `http://localhost:11434`. Di panel kiri dashboard:
- Isi Ollama URL: `http://localhost:11434`
- Isi nama model: `llama3.2`
- Klik **Tes koneksi AI**
- Buka tab **Research AI** atau **Script AI** lalu jalankan.

Jika memakai model berbeda, masukkan nama persis sesuai hasil `ollama list`.

## Catatan penting
- Research Agent membuat **riset awal dari pengetahuan model**, bukan penelusuran web langsung. Verifikasi semua klaim dengan buku, jurnal, arsip, dan sumber primer.
- Model lokal tidak otomatis mengakses internet.
- Aplikasi ini belum membuat video, audio/voice-over, thumbnail, atau mengunggah video ke YouTube.
- Untuk memakai dari VPS atau komputer lain, URL Ollama perlu dikonfigurasi secara aman; jangan membuka port Ollama ke internet tanpa perlindungan.
