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
