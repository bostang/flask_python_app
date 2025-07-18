Berikut adalah **panduan lengkap untuk membuat aplikasi berbasis Python menggunakan Flask** yang juga memiliki **antarmuka pengguna (UI)** berbasis HTML, CSS, dan JavaScript.

---

## 🧰 Alat yang Digunakan

* **Python** (versi 3.7 atau lebih baru)
* **Flask** – Framework backend
* **HTML/CSS/JS** – Untuk UI
* **Jinja2** – Template engine bawaan Flask
* (Opsional) Bootstrap – Untuk mempercantik tampilan

---

## 📁 Struktur Folder Sederhana

```
myapp/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
└── requirements.txt
```

---

## 1. 🔧 Instalasi & Persiapan

### a. Buat virtual environment (opsional tapi direkomendasikan)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### b. Install Flask

```bash
pip install flask
```

### c. Buat `requirements.txt`

```bash
pip freeze > requirements.txt
```

---

## 2. 🖥️ Buat File `app.py`

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. 🧩 Template HTML – `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask UI App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <h1>Welcome to My Flask App</h1>
    <form action="/submit" method="POST">
        <label for="name">Enter your name:</label>
        <input type="text" name="name" required>
        <button type="submit">Submit</button>
    </form>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

---

## 4. 🎨 File CSS – `static/css/styles.css`

```css
body {
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #f4f4f4;
}
h1 {
    color: #333;
}
```

---

## 5. 💡 File JavaScript – `static/js/script.js`

```javascript
console.log("JavaScript is working!");
```

---

## 6. ▶️ Menjalankan Aplikasi

```bash
python app.py
```

Buka browser dan akses:
👉 `http://127.0.0.1:5000/`

---

## 🧠 Tips Tambahan

* Gunakan **Flask-WTF** untuk validasi form yang lebih kompleks.
* Gunakan **Bootstrap** untuk tampilan yang lebih menarik:

  ```html
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  ```
* Untuk data dinamis, bisa gunakan **Flask-SQLAlchemy** dan database seperti SQLite atau PostgreSQL.

---

Kalau kamu ingin saya bantu membuat aplikasi dengan fitur tertentu (misalnya login, CRUD, dashboard, dll), tinggal beri tahu ya.

