from flask import Flask, redirect, url_for, render_template, request, session, jsonify,flash
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import bcrypt
import mysql.connector
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import telebot
import hashlib
import requests
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = '92b998e96f03a216ffdc613881e02934'
MERCHANT_CODE = 'DS21166'
API_KEY = '2e705cd6ec18b14774ac25cabb646d68'

# Configure the database connection
try:
    db = mysql.connector.connect(
        user="fenrir", 
        password="Journalctl@1371", 
        host="webfp-kopilucky7.mysql.database.azure.com", 
        port=3306, 
        database="db_kopi"
    )
    cursor = db.cursor(dictionary=True)
    print("Database connection established.")
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    
    
# Konfig email SMTP (menggunakan smtplib)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'kopi.lucky7@gmail.com'
EMAIL_PASSWORD = 'ijknwfrxgybzdliy '
RECIPIENT_EMAIL = 'joreljeferson@gmail.com'

logging.basicConfig(level=logging.INFO)


bot = telebot.TeleBot("7619006707:AAFu0O56AXzqaSnIL4CE2K0WoR_Mq1eMsCc")
CHAT_ID = "6656650132"  

# Fungsi untuk mengirim pesan ke Telegram
def send_message_to_telegram(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id, username, password, user_type):
        self.id = user_id
        self.username = username
        self.password = password
        self.user_type = user_type

    def is_admin(self):
        return self.user_type == 'admin'

    def is_user(self):
        return self.user_type == 'user'

@login_manager.user_loader
def load_user(user_id):
    cursor.execute('SELECT * FROM admin WHERE ID_Admin=%s', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, username, password = user_data['ID_Admin'], user_data['username'], user_data['password']
        return User(user_id, username, password, 'admin')

    cursor.execute('SELECT * FROM user WHERE ID_User=%s', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, username, password = user_data['ID_User'], user_data['username'], user_data['password']
        return User(user_id, username, password, 'user')

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cek apakah user ada di tabel admin
        cursor.execute('SELECT * FROM admin WHERE username=%s', (username,))
        admin_data = cursor.fetchone()

        if admin_data:
            print(f"Password yang disimpan di DB (admin): {admin_data['password']}")
            print(f"Password yang dimasukkan: {password}")
            
            db_password = admin_data['password']
            # Pastikan password di-encode sebagai bytes sebelum dicek dengan bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                print("Password cocok untuk admin.")
                user_id, username = admin_data['ID_Admin'], admin_data['username']
                user = User(user_id, username, db_password, 'admin')
                login_user(user)
                session['user_info'] = {
                    'user_id': user_id,
                    'username': username,
                    'user_type': 'admin'
                }
                return redirect(url_for('admin_page'))
            else:
                print("Password tidak cocok untuk admin.")

        # Cek apakah user ada di tabel user
        cursor.execute('SELECT * FROM user WHERE username=%s', (username,))
        user_data = cursor.fetchone()

        if user_data:
            print(f"Password yang disimpan di DB (user): {user_data['password']}")
            print(f"Password yang dimasukkan: {password}")
            
            db_password = user_data['password']
            # Pastikan password di-encode sebagai bytes sebelum dicek dengan bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                print("Password cocok untuk user.")
                user_id, username = user_data['ID_User'], user_data['username']
                user = User(user_id, username, db_password, 'user')
                login_user(user)
                session['user_info'] = {
                    'user_id': user_id,
                    'username': username,
                    'user_type': 'user'
                }
                return redirect(url_for('dashboard'))
            else:
                print("Password tidak cocok untuk user.")

        return 'Login gagal. Periksa kembali username dan password Anda.'

    return render_template('login.html')



@app.route('/daftar_user', methods=['POST'])
def daftar_user():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    alamat = data.get('alamat')
    email = data.get('email')

    if not all([username, password, alamat, email]):
        return jsonify({'message': 'Semua field harus diisi'}), 400

    try:
        # Menggunakan dictionary cursor dan buffered untuk memastikan semua hasil query diambil
        cursor = db.cursor(dictionary=True, buffered=True)

        # Hash password menggunakan bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Query untuk memasukkan data baru
        query = """
        INSERT INTO user (username, password, alamat, email) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password.decode('utf-8'), alamat, email))
        db.commit()

        # Redirect ke halaman login setelah berhasil
        return redirect(url_for('login'))

    except mysql.connector.Error as err:
        # Menangani error database dan mengirimkan pesan error
        return render_template('login.html', message=f"Error: {err}"), 500

    finally:
        # Pastikan cursor ditutup setelah eksekusi selesai
        if cursor:
            cursor.close()

@app.route('/admin_page')
@login_required
def admin_page():
    if not current_user.is_admin():  
        return redirect(url_for('dashboard'))  
    return render_template('admin_page.html')  

@app.route('/dashboard')
@login_required
def dashboard():
    # Admin tetap bisa mengakses halaman ini
    if current_user.is_admin():
        return render_template('dashboard.html')  # Halaman dashboard untuk admin
    elif current_user.is_user():
        return render_template('dashboard.html')  # Halaman dashboard untuk user biasa
    else:
        return redirect(url_for('login'))  # Redirect ke login jika pengguna tidak teridentifikasi


@app.route('/informasi_pengguna', methods=['GET'])
def informasi_pengguna():
    # Cek apakah pengguna sudah login (session)
    if 'user_info' in session:
        user_info = session['user_info']
        return jsonify({
            'nama_pengguna': user_info['username'],
            'user_id': user_info['user_id'],
            'user_type': user_info['user_type']
        })
    else:
        return jsonify({'error': 'User not logged in'}), 401

# Route untuk menerima POST dan mengambil data berdasarkan ID
@app.route('/get_menu', methods=['POST'])
def get_menu():
    menu_id = request.json.get('menu_id')  # Mengambil ID menu dari request POST
    
    # Pastikan ID ada
    if not menu_id:
        return jsonify({'error': 'ID menu tidak ada'}), 400
    
    # Gunakan db.cursor() dengan dictionary=True
    cursor = db.cursor(dictionary=True)

    # Query untuk mengambil data berdasarkan ID menu
    cursor.execute('SELECT * FROM menu_kopi WHERE id = %s', (menu_id,))
    menu_item = cursor.fetchone()

    cursor.close()

    if menu_item:
        return jsonify(menu_item)  # Mengirim data menu ke frontend dalam format JSON
    else:
        return jsonify({'error': 'Menu item not found'}), 404

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    
    # Ambil data dari request JSON
    user_id = data.get('user_id')  # Ambil user_id dari request
    menu_name = data.get('name')
    quantity = data.get('quantity')
    total_price = data.get('totalPrice')
    image_url = data.get('image')

    # Verifikasi jika user_id tersedia
    if not user_id:
        return jsonify({'error': 'User not logged in!'}), 400

    # Masukkan item ke dalam keranjang
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO keranjang (user_id, nama_kopi, jumlah, harga, url_gambar)
        VALUES (%s, %s, %s, %s, %s)
    ''', (user_id, menu_name, quantity, total_price, image_url))

    db.commit()

    return jsonify({'message': 'Item ditambahkan ke keranjang!'}), 200



@app.route('/get_cart', methods=['GET'])
def get_cart():
    # Ambil user_id dari session pengguna yang sedang login
    if 'user_info' not in session:
        return jsonify({'error': 'Pengguna belum login'}), 401
    
    user_id = session['user_info']['user_id']
    
    cursor = db.cursor()
    
    # Ambil data keranjang berdasarkan user_id yang sedang login
    cursor.execute('''SELECT id, nama_kopi, jumlah, harga, url_gambar FROM keranjang WHERE user_id = %s''', (user_id,))
    cart_items = cursor.fetchall()

    # Format data sebagai list of dictionaries dan hitung total harga
    cart_data = []
    for item in cart_items:
        total_harga = item[3] * item[2]  # harga * jumlah
        cart_data.append({
            'id': item[0],
            'nama_kopi': item[1],
            'jumlah': item[2],
            'harga': item[3],
            'total_harga': total_harga,
            'url_gambar': item[4]
        })

    return jsonify(cart_data)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()

    item_id = data['id']
    quantity = data['quantity']
    
    cursor = db.cursor()
    cursor.execute('SELECT harga FROM keranjang WHERE id = %s', (item_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Item tidak ditemukan'}), 404

    harga = result[0]  # Mengambil harga dari database

    if harga is None:
        return jsonify({'error': 'Harga tidak ditemukan'}), 400

    # Update jumlah item dalam keranjang tanpa menghitung total_harga di database
    cursor.execute('''UPDATE keranjang SET jumlah = %s WHERE id = %s''', 
                (quantity, item_id))
    db.commit()

    return jsonify({'message': 'Keranjang diperbarui'})


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    item_id = data['id']
    
    cursor = db.cursor()
    
    # Hapus item dari keranjang
    cursor.execute('''DELETE FROM keranjang WHERE id = %s''', (item_id,))
    db.commit()

    return jsonify({'message': 'Item berhasil dihapus dari keranjang'})

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    try:
        # Cek apakah pengguna sudah login (dengan session)
        if 'user_info' not in session:
            return jsonify({'error': 'User not logged in'}), 401

        user_info = session['user_info']
        user_id = user_info['user_id']  # Menggunakan user_id yang ada di session

        # Koneksi ke database
        cursor = db.cursor()

        # Query untuk menghapus semua item di keranjang berdasarkan user_id
        query = "DELETE FROM keranjang WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        db.commit()

        cursor.close()
        return jsonify({'message': 'Cart cleared successfully'}), 200

    except Exception as e:
        logging.error(f"Error clearing cart: {e}")
        return jsonify({'error': 'An error occurred while clearing the cart'}), 500



# Fungsi untuk menghitung signature
def generate_signature(merchant_code, merchant_order_id, payment_amount, api_key):
    data = f"{merchant_code}{merchant_order_id}{payment_amount}{api_key}"
    return hashlib.md5(data.encode()).hexdigest()

@app.route('/duitku/transaction', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()

        # Tambahkan logging untuk memeriksa data yang diterima
        logging.info(f"Received data for transaction: {data}")

        # Periksa apakah 'paymentAmount' ada di dalam data
        if 'paymentAmount' not in data:
            logging.error("Missing 'paymentAmount' in request data")
            return jsonify({'error': "'paymentAmount' is required"}), 400
        
        # Hitung signature
        signature = generate_signature(MERCHANT_CODE, data['merchantOrderId'], data['paymentAmount'], API_KEY)

        # Tambahkan signature ke data payload
        params = {
            'merchantCode': MERCHANT_CODE,
            'paymentAmount': data['paymentAmount'],
            'paymentMethod': data['paymentMethod'],
            'merchantOrderId': data['merchantOrderId'],
            'productDetails': data['productDetails'],
            'customerVaName': data['customerVaName'],
            'email': data['email'],
            'phoneNumber': data['phoneNumber'],
            'callbackUrl': data['callbackUrl'],
            'returnUrl': data['returnUrl'],
            'signature': signature,
            'expiryPeriod': data.get('expiryPeriod', 10)
        }

        # Kirim permintaan ke endpoint transaksi Duitku
        url = 'https://sandbox.duitku.com/webapi/api/merchant/v2/inquiry'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(params), headers=headers, verify=False)

        if response.status_code == 200:
            result = response.json()
            logging.info(f"Transaction result: {result}")

            # Simpan transaksi ke database
            cursor = db.cursor()
            query = """
                INSERT INTO transaksi (transaction_no, nama_pelanggan, total_harga, metode_pembayaran, waktu_transaksi, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (data['merchantOrderId'], data['customerVaName'], data['paymentAmount'], data['paymentMethod'], datetime.now(), "Proses"))
            db.commit()
            cursor.close()

            # Kirim URL pembayaran ke frontend
            return jsonify({
                "statusCode": result.get('statusCode', ''),
                "statusMessage": result.get('statusMessage', ''),
                "paymentUrl": result.get('paymentUrl')
            }), 200
        else:
            logging.error(f"Failed to create transaction, response: {response.text}")
            return jsonify({'error': 'Failed to create transaction', 'status_code': response.status_code, 'message': response.text}), 400

    except Exception as e:
        logging.error(f"Error creating transaction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/duitku/callback', methods=['POST'])
def duitku_callback():
    try:
        data = request.form  # Data dari callback

        # Ambil semua parameter penting dari data
        merchant_code = data.get('merchantCode')
        amount = data.get('amount')
        merchant_order_id = data.get('merchantOrderId')
        result_code = data.get('resultCode')
        signature = data.get('signature')
        product_details = data.get('productDetails')
        additional_param = data.get('additionalParam')
        payment_code = data.get('paymentCode')
        merchant_user_id = data.get('merchantUserId')
        reference = data.get('reference')
        publisher_order_id = data.get('publisherOrderId')
        sp_user_hash = data.get('spUserHash')
        settlement_date = data.get('settlementDate')
        issuer_code = data.get('issuerCode')

        # Validasi signature
        calculated_signature = hashlib.md5(
            f"{merchant_code}{amount}{merchant_order_id}{API_KEY}".encode()
        ).hexdigest()

        if signature == calculated_signature:
            # Tentukan status berdasarkan resultCode
            status_message = "Transaksi berhasil diproses!" if result_code == "00" else "Transaksi gagal."
            status_class = "success" if result_code == "00" else "failed"

            # Log detail transaksi untuk debugging
            logging.info(f"""
            Callback Received:
            Merchant Order ID: {merchant_order_id}
            Amount: {amount}
            Product Details: {product_details}
            Payment Code: {payment_code}
            Additional Param: {additional_param}
            Reference: {reference}
            Publisher Order ID: {publisher_order_id}
            SP User Hash: {sp_user_hash}
            Settlement Date: {settlement_date}
            Issuer Code: {issuer_code}
            """)

        else:
            status_message = "Signature tidak valid."
            status_class = "failed"
            merchant_order_id = "Tidak tersedia"

        # Tampilkan halaman callback
        redirect_url = f"/duitku/redirect?merchantOrderId={merchant_order_id}&resultCode={result_code}"
        return render_template(
            'callback.html', 
            status_message=status_message, 
            status_class=status_class, 
            merchant_order_id=merchant_order_id, 
            redirect_url=redirect_url
        )

    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        return "Error processing callback", 500

@app.route('/duitku/redirect', methods=['GET'])
def duitku_redirect():
    # Ambil parameter dari URL
    merchant_order_id = request.args.get('merchantOrderId')
    result_code = request.args.get('resultCode')
    reference = request.args.get('reference')

    # Log untuk debugging
    logging.info(f"Redirect received: merchantOrderId={merchant_order_id}, resultCode={result_code}, reference={reference}")

    # Validasi data
    if not merchant_order_id or not result_code or not reference:
        return "Invalid redirect parameters", 400

    # Periksa apakah transaksi berhasil
    if result_code == "00":
        # Update status transaksi di database
        cursor = db.cursor()
        query = """
            UPDATE transaksi
            SET status = 'Selesai'
            WHERE transaction_no = %s
        """
        cursor.execute(query, (merchant_order_id,))
        db.commit()
        cursor.close()

        # Tampilkan halaman sukses
        return render_template('success.html', reference=reference, merchant_order_id=merchant_order_id)
    else:
        # Update status transaksi di database sebagai "Gagal"
        cursor = db.cursor()
        query = """
            UPDATE transaksi
            SET status = 'Gagal'
            WHERE transaction_no = %s
        """
        cursor.execute(query, (merchant_order_id,))
        db.commit()
        cursor.close()

        # Tampilkan halaman gagal
        return render_template('failure.html', message="Transaksi gagal. Silakan coba lagi.")


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    # Mengambil informasi pengguna yang sedang login
    user_info = session.get('user_info')

    if not user_info:
        return jsonify({'error': 'User not logged in'}), 401

    # Mendapatkan nama pengguna dari session
    nama_pengguna = user_info['username']
    
    # Koneksi ke database
    cursor = db.cursor(dictionary=True)

    # Query untuk mengambil transaksi berdasarkan nama pengguna yang sedang login
    query = """
        SELECT id, transaction_no, nama_pelanggan, metode_pembayaran, waktu_transaksi, total_harga, status
        FROM transaksi
        WHERE nama_pelanggan = %s
    """
    cursor.execute(query, (nama_pengguna,))
    transactions = cursor.fetchall()

    # Mengubah hasil transaksi menjadi list of dictionaries
    transaction_list = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction['id'],
            'transaction_no': transaction['transaction_no'],  # Tambahkan kolom transaction_no
            'nama_pelanggan': transaction['nama_pelanggan'],
            'metode_pembayaran': transaction['metode_pembayaran'],
            'waktu_transaksi': transaction['waktu_transaksi'].strftime('%Y-%m-%d %H:%M:%S') if transaction['waktu_transaksi'] else None,
            'total_harga': transaction['total_harga'],
            'status': transaction['status']
        }
        transaction_list.append(transaction_data)

    cursor.close()

    # Mengirimkan data transaksi dalam format JSON
    return jsonify({'transactions': transaction_list})


@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.form
    username = data.get('username')  # Menggunakan username sebagai identifikasi
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    # Validasi input
    if not all([username, new_password, confirm_password]):
        return jsonify({'message': 'Semua field harus diisi'}), 400

    if new_password != confirm_password:
        return jsonify({'message': 'Password tidak cocok'}), 400

    try:
        cursor = db.cursor()

        # Hash password baru menggunakan bcrypt
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Query untuk memperbarui password berdasarkan username
        query = """
        UPDATE user
        SET password_hash = %s 
        WHERE username = %s
        """
        cursor.execute(query, (hashed_password.decode('utf-8'), username))
        db.commit()

        if cursor.rowcount == 0:
            return render_template('login.html', message="Username tidak ditemukan"), 404

        # Redirect ke halaman login setelah berhasil
        return redirect(url_for('login'))

    except mysql.connector.Error as err:
        return render_template('login.html', message=f"Error: {err}"), 500

    finally:
        cursor.close()

@app.route('/cetak_resi', methods=['POST'])
def cetak_resi():
    try:
        # Ambil data username yang dikirim dari frontend melalui AJAX
        data = request.get_json()
        username = data.get('username')  # Mengambil username, bukan user_id

        if not username:
            return jsonify({"error": "Username tidak ditemukan"}), 400

        # Koneksi ke database
        cursor = db.cursor(dictionary=True)

        # Ambil transaksi yang sesuai dengan username
        query = """
        SELECT * FROM transaksi WHERE nama_pelanggan = %s
        """
        cursor.execute(query, (username,))
        transactions = cursor.fetchall()

        if not transactions:
            return jsonify({"error": "Tidak ada transaksi ditemukan"}), 404

        # Menambahkan perhitungan total harga
        total_harga = 0  # Variabel untuk menyimpan total harga yang perlu dibayar
        for transaction in transactions:
            total_harga += transaction['total_harga']  # Cukup jumlahkan total_harga saja, tanpa mempertimbangkan jumlah

        # Menghasilkan ID transaksi acak 6 digit
        random_transaction_id = random.randint(100000, 999999)

        # Debugging log
        print("Data transaksi:", transactions)  # Menampilkan data transaksi di log

        # Render HTML untuk faktur
        rendered_html = render_template('cetak_resi.html', transactions=transactions, 
                                    transaction_id=random_transaction_id, total_harga=total_harga)
        return rendered_html

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()

@app.route('/contact_send', methods=['GET', 'POST'])
def contact_send():
    if request.method == 'POST':
        # Mengambil data dari form
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            # Koneksi ke database
            cursor = db.cursor(dictionary=True)
            cursor.execute('INSERT INTO contact (name, phone, email, message) VALUES (%s, %s, %s, %s)', 
                        (name, phone, email, message))
            db.commit()
            cursor.close()

            # Kirim email menggunakan smtplib
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = 'Laporan Email Kopi Lucky 7'

            body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
            server.quit()

            logging.info("Email sent successfully.")
            flash('Pesan Anda telah berhasil dikirim!', 'success')
        except Exception as e:
            logging.error(f"Failed to process the request: {e}")
            flash('Terjadi kesalahan saat memproses permintaan. Silakan coba lagi.', 'danger')

        # Render ulang halaman dengan pesan flash
        return render_template('contact.html')



@app.route('/komplain', methods=['POST'])
def komplain():
    cursor = db.cursor()

    # Mengambil data dari form
    nama = request.form['nama']
    jenis_keluhan = request.form['jenis_keluhan']
    isi_keluhan = request.form['isi_keluhan']
    
    id = f"#{random.randint(100000, 999999)}"
    
    try:
        cursor.execute("""
            INSERT INTO komplain (id, nama, jenis_keluhan, isi_keluhan)
            VALUES (%s, %s, %s, %s)
        """, (id, nama, jenis_keluhan, isi_keluhan))
        db.commit()
        cursor.close()

        # Kirim laporan ke Telegram
        message = f"Laporan Komplain Pelanggan Lucky 7!\n\nID Report: {id}\nNama: {nama}\nJenis Keluhan: {jenis_keluhan}\nIsi Keluhan: {isi_keluhan}"
        bot.send_message(chat_id=CHAT_ID, text=message)

        flash('Komplain Anda berhasil dikirim!', 'success')
    except Exception as e:
        logging.error(f"Error saat memproses komplain: {e}")
        flash('Terjadi kesalahan saat mengirim komplain. Silakan coba lagi.', 'danger')

    return render_template('support.html')

# ====== CRUD untuk User ======
@app.route("/users", methods=["GET"])
def get_users():
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    logging.debug(f"Data diterima: {data}")

    # Hash password menggunakan bcrypt
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    with db.cursor(dictionary=True, buffered=True) as cursor:
        query = "INSERT INTO user (username, password, alamat, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data["username"], hashed_password.decode('utf-8'), data["alamat"], data["email"]))
        db.commit()

    return jsonify({"message": "User berhasil ditambahkan!"})

@app.route("/users/<int:id_user>", methods=["DELETE"])
def delete_user(id_user):
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("DELETE FROM user WHERE ID_User = %s", (id_user,))
        db.commit()
    return jsonify({"message": f"User dengan ID {id_user} berhasil dihapus!"})

# ====== CRUD untuk Admin ======
@app.route("/admins", methods=["GET"])
def get_admins():
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM admin")
        admins = cursor.fetchall()
    return jsonify(admins)

@app.route("/admins", methods=["POST"])
def add_admin():
    data = request.json

    # Hash password menggunakan bcrypt
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    with db.cursor(dictionary=True, buffered=True) as cursor:
        query = "INSERT INTO admin (username, password, alamat, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data["username"], hashed_password.decode('utf-8'), data["alamat"], data["email"]))
        db.commit()

    return jsonify({"message": "Admin berhasil ditambahkan!"})

@app.route("/admins/<int:id_admin>", methods=["DELETE"])
def delete_admin(id_admin):
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("DELETE FROM admin WHERE ID_Admin = %s", (id_admin,))
        db.commit()
    return jsonify({"message": f"Admin dengan ID {id_admin} berhasil dihapus!"})

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logout pengguna
    session.pop('user_info', None)  # Hapus informasi sesi
    return redirect(url_for('login'))  # Redirect ke halaman login setelah logout

@app.route('/keranjang')
@login_required
def keranjang():
    # Logika untuk keranjang
    return render_template('keranjang.html')

@app.route('/status_pemesanan')
@login_required
def status_pemesanan():
    # Logika untuk halaman status pemesanan
    return render_template('status_pemesanan.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/forget')
def forget():
    return render_template('forget.html')

@app.route('/daftar')
def daftar():
    return render_template('daftar.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/callback')
def callback():
    return render_template('callback.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
