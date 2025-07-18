#!/bin/bash

# Langkah 0: Aktivasi environoment Python
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Langkah 1: Inisialisasi database
#echo "📦 Membuat database..."
#python3 init_db.py

# Langkah 2: Jalankan aplikasi Flask
echo "🚀 Menjalankan aplikasi Flask..."
# Jalankan di background (opsional), simpan PID
python3 app.py &

# Simpan PID proses untuk nanti bisa dihentikan
FLASK_PID=$!

# Tunggu sebentar agar server siap
sleep 2

# Langkah 3: Buka aplikasi di browser default
echo "🌐 Membuka http://127.0.0.1:5000/"
xdg-open http://127.0.0.1:5000/ 2>/dev/null || open http://127.0.0.1:5000/ 2>/dev/null || start http://127.0.0.1:5000/

# Opsional: Tunggu Flask sampai dihentikan (Ctrl+C)
wait $FLASK_PID

