from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db = SQLAlchemy(app)

# Model data pengguna
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)      # deprecated
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.name}>'

# Halaman utama (form input)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users'))
        except:
            return "Terjadi kesalahan saat menyimpan data."

    return render_template('index.html')


# Halaman daftar pengguna
@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# Tampilkan pesan hello
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    return render_template('greeting.html', name=name)

#  Route untuk Hapus User
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    # user_to_delete = User.query.get_or_404(user_id)
        # SQLAlchemy 2.0 prefers session.get() over Query.get()
    user_to_delete = db.session.get(User, user_id)
    if not user_to_delete: # Add a check if user not found
        return "Pengguna tidak ditemukan.", 404

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('users'))
    except:
        return "Terjadi kesalahan saat menghapus data."

# Route untuk Edit User
# In app.py, inside the edit_user route
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return "Pengguna tidak ditemukan.", 404

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']

        try:
            # Cek apakah email digunakan oleh user lain (excluding the current user)
            existing_user = User.query.filter(User.email == user.email, User.id != user.id).first()
            if existing_user:
                # *** THIS IS THE CRITICAL CHANGE ***
                return "Email sudah digunakan oleh pengguna lain."
            
            db.session.commit()
            return redirect(url_for('users'))
        
        except Exception as e:
            # This 'except' block will catch other potential database errors.
            # Keep it generic or make it more specific if you anticipate other types of errors.
            return "Terjadi kesalahan saat mengubah data."

    return render_template('edit.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)