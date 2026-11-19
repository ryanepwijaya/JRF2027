# Road to JRF 2027 🏃‍♂️

Program lari menuju **Jakarta Running Festival 2027 – Full Marathon** (Minggu, 24 Oktober 2027).
Target finish ≤ 4:30 (COT 5 jam, cadangan 30 menit untuk sholat, WS & darurat).

- **Fase 1 · Diet & Base** — 1 Jan – 6 Jun 2027 (lari Sel/Kam/Sab, Minggu off)
- **Fase 2 · Blok Intensif 20 minggu** — 7 Jun – 24 Okt 2027 (lari Sel/Kam/Sab/Min)
- 6 blok: Base & Diet → Aerobic Rebuild → Base Building → Build → Peak → Taper & Race
- Libur nasional & cuti bersama 2027 (SKB 3 Menteri) dikosongkan; Ramadhan ± 8 Feb – 9 Mar = deload

## Struktur

| File | Isi |
|---|---|
| `index.html` | Halaman jadi (static, langsung di-serve Vercel) |
| `src/plan.py` | Semua data program: sesi, WU/Main/CD, zona, libur, blok |
| `src/template.html` | Tampilan (HTML/CSS/JS) |
| `build.py` | Gabungkan data + tampilan → `index.html` |

## Ubah program

1. Edit `src/plan.py` (menu/jarak) atau `src/template.html` (tampilan)
2. `python3 build.py`
3. Commit & push ke `main` → Vercel deploy otomatis

## Realisasi (Progres)

Data realisasi **tidak diinput manual di web**. Setiap minggu Claude menarik data dari Coros/Strava, mencocokkan dengan program, lalu memperbarui:

- `data/actuals.json` → `updated` (tanggal data terakhir) + `activities`: `{date, type: "run"|"gym", km, dur (detik), hr}`; untuk sesi Time Trial / race tambahkan `tt: {km, dur}` = hasil segmen utamanya (dari data lap), supaya benchmark tidak memakai total sesi yang termasuk WU/CD
- `data/body.json` → `entries`: `{date, weight, bodyfat?, smm?, source}` (InBody / timbangan / Coros)

Yang dipublikasikan hanya tanggal, jenis, jarak, durasi, pace, dan HR rata-rata. **Tanpa** peta rute, jam mulai, nama, atau deskripsi aktivitas.
Lalu `python3 build.py` → commit → push.

### Tombol "Sinkronkan" (menu Progres)

Tombol → PIN 6 digit → `api/sync.js` (fungsi Vercel) cek PIN → menjalankan routine Claude **"JRF 2027 · Sinkronkan realisasi"** lewat API → sesi Claude di cloud menarik Strava & Coros 30 hari terakhir, mengisi tanggal yang belum terisi (yang sudah ada dilewati), `build.py`, commit, push → Vercel deploy ulang (±3–5 menit).

Env Vercel: `SYNC_PIN`, `ROUTINE_ID` (trig_…), `ROUTINE_TOKEN` (dibuat di claude.ai/code/routines → routine → Add trigger → API → Generate token).
Pengaman: salah PIN 5× → terkunci 15 menit; jeda 3 menit antar-sinkron; routine maks 30×/jam. Berat badan/InBody tetap manual.

