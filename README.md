# Users API

API RESTful untuk manajemen pengguna yang dibangun dengan FastAPI, menampilkan autentikasi, autorisasi, dan operasi CRUD.

## 🚀 Fitur

- **Manajemen Pengguna**: Buat, baca, perbarui, dan hapus pengguna
- **Autorisasi Berbasis Peran**: Peran Admin dan Staff dengan izin berbeda
- **Keamanan Password**: Hashing password dengan BCrypt
- **Validasi Input**: Validasi skema dengan Pydantic aturan email dan password
- **Database In-memory**: Penyimpanan data sederhana (dapat diperluas ke database persisten)

## 📋 Endpoint API

### Pengguna
- `POST /users/` - Buat pengguna baru (memerlukan peran admin)
- `GET /users/` - Dapatkan semua pengguna (hanya admin)
- `GET /users/{user_id}` - Dapatkan pengguna tertentu (admin atau data sendiri untuk staff)
- `PUT /users/{user_id}` - Perbarui pengguna (admin atau data sendiri untuk staff)
- `DELETE /users/{user_id}` - Hapus pengguna (hanya admin)

## 🔐 Autentikasi & Autoriasi

API menggunakan autentikasi berbasis header:

### Header yang Diperlukan:
- `x-role`: Peran pengguna (`admin` atau `staff`)
- `x-user-id`: ID Pengguna (untuk staff yang mengakses data sendiri)

### Izin Peran:
- **Admin**: Akses penuh ke semua operasi
- **Staff**: Hanya dapat membaca dan memperbarui data mereka sendiri

## 🛠️ Instalasi

1. **Clone repository**:
```bash
git clone https://github.com/stevano27nathan/Tugas-2-Kapsel-Andat.git
cd Tugas-2-Kapsel-Andat
```

2. **Buat virtual environment**:
```bash
python -m venv .venv
# Pada Windows: .venv\Scripts\activate
# Pada macOS/Linux: source .venv/bin/activate
```

3. **Instal dependensi**:
```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Aplikasi

### Server Development:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API akan tersedia di: `http://localhost:8000`

### Akses Dokumentasi:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📝 Contoh Penggunaan API

### Buat Pengguna (Hanya admin)
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "x-role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johnstaff",
    "email": "john@example.com",
    "password": "Password123!",
    "role": "staff"
  }'
```

### Dapatkan Semua Pengguna (Hanya admin)
```bash
curl -X GET "http://localhost:8000/users/" \
  -H "x-role: admin"
```

### Dapatkan Pengguna Tertentu
```bash
curl -X GET "http://localhost:8000/users/{user_id}" \
  -H "x-role: staff" \
  -H "x-user-id: {user_id}"
```

## 🏗️ Struktur Proyek

```
Tugas-2-Kapsel-Andat/
├── main.py                 # Entry point aplikasi FastAPI
├── requirements.txt        # Dependensi Python
├── .gitignore             # Aturan ignore Git
├── modules/
│   └── users/
│       ├── routes/         # Penangan rute API
│       │   ├── createUser.py
│       │   ├── readUser.py
│       │   ├── updateUser.py
│       │   └── deleteUser.py
│       ├── schema/
│       │   └── schemas.py  # Model Pydantic
│       └── models.py       # Model data dan logika bisnis
└── README.md
```

## 🔧 Konfigurasi

### Persyaratan Password:
- Minimal 8 karakter, maksimal 20 karakter
- Setidaknya satu huruf besar
- Setidaknya satu huruf kecil  
- Setidaknya satu angka
- Setidaknya satu karakter khusus (! atau @)
- Hanya karakter yang diizinkan: huruf, angka, !, @

### Persyaratan Username:
- 6-15 karakter
- Hanya huruf kecil dan angka
- Tidak ada karakter khusus atau spasi

## 🧪 Testing

Jalankan tests dengan pytest:
```bash
pytest
```

## 📚 Dokumentasi API

Setelah server berjalan, akses dokumentasi interaktif otomatis:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## 👥 Peran dan Izin

### Admin
- ✅ Buat pengguna
- ✅ Baca semua pengguna
- ✅ Perbarui pengguna mana pun
- ✅ Hapus pengguna mana pun
- ✅ Ubah peran pengguna

### Staff  
- ❌ Buat pengguna
- ✅ Baca data sendiri saja
- ✅ Perbarui data sendiri saja
- ❌ Hapus pengguna
- ❌ Ubah peran

## 🔒 Fitur Keamanan

- Hashing password dengan BCrypt
- Validasi input dengan Pydantic
- Kontrol akses berbasis peran
- Autentikasi berbasis header
- Validasi format email

## 🚨 Penanganan Error

API mengembalikan kode status HTTP yang sesuai:
- `200` - Sukses
- `400` - Bad Request (error validasi)
- `403` - Forbidden (izin tidak cukup)
- `404` - Not Found (pengguna tidak ditemukan)
- `422` - Unprocessable Entity (header tidak lengkap)
