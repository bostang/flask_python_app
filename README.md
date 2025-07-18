# Flask Simple App

## Cara Menjalankan

**Langkah 0** : Aktifkan environtment virtual

```bash
python -m venv venv   # KALAU BELUM ADA FOLDER venv
source venv/bin/activate
```

**Langkah 1** : Buat database dengan script Python

```bash
python init_db.py
```

**Langkah 2** : Jalankan aplikasi

```bash
python app.py
```

**Langkah 3** : Akses aplikasi
Pada browser, buka : `localhost:5000`

## TO-DO

1. Buat menu login. Apabila login sebagai admin, maka bisa melakukan edit db, tetapi kalau user, hanya dapat tampilan awal.

2. setelah tuntas development, coba tanya chatGPT bagaimana bisa deploy di docker kemudian taruh di dockerhub agar mudah di docker pull orang untuk testing.

