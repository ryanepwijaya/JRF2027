# -*- coding: utf-8 -*-
"""Generator data program lari JRF 2027 (Ryan)."""
import json, datetime as dt

D = dt.date

# ---------------- Libur nasional & cuti bersama 2027 (SKB 3 Menteri, 15 Sep 2026) ----------------
HOLIDAYS = {
    D(2027,1,1): "Tahun Baru Masehi",
    D(2027,1,5): "Isra Mikraj",
    D(2027,2,5): "Cuti Bersama Imlek",
    D(2027,2,6): "Tahun Baru Imlek",
    D(2027,3,8): "Hari Suci Nyepi",
    D(2027,3,9): "Cuti Bersama Idulfitri",
    D(2027,3,10): "Idulfitri 1448 H",
    D(2027,3,11): "Idulfitri 1448 H",
    D(2027,3,12): "Cuti Bersama Idulfitri",
    D(2027,3,15): "Cuti Bersama Idulfitri",
    D(2027,3,25): "Cuti Bersama Wafat Yesus Kristus",
    D(2027,3,26): "Wafat Yesus Kristus",
    D(2027,3,28): "Paskah",
    D(2027,5,1): "Hari Buruh",
    D(2027,5,6): "Kenaikan Yesus Kristus",
    D(2027,5,17): "Iduladha 1448 H",
    D(2027,5,18): "Cuti Bersama Iduladha",
    D(2027,5,19): "Cuti Bersama Waisak",
    D(2027,5,20): "Hari Raya Waisak",
    D(2027,6,1): "Hari Lahir Pancasila",
    D(2027,6,6): "1 Muharam 1449 H",
    D(2027,8,15): "Maulid Nabi",
    D(2027,8,17): "HUT RI ke-82",
}
RAMADAN = (D(2027,2,8), D(2027,3,9))

# ---------------- Helper sesi ----------------
def r1(x): return round(x + 1e-9, 1)

def sess(kind, title, wu, main, cd, target, notes="", tag=None):
    total = r1(wu["km"] + main["km"] + cd["km"])
    return dict(kind=kind, title=title, wu=wu, main=main, cd=cd, target=target,
                notes=notes, km=total, tag=tag)

def W(km, desc): return dict(km=km, desc=desc)
def M(km, desc, steps=None): return dict(km=km, desc=desc, steps=steps or [])

HR_T = lambda rng, note="": dict(mode="HR", range=rng, note=note)
PACE_T = lambda rng, note="": dict(mode="Pace", range=rng, note=note)

EZ_HR = "135–148 bpm"
REC_HR = "≤ 135 bpm"
LR1_HR = "140–152 bpm"
LR2_HR = "145–155 bpm"

WU_EASY = W(1.0, "Jog sangat pelan, HR ≤ 135. Biarkan badan panas pelan-pelan.")
CD_EASY = W(1.0, "Turunkan tempo, jog santai HR ≤ 135 sampai napas tenang.")

def easy(title, main_km, desc, steps=None, notes="", wu=None, cd=None, hr=EZ_HR):
    return sess("easy", title, wu or WU_EASY, M(main_km, desc, steps), cd or CD_EASY,
                HR_T(hr, "Pace ikut HR. Kalau panas dan HR naik, pelankan, jangan dipaksa."), notes)

def recovery(title, main_km, desc, notes="", steps=None):
    return sess("recovery", title, W(0.5, "Jog super pelan, hampir jalan, HR ≤ 125."),
                M(main_km, desc, steps), W(0.5, "Jog super pelan, HR ≤ 125."),
                HR_T(REC_HR, "Tujuannya sirkulasi darah, bukan latihan. Lebih pelan = lebih benar."), notes)

def longrun(title, total_km, desc, hr, notes="", steps=None, wu_km=1.5, cd_km=1.0):
    main_km = r1(total_km - wu_km - cd_km)
    return sess("long", title,
                W(wu_km, "Jog pelan HR ≤ 140, mulai lebih lambat dari pace steady."),
                M(main_km, desc, steps),
                W(cd_km, "Jog santai HR ≤ 135, lalu jalan 3–5 menit."),
                HR_T(hr, "Steady = nyaman, masih bisa ngobrol kalimat pendek. Enjoy the view."), notes)

def quality(title, wu, main_km, desc, steps, cd, target, notes=""):
    return sess("quality", title, wu, M(main_km, desc, steps), cd, target, notes)

# pace zones
T1, T2 = "5:45–6:00 /km", "5:35–5:50 /km"
I1, I2 = "5:05–5:20 /km", "4:55–5:10 /km"
R_ = "4:40–4:55 /km"
HMP = "6:00–6:10 /km"

WU_Q = W(2.0, "1.6 km jog easy HR ≤ 140, lalu 4 × 100 m strides (jog 100 m di antaranya).")
WU_Q25 = W(2.5, "2.1 km jog easy HR ≤ 140, lalu 4 × 100 m strides (jog 100 m di antaranya).")
WU_Q15 = W(1.5, "1.1 km jog easy HR ≤ 140, lalu 4 × 100 m strides.")
CD_Q = W(1.5, "Jog santai HR ≤ 135. Jangan langsung berhenti.")
CD_Q2 = W(2.0, "Jog santai HR ≤ 135, 500 m terakhir paling pelan.")

LONG_FUEL = "Bawa minum. Latihan asupan: gel/karbo tiap ±45 menit (mulai menit ke-45)."
LONG_FUEL_RACE = "Simulasi race: gel tiap 40–45 menit + minum sedikit tiap 2,5–3 km (seperti WS JRF). Catat apa yang cocok di perut."

# ---------------- FASE 1: Diet & Base (Sel/Kam/Sab, Minggu off) ----------------
# struktur: list minggu; tiap minggu dict hari->sesi (key: 'tue','thu','sat','sun')
P1 = []
def p1(block, tue=None, thu=None, sat=None, note=""):
    P1.append(dict(block=block, tue=tue, thu=thu, sat=sat, note=note))

# W0 (1–3 Jan)
p1("pembuka", sat=longrun("Long Run Pembuka 2027", 12,
   "Steady santai, rute favorit. Anggap ini 'cek kondisi' setelah Bormar dan libur akhir tahun.", LR1_HR),
   note="Minggu pembuka (hanya 1–3 Jan). Fokus mulai kebiasaan, bukan volume.")

# --- Base Maintenance W1–W5
p1("base_maint",
   thu=quality("Strides & Form", W(1.0, "Jog pelan HR ≤ 135."), 5.0,
        "Easy run dengan sisipan strides untuk menjaga kelincahan kaki.",
        ["4 km easy (HR 135–148)", "6 × 100 m strides (± 85% effort, rileks, bukan sprint)", "Recovery: jalan/jog 100 m tiap strides"],
        W(1.0, "Jog santai HR ≤ 135."), HR_T(EZ_HR, "Strides dirasakan, bukan dikejar angka pace."), "Selasa libur (Isra Mikraj), jadi minggu ini 2 sesi saja."),
   sat=longrun("Long Run Steady — Rute Sudirman–Thamrin", 14,
        "Steady konstan. Jalur lurus dan rata, nikmati kotanya pagi-pagi.", LR1_HR))
p1("base_maint",
   tue=easy("Easy Konstan", 5.0, "Lari easy rata dari awal sampai akhir. Fokus napas hidung–mulut tenang."),
   thu=quality("Fartlek Km 600/400", WU_Q, 5.0, "Fartlek berbasis jarak, ritme main-main.",
        ["5 × (600 m cepat @ 5:50–6:05 /km + 400 m easy)", "Bagian easy tetap jalan terus, jangan berhenti"],
        CD_Q, PACE_T("5:50–6:05 /km (bagian cepat)", "HR jangan lewat 175 di bagian cepat.")),
   sat=longrun("Long Run Steady — Loop GBK", 15, "Steady konstan, loop luar GBK (± 2,3 km/putaran). Gampang cari minum.", LR1_HR))
p1("base_maint",
   tue=easy("Easy Progresif Ringan", 5.0, "Mulai di HR 135, naik pelan. 1 km terakhir di HR 145–148.",
            ["Km 1–3: HR 135–142", "Km 4–5: HR 143–148"]),
   thu=quality("Cruise Interval 4 × 1 km", WU_Q, 5.2, "Threshold dalam potongan pendek, kontrol tempo.",
        ["4 × 1 km @ T (5:45–6:00 /km)", "Recovery: 400 m jog easy di antara repetisi"],
        CD_Q, PACE_T(T1, "HR guard: jangan lewat 178. Rep terakhir harus sama cepat dengan rep pertama.")),
   sat=longrun("Long Run Steady — Rute Kuningan–Menteng", 16, "Steady, rute rindang Menteng. Variasikan jalan supaya tidak bosan.", LR1_HR, LONG_FUEL))
p1("base_maint",
   tue=easy("Easy + Strides", 4.0, "Easy run lalu tutup dengan strides di 500 m terakhir main set.",
            ["3,5 km easy", "4 × 100 m strides di 500 m terakhir"]),
   thu=quality("Time Trial 5K (Benchmark #1)", WU_Q, 5.0, "Tes 5K all-out tapi terkontrol. Hasilnya jadi patokan pace fase ini.",
        ["Km 1: sedikit di bawah target, jangan meledak", "Km 2–4: tahan ritme", "Km 5: habiskan"],
        CD_Q, PACE_T("All-out terkontrol", "Catat waktu & HR rata-rata. Kalau 5K < 25:00, pace T bisa digeser 5–10 dtk lebih cepat."),
        "Minggu cutback: volume turun, satu tes kualitas."),
   sat=longrun("Long Run Steady Pendek — Recovery Week", 12, "Steady santai, pemulihan setelah time trial.", LR1_HR))
p1("base_maint",
   tue=easy("Easy + Drills Lari", 5.0, "Drills di km pertama main set, lalu easy biasa.",
            ["2 × 30 m A-skip, B-skip, high knees, butt kicks (jalan balik sebagai recovery)", "Sisanya easy HR 135–148"]),
   thu=quality("Hill Repeats Flyover 6 × 200 m", WU_Q25, 2.4, "Tanjakan pendek untuk kekuatan kaki (ramp flyover/parkir).",
        ["6 × 200 m tanjakan, effort kuat tapi form tegak", "Turun 200 m jog pelan sebagai recovery"],
        CD_Q2, PACE_T("Effort ± 5K (pace abaikan di tanjakan)", "Fokus dorongan pinggul & lengan. HR boleh sampai 180 di puncak.")),
   sat=longrun("Long Run Steady — Penutup Pra-Ramadhan", 16, "Steady konstan. Long run 'normal' terakhir sebelum Ramadhan.", LR1_HR, LONG_FUEL + " Sabtu ini libur Imlek, jadwal tetap jalan."))

# --- Ramadan deload W6–W9
RN = "Ramadhan: lari setelah tarawih (treadmill/outdoor malam) atau 'ngabuburun' pendek sebelum berbuka. Jangan lari kualitas saat puasa."
p1("ramadan",
   tue=easy("Easy Pasca-Tarawih (Treadmill)", 3.0, "Treadmill 0–1% incline, easy rata. Minum cukup setelah berbuka.", notes=RN),
   thu=quality("Easy + 4 Strides", W(1.0, "Jog pelan HR ≤ 135."), 3.0, "Easy pendek, strides untuk jaga 'rasa cepat'.",
        ["2,6 km easy", "4 × 100 m strides rileks"], W(1.0, "Jog santai."), HR_T(EZ_HR, "Lakukan setelah tarawih."), RN),
   sat=longrun("Steady Malam Pasca-Tarawih", 10, "Steady ringan, treadmill atau outdoor malam. Ini menjaga base, bukan membangun.", "135–148 bpm", RN))
p1("ramadan",
   tue=easy("Ngabuburun Pre-Buka", 2.0, "Super santai, selesai pas azan Magrib. Bawa air untuk berbuka.",
            wu=W(1.0, "Jog super pelan HR ≤ 130."), cd=W(1.0, "Jog/jalan pelan."), hr="≤ 140 bpm", notes=RN),
   thu=easy("Easy Progresif Ringan (Malam)", 3.0, "Pasca-tarawih. Mulai HR 135, 1 km terakhir HR 145.", notes=RN),
   sat=longrun("Steady Malam — Treadmill Incline 1%", 11, "Steady konstan di treadmill 1%, nonton kajian/podcast biar nggak bosan.", "135–148 bpm", RN))
p1("ramadan",
   tue=easy("Easy Treadmill Incline 1%", 3.0, "Easy rata di incline 1%, cadence ringan.", notes=RN),
   thu=quality("Pickup Ringan 6 × 200 m", W(1.0, "Jog pelan HR ≤ 135."), 3.5, "Sentuhan kecepatan ringan, bukan sesi berat.",
        ["6 × 200 m pickup @ ± 5:45 /km", "Recovery: 200 m jog easy", "Sisa jarak easy"],
        W(1.0, "Jog santai."), PACE_T("± 5:45 /km (pickup)", "Hanya setelah tarawih, perut sudah terisi."), RN),
   sat=longrun("Steady Malam — Rute Taman", 12, "Steady santai, rute taman/komplek yang aman malam hari.", "135–148 bpm", RN + " Bawa minum."))
p1("ramadan",
   tue=easy("Ngabuburun Pre-Buka", 2.0, "Super santai menjelang Magrib.", wu=W(1.0, "Jog super pelan HR ≤ 130."),
            cd=W(1.0, "Jog/jalan pelan."), hr="≤ 140 bpm", notes=RN),
   thu=quality("Easy + 4 Strides (Malam)", W(1.0, "Jog pelan HR ≤ 135."), 3.0, "Easy pendek + strides.",
        ["2,6 km easy", "4 × 100 m strides rileks"], W(1.0, "Jog santai."), HR_T(EZ_HR, "Setelah tarawih."), RN),
   sat=longrun("Steady Malam Penutup Ramadhan", 10, "Steady santai. Persiapan mudik/Lebaran.", "135–148 bpm", RN))

# --- Lebaran W10
p1("lebaran",
   sat=longrun("Lari Lebaran — Steady Santai", 10, "Steady santai di mana pun kamu mudik. Nikmati jalan kampung.", LR1_HR,
               "Selasa & Kamis libur Lebaran, dikosongkan."),
   note="Minggu Lebaran: Nyepi, cuti bersama, Idulfitri. Hanya Sabtu yang terprogram.")

# --- Rebuild Base W11–W14
p1("rebuild",
   tue=easy("Easy Kembali ke Ritme", 4.0, "Easy rata. Badan mungkin berat pasca-Lebaran, itu wajar."),
   thu=quality("Easy + 6 Strides", W(1.0, "Jog pelan HR ≤ 135."), 5.0, "Re-entry: easy dengan strides.",
        ["4,4 km easy", "6 × 100 m strides"], W(1.0, "Jog santai."), HR_T(EZ_HR, "Strides rileks, form tegak.")),
   sat=longrun("Long Run Steady — Re-Entry", 12, "Steady santai, cek kondisi.", LR1_HR))
p1("rebuild",
   tue=easy("Easy Cadence Focus", 5.0, "Easy, tiap awal km jaga cadence 180+ selama 200 m, lalu natural.",
            ["5 × (200 m cadence 180+ / 800 m natural)"]),
   sat=longrun("Long Run Steady — Rute Kanal Banjir Timur/Barat", 14, "Steady di rute baru yang panjang dan lurus.", LR1_HR),
   note="Kamis cuti bersama (Wafat Yesus Kristus), dikosongkan.")
p1("rebuild",
   tue=easy("Easy Konstan", 5.0, "Easy rata, fokus relaks bahu."),
   thu=quality("Tempo Progresif 4 km", WU_Q, 4.0, "Mulai di steady, akhiri di threshold.",
        ["Km 1: 6:30 /km", "Km 2: 6:15 /km", "Km 3: 6:00 /km", "Km 4: 5:50 /km"], CD_Q2,
        PACE_T("6:30 → 5:50 /km (turun tiap km)", "HR guard ≤ 176.")),
   sat=longrun("Long Run Steady — Loop GBK", 16, "Steady konstan, loop GBK.", LR1_HR, LONG_FUEL))
p1("rebuild",
   tue=easy("Easy + Strides", 4.6, "Easy, tutup dengan strides.", ["4 km easy", "6 × 100 m strides"]),
   thu=quality("Ladder 400-800-1200-800-400", WU_Q, 5.2, "Tangga naik-turun, ritme interval.",
        ["400 m @ 5:10", "800 m @ 5:20", "1200 m @ 5:40", "800 m @ 5:20", "400 m @ 5:10", "Recovery: 400 m jog tiap rep"],
        CD_Q, PACE_T("5:10–5:40 /km sesuai rep", "HR guard ≤ 183 di rep pendek.")),
   sat=longrun("Long Run Steady — Rute Pesisir PIK/Ancol", 17, "Steady, rute baru dekat laut. Berangkat subuh, angin pagi enak.", LR1_HR, LONG_FUEL))

# --- Aerobic Build W15–W19
p1("aerobic",
   tue=easy("Easy Rute Baru (Eksplorasi)", 6.0, "Easy di rute yang belum pernah kamu lewati. Biar nggak bosan."),
   thu=quality("Cruise Interval 3 × 1,5 km", WU_Q, 5.3, "Threshold lebih panjang per rep.",
        ["3 × 1,5 km @ T (5:45–6:00 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T(T1, "HR guard ≤ 178.")),
   sat=longrun("Long Run Steady — Sudirman CFD Vibes", 18, "Steady konstan, rute protokol. Long run 18K pertama fase ini.", LR1_HR, LONG_FUEL))
p1("aerobic",
   tue=easy("Easy Negative Split", 6.0, "3 km pertama HR 135–140, 3 km kedua HR 142–148."),
   thu=quality("Interval 5 × 800 m", WU_Q, 5.6, "VO2 ringan, rep 800 m.",
        ["5 × 800 m @ I (5:05–5:20 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T(I1, "Rep 1 jangan terlalu cepat. HR boleh 175–185.")),
   sat=longrun("Long Run Steady — Loop Senayan–Kebayoran", 19, "Steady, sedikit variasi elevasi ringan.", LR1_HR, LONG_FUEL))
p1("aerobic",
   tue=easy("Easy + Strides (Cutback)", 4.0, "Easy pendek + strides.", ["3,4 km easy", "6 × 100 m strides"]),
   thu=quality("Drills & Strides Session", W(1.0, "Jog pelan HR ≤ 135."), 5.0, "Teknik lari: drills + strides, kaki tetap segar.",
        ["1 km easy", "2 × 30 m: A-skip, B-skip, high knees, butt kicks, carioca", "8 × 100 m strides", "Sisanya easy"],
        W(1.0, "Jog santai."), HR_T(EZ_HR, "Fokus kualitas gerak, bukan capek.")),
   sat=longrun("Long Run Steady Pendek — Cutback", 14, "Steady santai. Sabtu ini Hari Buruh, jadwal tetap jalan.", LR1_HR),
   note="Minggu cutback: volume turun untuk menyerap latihan.")
p1("aerobic",
   tue=easy("Easy Konstan Panjang", 6.0, "Easy rata, sedikit lebih panjang dari biasanya."),
   sat=longrun("Long Run Steady — 20K Pertama", 20, "Steady konstan. Milestone 20K fase diet.", LR1_HR, LONG_FUEL),
   note="Kamis libur Kenaikan Yesus Kristus, dikosongkan.")
p1("aerobic",
   tue=easy("Easy Progresif", 6.0, "Mulai HR 135, akhiri HR 148.", ["Km 1–3: HR 135–140", "Km 4–6: HR 142–148"]),
   thu=quality("Progression Run 8 km", W(1.0, "Jog pelan HR ≤ 135."), 8.0, "Naik bertahap dari easy ke threshold.",
        ["3 km easy (HR 140–148)", "3 km steady @ 6:25–6:35 /km", "2 km @ T 5:50–6:00 /km"],
        W(1.0, "Jog santai HR ≤ 135."), PACE_T("6:35 → 5:50 /km", "HR guard ≤ 176.")),
   sat=longrun("Long Run Steady — Rute Pesisir", 21, "Steady konstan. Long run terpanjang fase diet.", LR1_HR, LONG_FUEL))

# --- Pre-JAKIM Sharpening W20–W22
p1("prejakim",
   sat=longrun("Long Run Steady — Minggu Iduladha", 18, "Steady konstan.", LR1_HR, LONG_FUEL),
   note="Iduladha, cuti bersama, dan Waisak: Selasa & Kamis dikosongkan.")
p1("prejakim",
   tue=easy("Easy + Strides", 6.0, "Easy + strides.", ["5,4 km easy", "6 × 100 m strides"]),
   thu=quality("HM Pace 3 × 2 km", WU_Q, 6.8, "Latihan pace target JAKIM.",
        ["3 × 2 km @ HM pace (6:00–6:10 /km)", "Recovery: 400 m jog"], CD_Q,
        PACE_T(HMP, "HM pace ini estimasi. Sesuaikan dengan hasil TT 5K: HM pace ≈ pace 5K + 45–50 dtk.")),
   sat=longrun("Long Run Steady — Terakhir Sebelum JAKIM", 18, "Steady konstan, rute favorit.", LR1_HR, LONG_FUEL))
p1("prejakim",
   thu=quality("Tempo 4 km @ HM Pace", WU_Q, 4.0, "Sesi tajam terakhir sebelum JAKIM.",
        ["4 km kontinu @ HM pace 6:00–6:10 /km"], CD_Q, PACE_T(HMP, "Harus terasa terkontrol. Kalau berat, JAKIM jangan dipaksa cepat.")),
   sat=longrun("Steady Pendek — Taper Mini", 12, "Steady santai, kaki disegarkan.", LR1_HR),
   note="Selasa libur Hari Lahir Pancasila. Minggu = 1 Muharam (off).")

# ---------------- FASE 2: Blok Intensif 20 minggu (Sel/Kam/Sab/Min) ----------------
P2 = []
def p2(block, tue=None, thu=None, sat=None, sun=None, note=""):
    P2.append(dict(block=block, tue=tue, thu=thu, sat=sat, sun=sun, note=note))

def mp_t(rng): return PACE_T(rng, "Pace utama, HR guard 155–165. Kalau HR > 168 sebelum separuh sesi, turunkan 5–10 dtk/km.")

# B1 — JAKIM
p2("jakim",
   tue=easy("Easy + Strides", 6.4, "Easy, kaki dijaga segar.", ["5,8 km easy", "6 × 100 m strides"]),
   thu=quality("Sharpener 3 × 1 km HM Pace", WU_Q, 3.8, "Pengingat ritme race, bukan sesi berat.",
        ["3 × 1 km @ HM pace (6:00–6:10 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T(HMP, "Harus terasa mudah.")),
   sat=sess("easy", "Shakeout Pra-JAKIM", W(0.5, "Jog super pelan."),
        M(3.0, "Shakeout + 3 strides, lalu istirahat, siapkan race kit.", ["2,6 km jog santai", "3 × 100 m strides"]),
        W(0.5, "Jog super pelan."), HR_T("≤ 140 bpm", "Pendek saja.")),
   sun=sess("race", "RACE: Jakarta International Marathon — Half Marathon (tune-up)", W(1.5, "1 km jog pelan + 3 strides, 15–20 menit sebelum start."),
        M(21.1, "HM all-out terkontrol. Hasilnya dipakai menghitung MP blok ini.",
          ["Km 0–5: 5–10 dtk lebih lambat dari target (HR ≤ 165)", "Km 5–16: target pace", "Km 16–21: habiskan kalau masih ada"]),
        W(1.0, "Jalan/jog pelan setelah finish."),
        PACE_T("Target ± 6:00–6:10 /km", "Rumus kalibrasi: MP blok = pace HM JAKIM + 25–30 dtk/km."),
        "Catat: waktu, HR rata-rata, rasa di km 15–21."),
   note="Minggu 1 blok: JAKIM HM sebagai tes awal. Minggu (race) menggantikan recovery run.")
# B2 — recovery
p2("jakim",
   tue=recovery("Recovery Pasca-JAKIM", 4.0, "Recovery murni, kaki dikendurkan."),
   thu=easy("Easy + 4 Strides", 5.4, "Easy, cek kaki sudah pulih.", ["5 km easy", "4 × 100 m strides kalau kaki enak"]),
   sat=longrun("Long Run Steady Santai", 14, "Steady santai, belum dipaksa.", LR2_HR),
   sun=recovery("Recovery Flat", 4.0, "Rute rata, super santai."),
   note="Minggu pemulihan setelah JAKIM. Belum ada sesi kualitas.")

# Base Building B3–B7
p2("base",
   tue=easy("Easy Konstan", 6.0, "Easy rata, mulai bangun volume."),
   thu=quality("Fartlek Km 800/400", WU_Q, 7.2, "Fartlek berbasis jarak, ritme threshold.",
        ["6 × (800 m @ 5:40–5:55 /km + 400 m easy)"], CD_Q, PACE_T("5:40–5:55 /km (bagian cepat)", "HR guard ≤ 178.")),
   sat=longrun("Long Run Steady — Loop GBK", 20, "Steady konstan.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Treadmill 0%", 4.0, "Treadmill 0%, sambil nonton. Santai total."))
p2("base",
   tue=easy("Easy Progresif", 7.0, "Mulai HR 135, akhiri HR 148.", ["Km 1–4: HR 135–142", "Km 5–7: HR 143–148"]),
   thu=quality("Hill Repeats 8 × 200 m + Easy", WU_Q25, 4.2, "Kekuatan tanjakan untuk betis & glute.",
        ["8 × 200 m tanjakan, effort kuat, form tegak", "Turun 200 m jog pelan", "Setelah set: 1 km easy datar"],
        CD_Q2, PACE_T("Effort ± 5K di tanjakan", "Pace abaikan di tanjakan. HR boleh sampai 182.")),
   sat=longrun("Long Run Steady — Rute Kanal Banjir", 22, "Steady konstan, rute panjang & lurus.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Taman Kota", 5.0, "Rute taman, permukaan lembut kalau ada."))
p2("base",
   tue=easy("Easy + Drills", 7.0, "Drills di awal, lalu easy.",
            ["2 × 30 m A-skip, B-skip, high knees, butt kicks", "Sisanya easy HR 135–148"]),
   thu=quality("Threshold Kontinu 5 km", WU_Q, 5.0, "Tempo kontinu, belajar 'nyaman-tidak-nyaman'.",
        ["5 km kontinu @ T (5:35–5:50 /km)"], CD_Q, PACE_T(T2, "HR guard ≤ 178. Pace rata, bukan makin cepat.")),
   sat=longrun("Long Run Steady — Eksplorasi Rute Baru", 24, "Steady, coba rute yang belum pernah. Pecah bosan.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Flat", 5.0, "Rute rata, super santai."))
p2("base",
   tue=easy("Easy Konstan (Cutback)", 5.0, "Easy rata, volume turun."),
   thu=quality("Repetisi 10 × 400 m", WU_Q, 5.8, "Kecepatan & ekonomi lari.",
        ["10 × 400 m @ R (4:40–4:55 /km)", "Recovery: 200 m jog"], CD_Q, PACE_T(R_, "Rileks di kecepatan. Jangan tegang di bahu.")),
   sat=longrun("Long Run Steady Pendek — Cutback", 16, "Steady santai.", LR2_HR),
   sun=recovery("Recovery + 4 Strides", 4.0, "Recovery, akhiri 4 strides ringan kalau kaki enak.", steps=["3,6 km recovery", "4 × 100 m strides opsional"]),
   note="Minggu cutback.")
p2("base",
   tue=easy("Easy Rute Baru", 8.0, "Easy di rute baru."),
   thu=quality("MP Intro 3 × 3 km", WU_Q, 10.0, "Kenalan dengan marathon pace.",
        ["3 × 3 km @ MP (6:45–6:55 /km)", "Recovery: 500 m jog easy"], CD_Q, mp_t("6:45–6:55 /km (MP awal)"),
        "MP awal ini asumsi. Setelah JAKIM: MP = pace HM JAKIM + 25–30 dtk/km."),
   sat=longrun("Long Run Steady — 25K", 25, "Steady konstan, rute favorit.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Treadmill 0%", 5.0, "Treadmill, santai total."))

# Build B8–B13
p2("build",
   tue=easy("Easy + Strides", 8.0, "Easy + strides.", ["7,4 km easy", "6 × 100 m strides"]),
   thu=quality("Cruise Interval 4 × 2 km", WU_Q, 9.2, "Threshold panjang, fondasi stamina.",
        ["4 × 2 km @ T (5:35–5:50 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T(T2, "HR guard ≤ 178.")),
   sat=longrun("Long Run Steady — Rute Sudirman–Kota Tua", 26, "Steady, rute lurus ke arah Kota Tua.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Flat", 5.0, "Super santai."))
p2("build",
   tue=easy("Medium Easy", 9.0, "Easy rata, sedikit lebih panjang."),
   thu=quality("MP Kontinu 8 km", WU_Q, 8.0, "MP kontinu pertama.",
        ["8 km kontinu @ MP (6:40–6:50 /km)"], CD_Q2, mp_t("6:40–6:50 /km")),
   sat=longrun("Long Run Steady — 28K", 28, "Steady konstan, rute pesisir/rindang.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Taman", 5.0, "Santai, permukaan lembut kalau ada."))
p2("build",
   tue=easy("Easy Konstan (Cutback)", 6.0, "Easy rata."),
   thu=quality("Yasso 6 × 800 m", WU_Q, 6.8, "Sesi klasik marathoner.",
        ["6 × 800 m @ 5:00–5:10 /km", "Recovery: 400 m jog"], CD_Q, PACE_T("5:00–5:10 /km", "HR boleh 175–185.")),
   sat=longrun("Long Run Steady Pendek — Cutback", 20, "Steady santai.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Flat (Maulid)", 4.0, "Super santai. Hari libur Maulid, tapi akhir pekan tetap jalan."),
   note="Minggu cutback.")
p2("build",
   thu=quality("MP Sandwich 4–1–4", WU_Q, 9.0, "Dua blok MP dipisah 1 km easy.",
        ["4 km @ MP (6:35–6:45 /km)", "1 km easy", "4 km @ MP (6:35–6:45 /km)"], CD_Q, mp_t("6:35–6:45 /km")),
   sat=longrun("Long Run Steady — 29K", 29, "Steady konstan.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Treadmill 0%", 6.0, "Santai total."),
   note="Selasa libur HUT RI, dikosongkan.")
p2("build",
   tue=easy("Medium Easy Panjang", 10.0, "Easy rata, medium-long midweek."),
   thu=quality("Over-Under 6 × (600/400)", WU_Q, 6.0, "Ganti-ganti sedikit di atas & di bawah threshold, kontinu.",
        ["6 × (600 m @ 5:30–5:40 /km + 400 m @ 6:30–6:40 /km), tanpa berhenti"], CD_Q,
        PACE_T("5:30–5:40 / 6:30–6:40 /km", "Belajar membuang laktat sambil tetap lari. HR guard ≤ 180.")),
   sat=longrun("Long Run Steady — 30K", 30, "Steady konstan. Long run 30K pertama blok.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Flat", 6.0, "Super santai."))
p2("build",
   tue=easy("Easy + Strides", 7.4, "Easy + strides.", ["6,8 km easy", "6 × 100 m strides"]),
   thu=quality("Sharpener 4 × 1 km HM Pace", WU_Q, 5.2, "Ingatkan ritme race sebelum time trial.",
        ["4 × 1 km @ HM pace (5:50–6:00 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T("5:50–6:00 /km", "Harus terasa mudah.")),
   sat=sess("race", "HM Time Trial (Benchmark #2)", W(2.0, "1,6 km jog easy + 4 strides."),
        M(21.1, "Time trial HM solo atau race HM resmi kalau ada. Ini cek realistis target 4:30.",
          ["Km 0–5: sedikit di bawah target", "Km 5–16: tahan pace rata", "Km 16–21: habiskan"]),
        W(1.0, "Jalan/jog pelan."),
        PACE_T("Target ± 5:50–6:00 /km", "Kalau HM ≤ 2:07, target 4:30 realistis. Kalau > 2:12, turunkan target ke 4:40–4:45."),
        LONG_FUEL_RACE),
   sun=recovery("Recovery Pasca-TT", 5.0, "Recovery murni."),
   note="Minggu time trial: Sabtu HM TT menggantikan long run.")

# Peak B14–B17
p2("peak",
   tue=easy("Easy Pemulihan Pasca-TT", 7.0, "Easy pelan, di bawah HR 145.", hr="135–145 bpm"),
   thu=quality("Progression Run 10 km", W(1.0, "Jog pelan HR ≤ 135."), 10.0, "Easy → MP → threshold.",
        ["4 km easy (HR 140–148)", "3 km @ MP (6:25–6:35 /km)", "3 km @ T (5:35–5:50 /km)"],
        W(1.0, "Jog santai."), PACE_T("Easy → 6:30 → 5:40 /km", "HR guard ≤ 178.")),
   sat=longrun("Long Run Steady — 30K", 30, "Steady konstan.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Taman", 6.0, "Santai."))
p2("peak",
   tue=easy("Medium Easy Panjang", 10.0, "Easy rata, medium-long."),
   thu=quality("MP Kontinu 10 km", WU_Q, 10.0, "MP kontinu, makin dekat ke target race.",
        ["10 km kontinu @ MP (6:25–6:35 /km)"], CD_Q, mp_t("6:25–6:35 /km")),
   sat=longrun("Long Run Steady — 32K", 32, "Steady konstan. Berangkat sepagi mungkin (sebelum Subuh), sholat di jalan seperti race nanti.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Treadmill 0%", 6.0, "Santai total."))
p2("peak",
   tue=easy("Easy Konstan (Cutback)", 7.0, "Easy rata."),
   thu=quality("Interval 5 × 1 km", WU_Q, 6.6, "VO2 terakhir sebelum puncak.",
        ["5 × 1 km @ I (4:55–5:10 /km)", "Recovery: 400 m jog"], CD_Q, PACE_T(I2, "HR boleh 175–185.")),
   sat=longrun("Long Run Steady — Cutback 22K", 22, "Steady santai.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Flat", 5.0, "Santai."),
   note="Minggu cutback sebelum long run terpanjang.")
p2("peak",
   tue=easy("Medium Easy Panjang", 10.0, "Easy rata."),
   thu=quality("MP 2 × 5 km", WU_Q, 10.5, "MP dalam dua blok, dekat target race.",
        ["2 × 5 km @ MP (6:20–6:30 /km)", "Recovery: 500 m jog"], CD_Q, mp_t("6:20–6:30 /km")),
   sat=longrun("Long Run Steady — 33K Dress Rehearsal", 33,
        "Steady konstan dengan full race kit: sepatu, baju, gel, jam start sama seperti JRF. Opsional: 3 km terakhir di MP kalau badan masih enak.",
        LR2_HR, LONG_FUEL_RACE + " Ini long run terpanjang. Latih juga jeda sholat Subuh.",
        steps=["Km 1–27: steady HR 145–155", "Km 28–30,5 (opsional): MP 6:25–6:30 /km, hanya kalau HR masih ≤ 158"]),
   sun=recovery("Recovery Flat", 6.0, "Super santai."),
   note="Minggu puncak. Setelah ini taper.")

# Taper B18–B20
p2("taper",
   tue=easy("Easy Konstan", 8.0, "Easy rata, volume mulai turun."),
   thu=quality("MP Kontinu 8 km", WU_Q, 8.0, "Ritme race, volume lebih kecil.",
        ["8 km kontinu @ MP (6:20–6:28 /km)"], CD_Q, mp_t("6:20–6:28 /km")),
   sat=longrun("Long Run Steady — Taper 24K", 24, "Steady santai.", LR2_HR, LONG_FUEL_RACE),
   sun=recovery("Recovery Treadmill 0%", 5.0, "Santai."))
p2("taper",
   tue=easy("Easy + Strides", 6.0, "Easy + strides.", ["5,4 km easy", "6 × 100 m strides"]),
   thu=quality("MP 3 × 2 km", W(1.5, "1,1 km jog easy + 4 strides."), 6.8, "Pengingat ritme race.",
        ["3 × 2 km @ MP (6:20–6:28 /km)", "Recovery: 400 m jog"], CD_Q, mp_t("6:20–6:28 /km")),
   sat=longrun("Long Run Steady — Taper 16K", 16, "Steady santai, kaki disegarkan.", LR2_HR, LONG_FUEL),
   sun=recovery("Recovery Flat", 4.0, "Super santai."))
p2("taper",
   tue=easy("Easy + 2 × 1 km MP", 5.0, "Easy dengan sentuhan MP.", ["1,5 km easy", "2 × 1 km @ MP 6:24 /km (jog 500 m)", "Sisanya easy"]),
   thu=easy("Shakeout + 3 × 400 m MP", 3.0, "Pendek. Rasakan pace race, lalu selesai.", ["1 km easy", "3 × 400 m @ MP 6:24 /km (jog 200 m)", "Sisanya easy"]),
   sat=sess("easy", "Shakeout Pra-Race", W(0.5, "Jog super pelan."),
        M(2.0, "Shakeout + 3 strides. Ambil race pack, siapkan race kit, tidur awal.", ["1,7 km jog santai", "3 × 100 m strides"]),
        W(0.5, "Jog super pelan."), HR_T("≤ 140 bpm", "Pendek saja.")),
   sun=sess("race", "🏁 RACE DAY: Jakarta Running Festival 2027 — Full Marathon", W(0.5, "Jog sangat pelan 5 menit + 2 strides sebelum masuk start."),
        M(42.2, "Target finish ≤ 4:30 (COT 5 jam, cadangan 30 menit untuk sholat, WS, darurat).",
          ["Km 0–5: 6:35–6:40 /km (sengaja lebih lambat, HR ≤ 158)",
           "Km 5–30: 6:22–6:26 /km, HR 158–165",
           "Sholat Subuh: berhenti di titik aman, ± 5–7 menit, sudah dihitung di cadangan",
           "Km 30–42: tahan 6:24. Kalau masih kuat di km 35, baru naikkan tempo",
           "Gel tiap 40–45 menit, minum sedikit di tiap WS"]),
        W(0.0, "Jalan pelan setelah finish, minum, makan."),
        PACE_T("6:24 /km rata-rata (4:30)", "Pace final ditentukan dari HM TT minggu ke-13. Jangan ikut-ikutan pace orang di 10 km pertama.")),
   note="Race week. Total minggu ini sudah termasuk 42,2 km race.")

# ---------------- Rakit kalender ----------------
STAGE = {
  "pembuka":"Pembuka", "base_maint":"Base Maintenance", "ramadan":"Ramadhan Deload", "lebaran":"Lebaran",
  "rebuild":"Rebuild", "aerobic":"Aerobic Build", "prejakim":"Pre-JAKIM", "jakim":"JAKIM & Recovery",
  "base":"Base Building", "build":"Build", "peak":"Peak", "taper":"Taper & Race",
}
REMAP = {"pembuka":"b1","base_maint":"b1","ramadan":"b1","lebaran":"b1",
         "rebuild":"b2","aerobic":"b2","prejakim":"b2",
         "jakim":"b3","base":"b3","build":"b4","peak":"b5","taper":"b6"}
BLOCKS = {
  "b1": dict(no=1, name="Base & Diet", phase=1, color="#0ea5e9",
             desc="1 Jan – 14 Mar. Jaga base pasca-Bormar sambil fokus diet & gym: 3 lari/minggu, long run steady 12–16 km. Di dalamnya ada Ramadhan deload (± 20 km/minggu, lari setelah tarawih) dan minggu Lebaran."),
  "b2": dict(no=2, name="Aerobic Rebuild", phase=1, color="#22c55e",
             desc="15 Mar – 6 Jun. Bangun lagi base aerobik pasca-Lebaran: long run naik 12 → 21 km, kualitas threshold/interval ringan, ditutup pertajaman HM pace menuju JAKIM."),
  "b3": dict(no=3, name="Base Building", phase=2, color="#ec4899",
             desc="7 Jun – 25 Jul. Dibuka JAKIM HM sebagai tes awal (hasilnya menentukan MP), 1 minggu pemulihan, lalu volume naik 40 → 55 km dan long run 20 → 25 km. Kenalan dengan MP."),
  "b4": dict(no=4, name="Build", phase=2, color="#6366f1",
             desc="26 Jul – 5 Sep. Marathon specific: MP kontinu, cruise interval, Yasso, long run 26 → 30 km. Ditutup HM Time Trial sebagai cek realistis target 4:30."),
  "b5": dict(no=5, name="Peak", phase=2, color="#e11d48",
             desc="6 Sep – 3 Okt. Minggu terberat: long run 30–33 km, MP 10 km. Dress rehearsal full race kit di minggu ke-17."),
  "b6": dict(no=6, name="Taper & Race", phase=2, color="#ca8a04",
             desc="4 – 24 Okt. Volume turun bertahap, intensitas MP dijaga. Puncaknya JRF Full Marathon, Minggu 24 Okt 2027."),
}

DAYNAMES = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
KEYS = {1:"tue",3:"thu",5:"sat",6:"sun"}


# ---------------- GYM (Senin lower, Rabu upper, Jumat shoulder & core) ----------------
# Gerakan diambil dari log Hevy/Strava Ryan (alat yang tersedia di gym-nya). Menu A/B bergantian tiap minggu.
GYM_MENU = {
  0: dict(focus="Lower Body", menus={
      "A": [("Squat (Machine)",4),("Romanian Deadlift (Barbell)",4),("Bulgarian Split Squat (Dumbbell)",3),
            ("Hip Thrust (Smith Machine)",3),("Standing Calf Raise (Machine)",4),("Weighted Tibialis",3)],
      "B": [("Leg Press (Machine)",4),("Romanian Deadlift (Dumbbell)",4),("Lying Leg Curl (Machine)",3),
            ("Hip Thrust (Dumbbell)",3),("Calf Press (Machine)",4),("Weighted Tibialis",3),("Hip Abduction (Machine)",2)]}),
  2: dict(focus="Upper Body", menus={
      "A": [("Incline Chest Press (Machine)",4),("Lat Pulldown (Cable)",4),("Seated Cable Row - V Grip (Cable)",4),
            ("Chest Fly (Machine)",3),("Bicep Curl (Dumbbell)",3),("Triceps Rope Pushdown",3)],
      "B": [("Incline Bench Press (Dumbbell)",4),("Pull Up (Assisted)",4),("Bent Over Row (Barbell)",4),
            ("Chest Dip (Assisted)",3),("Bicep Curl (Cable)",3),("Triceps Extension (Dumbbell)",3)]}),
  4: dict(focus="Shoulder & Core", menus={
      "A": [("Lateral Raise (Dumbbell)",4),("Face Pull",3),("Plank",3),("Dead Bug",3),("Side Plank",3),
            ("Standing Calf Raise (Machine) — ringan",3)],
      "B": [("Lateral Raise (Dumbbell)",4),("Face Pull",3),("Lying Leg Raise",3),("Russian Twist (Bodyweight)",3),
            ("Superman",3),("Weighted Tibialis — ringan",2)]}),
}
GYM_NOTES = {
  "f1":      {0:"Fase bangun kekuatan: 8–12 rep, beban naik bertahap, sisakan 1–2 rep.",
              2:"8–12 rep, beban naik bertahap. Fokus dada & punggung (bahu dilatih Jumat).",
              4:"Bahu 12–15 rep. Core terkontrol. Aksesori kaki ringan saja, besok long run."},
  "ramadan": {0:"Ramadhan: beban turun ± 20%, jangan sampai gagal. Gym setelah berbuka/tarawih.",
              2:"Ramadhan: beban turun ± 20%, jangan sampai gagal.",
              4:"Ramadhan: ringan & terkontrol."},
  "f2":      {0:"Maintenance kekuatan: 5–8 rep berat, sisakan 2–3 rep. Jangan sampai gagal.",
              2:"Pertahankan, jangan kejar PR. Sisakan 2 rep.",
              4:"Ringan & terkontrol. Besok long run, kaki jangan capek."},
  "peak":    {0:"Blok Peak: volume dipangkas, beban tetap. Kaki harus segar untuk Kamis & long run.",
              2:"Volume dipangkas, beban tetap.",
              4:"Ringan. Besok long run terpanjang."},
  "light":   {0:"Ringan: beban ± 60%, fokus gerak. Ada race/benchmark dekat.",
              2:"Ringan: beban ± 60%.",
              4:"Ringan: fokus core & mobilitas."},
}
MOBILITY = [("Foam roll kaki (betis, paha, glute)","10 mnt"),("Mobility pinggul & ankle","10 mnt"),("Stretching ringan","5 mnt")]

def gym_sets(base, mode, dow):
    if mode == "f1": return base
    if mode == "ramadan": return max(2, min(base, 4) - 1)
    if mode == "f2": return 3 if dow == 0 else (base if dow == 4 else max(3, base - 1))
    if mode == "peak": return 2 if dow == 0 else max(2, base - 1)
    if mode == "light": return 2
    return base

# override per minggu-blok (label, dow) -> mode
GYM_OVERRIDE = {
  ("B01",0):"light", ("B01",2):"f2", ("B01",4):"light",      # minggu JAKIM
  ("B02",0):"skip",                                         # sehari setelah JAKIM HM
  ("B13",0):"light", ("B13",4):"light",                     # minggu HM Time Trial
  ("B14",0):"light",                                        # pasca HM TT
  ("B19",0):"light", ("B19",2):"light", ("B19",4):"light",
  ("B20",0):"skip",  ("B20",2):"light", ("B20",4):"skip",   # race week
}

def gym_session(label, phase, stage, dow, variant, ramadan):
    mode = GYM_OVERRIDE.get((label, dow))
    if mode is None:
        if phase == 1: mode = "ramadan" if (ramadan or stage == "ramadan") else "f1"
        elif stage in ("peak",) or label in ("B15","B16","B17","B18"): mode = "peak"
        else: mode = "f2"
    g = GYM_MENU[dow]
    if mode == "skip":
        return dict(kind="gym", focus=g["focus"], variant="—", title="Mobility & Pemulihan",
                    items=[dict(name=n, sets=v) for n, v in MOBILITY],
                    note="Tanpa beban. " + ("Pemulihan setelah race." if label == "B02" else "Race week: kaki disimpan untuk JRF."),
                    sets=0, mode=mode)
    items = [dict(name=n, sets=gym_sets(b, mode, dow)) for n, b in g["menus"][variant]]
    return dict(kind="gym", focus=g["focus"], variant=variant, title=f"{g['focus']} · Menu {variant}",
                items=items, note=GYM_NOTES[mode][dow], sets=sum(i["sets"] for i in items), mode=mode)

def build_week(start, wk, phase, label, num):
    days = []
    total = 0.0
    for i in range(7):
        d = start + dt.timedelta(days=i)
        hol = HOLIDAYS.get(d)
        ram = RAMADAN[0] <= d <= RAMADAN[1]
        entry = dict(date=d.isoformat(), dow=i, holiday=hol, ramadan=ram)
        if phase == 1 and d < D(2027,1,1):
            entry["type"] = "none"
        elif i in (0,2,4):
            if hol:
                entry["type"] = "holiday"
            else:
                entry["type"] = "gym"
                variant = "A" if (len(weeks) % 2 == 1) else "B"
                entry["session"] = gym_session(label, phase, wk["block"], i, variant, ram)
        else:
            key = KEYS[i]
            s = wk.get(key)
            weekend = i in (5,6)
            if hol and not weekend:
                assert s is None, f"Sesi di hari libur {d} {hol}"
                entry["type"] = "holiday"
            elif phase == 1 and i == 6:
                entry["type"] = "off"
            elif s is None:
                raise SystemExit(f"Hari lari kosong tanpa alasan: {d}")
            else:
                entry["type"] = "run"
                entry["session"] = s
                total += s["km"]
        days.append(entry)
    return dict(phase=phase, label=label, num=num, block=REMAP[wk["block"]], stage=STAGE[wk["block"]], start=start.isoformat(),
                end=(start + dt.timedelta(days=6)).isoformat(), total=r1(total), note=wk.get("note",""), days=days)

weeks = []
# Fase 1: W0 mulai Senin 28 Des 2026 (hanya 1–3 Jan aktif)
start = D(2026,12,28)
for n, wk in enumerate(P1):
    weeks.append(build_week(start, wk, 1, f"A{n:02d}", n))
    start += dt.timedelta(days=7)
assert start == D(2027,6,7), start
for n, wk in enumerate(P2, 1):
    weeks.append(build_week(start, wk, 2, f"B{n:02d}", n))
    start += dt.timedelta(days=7)
assert start == D(2027,10,25), start
assert len(P1) == 23 and len(P2) == 20

ZONES = [
  dict(name="Recovery", mode="HR", f1="≤ 135 bpm", f2="≤ 135 bpm", use="Recovery run Minggu (Fase B), WU & CD", color="#94a3b8"),
  dict(name="Easy (Z2)", mode="HR", f1="135–148 bpm", f2="135–148 bpm", use="Easy run Selasa. Pace referensi ± 7:15–7:45 /km (akan makin cepat seiring BB turun)", color="#22c55e"),
  dict(name="Steady / Long Run", mode="HR", f1="140–152 bpm", f2="145–155 bpm", use="Long run Sabtu. Konstan, enjoy the view", color="#0ea5e9"),
  dict(name="Marathon Pace (MP)", mode="Pace", f1="—", f2="6:55 → 6:24 /km (naik bertahap)", use="Sesi MP Kamis. HR guard 155–165. Dikalibrasi ulang setelah JAKIM & HM TT", color="#6366f1"),
  dict(name="HM Pace", mode="Pace", f1="6:00–6:10 /km", f2="5:50–6:00 /km", use="Persiapan JAKIM & HM time trial", color="#a855f7"),
  dict(name="Threshold (T)", mode="Pace", f1="5:45–6:00 /km", f2="5:35–5:50 /km", use="Cruise interval, tempo. HR guard ≤ 178", color="#f97316"),
  dict(name="Interval (I)", mode="Pace", f1="5:05–5:20 /km", f2="4:55–5:10 /km", use="Rep 800 m–1 km. HR boleh 175–185", color="#ef4444"),
  dict(name="Repetisi (R)", mode="Pace", f1="4:40–4:55 /km", f2="4:40–4:55 /km", use="Rep 200–400 m, fokus form", color="#be123c"),
  dict(name="Strides", mode="Feel", f1="± 85–90% effort", f2="± 85–90% effort", use="100 m akselerasi rileks, bukan sprint", color="#eab308"),
]

data = dict(weeks=weeks, blocks=BLOCKS, zones=ZONES,
            holidays=[dict(date=k.isoformat(), name=v) for k, v in sorted(HOLIDAYS.items())],
            ramadan=[RAMADAN[0].isoformat(), RAMADAN[1].isoformat()])

for w in weeks:
    for d in w["days"]:
        s = d.get("session")
        if s and s["kind"] == "quality" and s["target"]["mode"] == "HR":
            s["kind"] = "easy"

if __name__ == "__main__":
    import os; json.dump(data, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan.json"),"w"), ensure_ascii=False)
    tot1 = sum(w["total"] for w in weeks if w["phase"]==1)
    tot2 = sum(w["total"] for w in weeks if w["phase"]==2)
    for w in weeks:
        runs = [d["session"]["km"] for d in w["days"] if d["type"]=="run"]
        print(w["label"], w["start"], w["block"], w["total"], runs)
    print("F1", r1(tot1), "F2", r1(tot2))
