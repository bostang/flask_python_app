import pytest
from app import app, db, User # Import aplikasi, instance db, dan model User

@pytest.fixture
def client():
    """Konfigurasi klien pengujian untuk setiap tes."""
    # Gunakan database in-memory untuk pengujian agar tidak mengganggu database asli
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Buat semua tabel untuk database in-memory
        yield client
        with app.app_context():
            db.drop_all() # Hapus semua tabel setelah tes selesai

def test_index_get(client):
    """Uji halaman utama (GET request)."""
    response = client.get('/')
    assert response.status_code == 200
    # Update this line to match actual content in index.html
    # You can pick a clear, unique phrase. "Flask Simple App" or "Simpan ke database sederhana"
    assert b"Flask Simple App" in response.data
    # Or, if you want to be more specific to the form section:
    # assert b"Masukkan Nama dan Email Anda:" in response.data

def test_index_post_add_user(client):
    """Uji penambahan user melalui POST request ke halaman utama."""
    response = client.post('/', data={
        'name': 'Test User',
        'email': 'test@example.com'
    }, follow_redirects=True) # Ikuti redirect ke /users

    assert response.status_code == 200 # Setelah redirect ke /users
    assert b"Daftar Pengguna" in response.data # Pastikan di halaman users
    assert b"Test User" in response.data # Pastikan user yang baru ditambahkan terlihat

    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.name == 'Test User'

def test_users_page(client):
    """Uji halaman daftar pengguna."""
    with app.app_context():
        # Tambahkan beberapa pengguna untuk diuji
        db.session.add(User(name='User A', email='a@example.com'))
        db.session.add(User(name='User B', email='b@example.com'))
        db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert b"User A" in response.data
    assert b"User B" in response.data

def test_submit_route(client):
    """Uji route /submit."""
    response = client.post('/submit', data={'name': 'Alice'})
    assert response.status_code == 200
    # Update this line to match actual content in greeting.html
    assert b"Hello, Alice!" in response.data


def test_delete_user(client):
    """Uji penghapusan pengguna."""
    with app.app_context():
        new_user = User(name='User Delete', email='delete@example.com')
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id # Define user_id here

    # Now user_id is accessible outside this app_context block
    response = client.get(f'/delete/{user_id}', follow_redirects=True)
    assert response.status_code == 200 # This assertion should be 200 after redirect
    assert b"Daftar Pengguna" in response.data
    assert b"User Delete" not in response.data

    with app.app_context():
        deleted_user = db.session.get(User, user_id) # user_id is available here
        assert deleted_user is None

def test_edit_user_get(client):
    """Uji tampilan halaman edit user (GET request)."""
    with app.app_context():
        new_user = User(name='User Edit', email='edit@example.com')
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id

    response = client.get(f'/edit/{user_id}')
    assert response.status_code == 200
    assert b"Edit Pengguna" in response.data # Pastikan teks dari template ada
    assert b'value="User Edit"' in response.data
    assert b'value="edit@example.com"' in response.data

def test_edit_user_post_success(client):
    """Uji pengeditan user (POST request) yang berhasil."""
    with app.app_context():
        new_user = User(name='Original Name', email='original@example.com')
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id # Define user_id here

    response = client.post(f'/edit/{user_id}', data={
        'name': 'Updated Name',
        'email': 'updated@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Daftar Pengguna" in response.data
    assert b"Updated Name" in response.data
    assert b"original@example.com" not in response.data # Email lama harusnya tidak ada

    with app.app_context():
        updated_user = db.session.get(User, user_id) # user_id is available here
        assert updated_user.name == 'Updated Name'
        assert updated_user.email == 'updated@example.com'

# def test_edit_user_post_duplicate_email(client):
#     """Uji pengeditan user dengan email yang sudah ada."""
#     with app.app_context():
#         user1 = User(name='User One', email='one@example.com')
#         user2 = User(name='User Two', email='two@example.com')
#         db.session.add_all([user1, user2])
#         db.session.commit()
#         user_id_one = user1.id
#         # user_id_two = user2.id # Ini user yang emailnya akan diduplikat

#     response = client.post(f'/edit/{user_id_one}', data={
#         'name': 'User One Edited',
#         'email': 'two@example.com' # Menggunakan email yang sudah ada
#     })
    
#     assert response.status_code == 200
#     assert b"Email sudah digunakan oleh pengguna lain." in response.data

#     with app.app_context():
#         # Pastikan data user1 tidak berubah karena email duplikat
#         original_user = User.query.get(user_id_one)
#         assert original_user.name == 'User One'
#         assert original_user.email == 'one@example.com'