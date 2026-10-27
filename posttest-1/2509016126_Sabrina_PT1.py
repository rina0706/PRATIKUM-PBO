# ============================================================
# SISTEM PENDATAAN MENU DI RESTORAN SUSHI
# ============================================================

class MenuSushi:
    nama_restoran = "Sushi Ten"
    total_menu_terdaftar = 0
    pajak_persen = 10 

    def __init__(self, nama, harga, stok, kategori):
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.__stok = stok
        MenuSushi.total_menu_terdaftar += 1

    def tampilkan_info(self):
        print(f"[{self.kategori}] {self.nama} | Harga: Rp{self.harga:,} | Stok: {self.__stok}")

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            print("Jumlah pengurangan tidak valid.")
        elif jumlah > self.__stok:
            print(f"Stok {self.nama} tidak cukup.")
        else:
            self.__stok -= jumlah
            print(f"Stok {self.nama} berkurang {jumlah}. Sisa: {self.__stok}")

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai_baru):
        if nilai_baru < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self.__stok = nilai_baru
 
    @classmethod
    def dari_dict(cls, data):
        return cls(data["nama"], data["harga"], data["stok"], data["kategori"])

    @classmethod
    def ubah_pajak(cls, pajak_baru):
        if pajak_baru < 0:
            raise ValueError("Pajak tidak boleh negatif!")
        cls.pajak_persen = pajak_baru

    @staticmethod
    def validasi_nama_menu(nama):
        return isinstance(nama, str) and len(nama.strip()) >= 3

    @staticmethod
    def hitung_harga_setelah_pajak(harga):
        return int(harga * (1 + MenuSushi.pajak_persen / 100))

class Pesanan:
    nomor_pesanan_terakhir = 0
    status_default = "Menunggu"

    def __init__(self, nama_pelanggan, menu, jumlah):
        Pesanan.nomor_pesanan_terakhir += 1
        self.id_pesanan = Pesanan.nomor_pesanan_terakhir
        self.nama_pelanggan = nama_pelanggan
        self.menu = menu
        self.jumlah = jumlah
        self.status = Pesanan.status_default
        self.__total_bayar = 0

    def hitung_total(self):
        total = self.menu.harga * self.jumlah
        self.__total_bayar = MenuSushi.hitung_harga_setelah_pajak(total)
        return self.__total_bayar

    def proses_pesanan(self):
        if self.menu.stok >= self.jumlah:
            self.menu.kurangi_stok(self.jumlah)
            self.status = "Diproses"
            print(f"Pesanan #{self.id_pesanan} sedang diproses.")
        else:
            print(f"Pesanan #{self.id_pesanan} gagal: stok tidak cukup.")

    def tampilkan_pesanan(self):
        print(f"Pesanan #{self.id_pesanan} | {self.nama_pelanggan} | "
              f"{self.menu.nama} x{self.jumlah} | Status: {self.status} | "
              f"Total: Rp{self.__total_bayar:,}")
        
    @property
    def total_bayar(self):
        return self.__total_bayar

    @total_bayar.setter
    def total_bayar(self, nilai):
        if nilai < 0:
            raise ValueError("Total bayar tidak boleh negatif!")
        self.__total_bayar = nilai

    @classmethod
    def dari_dict(cls, data, daftar_menu):
        menu_ditemukan = None
        for m in daftar_menu:
            if m.nama.lower() == data["menu"].lower():
                menu_ditemukan = m
                break
        if menu_ditemukan is None:
            raise ValueError(f"Menu '{data['menu']}' tidak ditemukan.")
        return cls(data["pelanggan"], menu_ditemukan, data["jumlah"])

    @classmethod
    def reset_nomor_pesanan(cls):
        cls.nomor_pesanan_terakhir = 0

    @staticmethod
    def validasi_jumlah(jumlah):
        return isinstance(jumlah, int) and jumlah > 0

class Kasir:
    nama_instansi = "Sushi Ten Resto"
    total_transaksi = 0
    __pin_rahasia = "1234"

    def __init__(self, nama_kasir, shift):
        self.nama_kasir = nama_kasir
        self.shift = shift
        self.__saldo_kas = 0

    def terima_pembayaran(self, pesanan):
        total = pesanan.hitung_total()
        self.__saldo_kas += total
        Kasir.total_transaksi += 1
        pesanan.status = "Selesai"
        print(f"Kasir {self.nama_kasir} menerima Rp{total:,} dari pesanan #{pesanan.id_pesanan}")

    def tampilkan_saldo(self):
        print(f"Saldo kas {self.nama_kasir} (shift {self.shift}): Rp{self.__saldo_kas:,}")

    @property
    def saldo_kas(self):
        return self.__saldo_kas

    @saldo_kas.setter
    def saldo_kas(self, nilai):
        if nilai < 0:
            raise ValueError("Saldo kas tidak boleh negatif!")
        self.__saldo_kas = nilai

    @classmethod
    def dari_dict(cls, data):
        return cls(data["nama"], data["shift"])

    @classmethod
    def cek_pin(cls, pin):
        return pin == cls.__pin_rahasia

    @staticmethod
    def format_rupiah(angka):
        return f"Rp{angka:,}".replace(",", ".")

    @staticmethod
    def validasi_shift(shift):
        return shift.lower() in ["pagi", "siang", "malam"]

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEM PENDATAAN MENU DI RESTORAN SUSHI")
    print("=" * 60)

    print("\n--- 1. Membuat Objek MenuSushi ---")
    menu1 = MenuSushi("Salmon Nigiri", 35000, 20, "Nigiri")
    menu2 = MenuSushi("Tuna Maki", 25000, 15, "Maki")
    menu3 = MenuSushi.dari_dict({
        "nama": "Dragon Roll",
        "harga": 55000,
        "stok": 10,
        "kategori": "Roll"
    })

    menu1.tampilkan_info()
    menu2.tampilkan_info()
    menu3.tampilkan_info()

    print("\n--- 2. Membuat Objek Pesanan ---")
    pesanan1 = Pesanan("Andi", menu1, 2)
    pesanan2 = Pesanan.dari_dict(
        {"pelanggan": "Budi", "menu": "Tuna Maki", "jumlah": 3},
        [menu1, menu2, menu3]
    )

    pesanan1.proses_pesanan()
    pesanan2.proses_pesanan()

    pesanan1.hitung_total()
    pesanan2.hitung_total()
    pesanan1.tampilkan_pesanan()
    pesanan2.tampilkan_pesanan()

    print("\n--- 3. Membuat Objek Kasir ---")
    kasir1 = Kasir("Siti", "Pagi")
    kasir2 = Kasir.dari_dict({"nama": "Rina", "shift": "Malam"})

    kasir1.terima_pembayaran(pesanan1)
    kasir2.terima_pembayaran(pesanan2)

    kasir1.tampilkan_saldo()
    kasir2.tampilkan_saldo()

    print("\n--- 4. Uji Class Method ---")
    print(f"Total menu terdaftar: {MenuSushi.total_menu_terdaftar}")
    print(f"Pajak sebelum diubah: {MenuSushi.pajak_persen}%")
    MenuSushi.ubah_pajak(15)
    print(f"Pajak setelah diubah: {MenuSushi.pajak_persen}%")
    print(f"Total transaksi: {Kasir.total_transaksi}")
    print(f"Cek PIN '1234': {Kasir.cek_pin('1234')}")
    print(f"Cek PIN '9999': {Kasir.cek_pin('9999')}")

    print("\n--- 5. Uji Static Method ---")
    print(f"Validasi nama 'Salmon' : {MenuSushi.validasi_nama_menu('Salmon')}")
    print(f"Validasi nama 'ab'     : {MenuSushi.validasi_nama_menu('ab')}")
    print(f"Harga 35000 + pajak    : {MenuSushi.hitung_harga_setelah_pajak(35000)}")
    print(f"Validasi jumlah 3      : {Pesanan.validasi_jumlah(3)}")
    print(f"Validasi jumlah -1     : {Pesanan.validasi_jumlah(-1)}")
    print(f"Validasi shift 'Pagi'  : {Kasir.validasi_shift('Pagi')}")
    print(f"Format rupiah 150000   : {Kasir.format_rupiah(150000)}")

    print("\n--- 6. Uji Getter & Setter ---")
    print(f"Stok awal menu1: {menu1.stok}")
    menu1.stok = 30
    print(f"Stok menu1 setelah set valid (30): {menu1.stok}")

    try:
        menu1.stok = -5
    except ValueError as e:
        print(f"Error saat set stok -5: {e}")

    pesanan1.total_bayar = 100000
    print(f"Total bayar pesanan1 setelah set valid: {pesanan1.total_bayar}")

    try:
        pesanan1.total_bayar = -1000
    except ValueError as e:
        print(f"Error saat set total bayar -1000: {e}")

    kasir1.saldo_kas = 500000
    print(f"Saldo kasir1 setelah set valid: {kasir1.saldo_kas}")

    try:
        kasir1.saldo_kas = -50000
    except ValueError as e:
        print(f"Error saat set saldo kas -50000: {e}")

    print("\n" + "=" * 60)
    print("PROGRAM SELESAI")
    print("=" * 60)