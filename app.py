import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title='RAK FAKTA AI Control Center', page_icon='🧠', layout='wide')

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family: Inter, sans-serif;}
.stApp {background: radial-gradient(circle at 50% 0%, #102638 0%, #07111d 45%, #050a12 100%); color:#e8f2ff;}
.block-container {padding-top:1.4rem; max-width:1500px;}
[data-testid="stMetric"] {background:linear-gradient(145deg,#102334,#0a1724); border:1px solid #1b4055; padding:16px; border-radius:14px;}
.panel {background:linear-gradient(145deg,rgba(16,37,54,.96),rgba(7,19,31,.96)); border:1px solid #1b4055; border-radius:16px; padding:18px; min-height:120px;}
.agent {border:1px solid #1e4356; border-radius:12px; padding:13px; background:#0b1b29; margin-bottom:9px;}
.muted {color:#8ca8ba;font-size:12px;}
.globe {height:290px; border-radius:18px; border:1px solid #15506a; background:radial-gradient(circle at 50% 45%,#164b63 0%,#0b2638 32%,#071522 68%,#06101a 100%); display:flex; align-items:center; justify-content:center; text-align:center; box-shadow: inset 0 0 55px #0b5a7650,0 0 28px #00d5ff18;}
.globe .earth {font-size:100px; filter:drop-shadow(0 0 20px #00d9ff);}
div.stButton>button {background:linear-gradient(90deg,#00a8c9,#087e9d); color:white; border:0; border-radius:10px; font-weight:700;}
</style>
''', unsafe_allow_html=True)

if 'logs' not in st.session_state:
    st.session_state.logs = ['Control Center berhasil dimuat.', 'AI lokal siap dikonfigurasi.']
if 'research_result' not in st.session_state:
    st.session_state.research_result = ''
if 'script_result' not in st.session_state:
    st.session_state.script_result = ''

# Configuration can be overridden with environment variables or Streamlit secrets.
def get_config(key, default):
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

with st.sidebar:
    st.markdown('## ⚙️ AI Connection')
    ollama_url = st.text_input('Ollama URL', value=get_config('OLLAMA_URL', 'http://localhost:11434')).rstrip('/')
    model = st.text_input('Nama model', value=get_config('OLLAMA_MODEL', 'llama3.2'))
    st.caption('Contoh model: llama3.2, qwen2.5, gemma3')
    check = st.button('Tes koneksi AI')
    if check:
        try:
            resp = requests.get(f'{ollama_url}/api/tags', timeout=3)
            resp.raise_for_status()
            installed = [m.get('name', '') for m in resp.json().get('models', [])]
            st.success('Ollama terhubung.')
            st.write('Model tersedia:', ', '.join(installed) if installed else 'Belum ada model yang diunduh.')
            if installed and not any(x == model or x.startswith(model + ':') for x in installed):
                st.warning(f'Model {model} belum terlihat di daftar model lokal.')
        except Exception as e:
            st.error('Belum dapat terhubung ke Ollama. Pastikan Ollama sudah berjalan.')
            st.caption(str(e))
    st.divider()
    st.caption('Mode lokal: pemrosesan dilakukan oleh Ollama di komputer yang menjalankan aplikasi. Tidak membutuhkan API key berbayar.')


def ask_ollama(prompt, system_prompt):
    response = requests.post(
        f'{ollama_url}/api/chat',
        json={
            'model': model,
            'stream': False,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ],
            'options': {'temperature': 0.35},
        },
        timeout=240,
    )
    response.raise_for_status()
    data = response.json()
    return data.get('message', {}).get('content', '').strip()

st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap'><div><div class='muted'>RAK FAKTA • CREATOR INTELLIGENCE SYSTEM</div><h1 style='margin:0;color:#eaf7ff'>🧠 AI CONTROL CENTER</h1><div class='muted'>Mengungkap Sejarah, Menjaga Fakta</div></div><div style='text-align:right'><span style='color:#39e6a5'>● DASHBOARD ONLINE</span><br><span class='muted'>MVP v0.2 • Local AI integration</span></div></div>", unsafe_allow_html=True)
st.divider()

m1,m2,m3,m4 = st.columns(4)
m1.metric('AI AGENTS', '05', 'Research & Script aktifkan via Ollama')
m2.metric('PROYEK AKTIF', '01', 'RAK FAKTA')
m3.metric('WORKFLOW', '02', 'Research + Script')
m4.metric('MODEL AI', model, 'Ollama lokal')

left, center, right = st.columns([1.05,1.65,1.05], gap='medium')
with left:
    st.markdown('### 🤖 Agent Monitor')
    agents=[('Research Agent','Ollama lokal','🔎'),('Script Agent','Ollama lokal','📝'),('Video Agent','Belum terhubung','🎬'),('Voice Over Agent','Belum terhubung','🎙️'),('SEO Agent','Belum terhubung','📈')]
    for name,status,emoji in agents:
        st.markdown(f"<div class='agent'><b>{emoji} {name}</b><br><span class='muted'>{status}</span></div>",unsafe_allow_html=True)
with center:
    st.markdown('### 🌐 Global Intelligence Network')
    st.markdown("<div class='globe'><div><div class='earth'>🌐</div><b style='letter-spacing:3px;color:#69e6ff'>RAK FAKTA NETWORK</b><div class='muted'>Research • Script • Production • Publishing</div></div></div>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.markdown(f"<div class='panel'><div class='muted'>RESEARCH JOBS</div><h2>{sum('Research job' in x for x in st.session_state.logs)}</h2><span class='muted'>Tersimpan di sesi ini</span></div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='panel'><div class='muted'>SCRIPT DRAFTS</div><h2>{sum('Script project' in x for x in st.session_state.logs)}</h2><span class='muted'>Tersimpan di sesi ini</span></div>",unsafe_allow_html=True)
    c3.markdown("<div class='panel'><div class='muted'>PUBLISH QUEUE</div><h2>0</h2><span class='muted'>YouTube belum terhubung</span></div>",unsafe_allow_html=True)
with right:
    st.markdown('### ⚡ Automation Status')
    st.progress(0.45, text='MVP dengan AI lokal: 45%')
    st.markdown("<div class='agent'><b>🟢 Dashboard UI</b><br><span class='muted'>Aktif</span></div><div class='agent'><b>🟡 Ollama AI</b><br><span class='muted'>Tes koneksi dari panel kiri</span></div><div class='agent'><b>🟡 Research + Script</b><br><span class='muted'>Siap setelah model tersedia</span></div><div class='agent'><b>⚪ YouTube API</b><br><span class='muted'>Belum dihubungkan</span></div>",unsafe_allow_html=True)

st.divider()
t1,t2,t3=st.tabs(['🔎 Research AI','📝 Script AI','📡 Activity Log'])
with t1:
    st.subheader('Research Agent — Riset Sejarah')
    topic=st.text_input('Topik sejarah',placeholder='Contoh: Traktat London 1824 dan pembagian wilayah Nusantara')
    focus=st.text_area('Fokus riset',placeholder='Pertanyaan utama, periode, tokoh, atau sudut pandang yang ingin diteliti...')
    if st.button('Jalankan AI Research',key='research'):
        if not topic.strip():
            st.warning('Masukkan topik terlebih dahulu.')
        else:
            prompt = f"Buat laporan riset awal untuk dokumenter sejarah berbahasa Indonesia. Topik: {topic}. Fokus: {focus or 'latar belakang, kronologi, tokoh, sebab-akibat, dan dampak'} . Susun: (1) ringkasan, (2) konteks dan kronologi, (3) tokoh/lembaga, (4) fakta yang perlu diverifikasi, (5) kemungkinan mitos atau klaim kontroversial, (6) daftar kata kunci untuk mencari sumber primer dan akademik. Bedakan fakta mapan dari dugaan. Jangan mengarang judul buku, arsip, kutipan, nomor halaman, atau URL sumber. Jika tidak yakin, tulis bahwa perlu verifikasi."
            system = 'Anda adalah asisten peneliti sejarah untuk kanal dokumenter RAK FAKTA. Utamakan kehati-hatian, konteks, kronologi, dan pemisahan fakta dari interpretasi. Anda tidak memiliki akses web otomatis; jangan mengklaim sudah memeriksa sumber terkini atau arsip.'
            with st.spinner('AI sedang menyusun riset awal...'):
                try:
                    result = ask_ollama(prompt, system)
                    st.session_state.research_result = result
                    st.session_state.logs.insert(0, f"Research job selesai: {topic} • {datetime.now().strftime('%d-%m-%Y %H:%M')}")
                except requests.exceptions.ConnectionError:
                    st.error('Tidak bisa terhubung ke Ollama. Jalankan Ollama dan pastikan model sudah diunduh.')
                except requests.exceptions.Timeout:
                    st.error('Proses terlalu lama. Coba model yang lebih ringan atau tunggu lalu ulangi.')
                except Exception as e:
                    st.error(f'Gagal menjalankan riset: {e}')
    if st.session_state.research_result:
        st.markdown('#### Hasil riset AI')
        st.markdown(st.session_state.research_result)
        st.download_button('Unduh hasil riset (.md)', st.session_state.research_result, file_name='riset_rak_fakta.md', mime='text/markdown')
        st.warning('Catatan: ini riset awal yang dihasilkan model lokal, bukan verifikasi sumber. Periksa setiap klaim dengan buku, jurnal, arsip, atau sumber primer sebelum produksi.')
with t2:
    st.subheader('Script Agent — Naskah Dokumenter')
    title=st.text_input('Judul video',placeholder='Contoh: Mengapa Belanda Membagi Nusantara?')
    duration=st.selectbox('Durasi target',['Shorts 60 detik','3 menit','5 menit','8 menit','10 menit','15 menit'])
    style=st.selectbox('Gaya narasi',['Dokumenter sinematik','Misteri sejarah','Edukatif dan netral','Storytelling dramatis'])
    research_context=st.text_area('Bahan riset (opsional)',placeholder='Tempelkan hasil riset yang ingin dijadikan dasar naskah...')
    if st.button('Buat naskah dengan AI',key='script'):
        if not title.strip():
            st.warning('Masukkan judul video terlebih dahulu.')
        else:
            prompt=f"Tulis naskah video YouTube dokumenter sejarah berbahasa Indonesia. Judul: {title}. Durasi: {duration}. Gaya: {style}. Bahan riset: {research_context or 'Belum diberikan; tandai klaim spesifik yang perlu diverifikasi dan jangan mengarang fakta.'}. Buat hook pembuka, narasi terstruktur dengan transisi, penutup, dan ajakan subscribe yang natural. Perkirakan pembagian waktu per segmen. Jangan menciptakan kutipan atau detail sejarah yang tidak didukung bahan."
            system='Anda adalah penulis naskah dokumenter sejarah kanal RAK FAKTA. Narasi menarik tetapi akurat, tidak sensasional tanpa dasar, dan tandai bagian yang perlu verifikasi.'
            with st.spinner('AI sedang menulis naskah...'):
                try:
                    result=ask_ollama(prompt,system)
                    st.session_state.script_result=result
                    st.session_state.logs.insert(0,f"Script project selesai: {title} • {datetime.now().strftime('%d-%m-%Y %H:%M')}")
                except requests.exceptions.ConnectionError:
                    st.error('Tidak bisa terhubung ke Ollama. Jalankan Ollama dan pastikan model sudah diunduh.')
                except requests.exceptions.Timeout:
                    st.error('Proses terlalu lama. Coba model yang lebih ringan atau tunggu lalu ulangi.')
                except Exception as e:
                    st.error(f'Gagal membuat naskah: {e}')
    if st.session_state.script_result:
        st.markdown('#### Draft naskah')
        st.markdown(st.session_state.script_result)
        st.download_button('Unduh naskah (.md)',st.session_state.script_result,file_name='naskah_rak_fakta.md',mime='text/markdown')
with t3:
    st.subheader('Riwayat Aktivitas')
    for log in st.session_state.logs:
        st.write('• '+log)
    if st.button('Bersihkan log'):
        st.session_state.logs=[]
        st.rerun()

st.caption('RAK FAKTA AI Control Center • MVP v0.2 • Research dan Script menggunakan Ollama lokal. Belum melakukan pencarian web, verifikasi sumber otomatis, pembuatan video, voice-over, atau publikasi YouTube.')
