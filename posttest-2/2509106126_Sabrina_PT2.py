class MenuSushi:
    nama_restoran = "Sushi Ten"
    total_menu_terdaftar = 0
    pajak_persen = 10

    __kode_internal_resto = "ST-INTERNAL-001"

    def __init__(self, nama, harga, stok, kategori):
        self.nama = nama
        self.harga = harga
        self.kategori = kategori
        self._stok = stok
        self.__kode_menu = f"MENU-{MenuSushi.total_menu_terdaftar + 1:03d}"
        MenuSushi.total_menu_terdaftar += 1

    def tampilkan_info(self):
        print(f"[{self.kategori}] {self.nama} | Harga: Rp{self.harga:,} | Stok: {self._stok}")

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            print("Jumlah pengurangan tidak valid.")
        elif jumlah > self._stok:
            print(f"Stok {self.nama} tidak cukup.")
        else:
            self._stok -= jumlah
            print(f"Stok {self.nama} berkurang {jumlah}. Sisa: {self._stok}")

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai_baru):
        if nilai_baru < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self._stok = nilai_baru

    @classmethod
    def dari_dict(cls, data):
        return cls(data["nama"], data["harga"], data["stok"], data["kategori"])

    @classmethod
    def ubah_pajak(cls, pajak_baru):
        if pajak_baru < 0:
            raise ValueError("Pajak tidak boleh negatif!")
        cls.pajak_persen = pajak_baru

    @classmethod
    def cek_kode_internal(cls, kode):
        return kode == cls.__kode_internal_resto

    @staticmethod
    def validasi_nama_menu(nama):
        return isinstance(nama, str) and len(nama.strip()) >= 3

    @staticmethod
    def hitung_harga_setelah_pajak(harga):
        return int(harga * (1 + MenuSushi.pajak_persen / 100))


class SushiNigiri(MenuSushi):
    def __init__(self, nama, harga, stok, jenis_ikan, is_premium=False):
        super().__init__(nama, harga, stok, "Nigiri")
        self.jenis_ikan = jenis_ikan
        self.is_premium = is_premium

    def tampilkan_info(self):
        status = "PREMIUM" if self.is_premium else "Reguler"
        print(f"[{self.kategori}] {self.nama} ({self.jenis_ikan}) | "
              f"Harga: Rp{self.harga:,} | Stok: {self._stok} | {status}")

    def cek_kualitas(self):
        if self.is_premium and self.jenis_ikan.lower() in ["salmon", "tuna", "uni"]:
            print(f"{self.nama} kualitas ekspor - layak disajikan.")
        else:
            print(f"{self.nama} kualitas standar.")


class SushiRoll(MenuSushi):
    def __init__(self, nama, harga, stok, jumlah_potongan, saus_khas):
        super().__init__(nama, harga, stok, "Roll")
        self.jumlah_potongan = jumlah_potongan
        self.saus_khas = saus_khas

    def tampilkan_info(self):
        print(f"[{self.kategori}] {self.nama} | {self.jumlah_potongan} potong | "
              f"Saus: {self.saus_khas} | Harga: Rp{self.harga:,} | Stok: {self._stok}")

    def bagi_potongan(self, jumlah_orang):
        if jumlah_orang <= 0:
            print("Jumlah orang tidak valid.")
        else:
            per_orang = self.jumlah_potongan // jumlah_orang
            print(f"{self.nama} dibagi {jumlah_orang} orang = {per_orang} potong/orang.")


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


class DaftarMenu:
    nama_instansi = "Sushi Ten Resto"
    total_daftar = 0

    def __init__(self, nama_daftar):
        self.nama_daftar = nama_daftar
        self._koleksi_menu = []
        self.__total_harga_semua = 0
        DaftarMenu.total_daftar += 1

    def tambah_menu(self, menu):
        if isinstance(menu, MenuSushi):
            self._koleksi_menu.append(menu)
            self.__total_harga_semua += menu.harga
            print(f"[+] {menu.nama} ditambahkan ke {self.nama_daftar}")
        else:
            print("Objek bukan MenuSushi, tidak bisa ditambahkan.")

    def hapus_menu(self, nama_menu):
        awal = len(self._koleksi_menu)
        self._koleksi_menu = [
            m for m in self._koleksi_menu if m.nama.lower() != nama_menu.lower()
        ]
        if len(self._koleksi_menu) < awal:
            print(f"[-] {nama_menu} dihapus dari {self.nama_daftar}")
        else:
            print(f"Menu {nama_menu} tidak ditemukan.")

    def tampilkan_semua(self):
        print(f"\n=== Daftar Menu: {self.nama_daftar} ===")
        for i, m in enumerate(self._koleksi_menu, 1):
            print(f"{i}. ", end="")
            m.tampilkan_info()

    @property
    def total_harga_semua(self):
        return self.__total_harga_semua

    @total_harga_semua.setter
    def total_harga_semua(self, nilai):
        if nilai < 0:
            raise ValueError("Total harga tidak boleh negatif!")
        self.__total_harga_semua = nilai

    @classmethod
    def dari_dict(cls, data):
        return cls(data["nama_daftar"])

    @staticmethod
    def validasi_nama_daftar(nama):
        return isinstance(nama, str) and len(nama.strip()) >= 3


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


class RiwayatTransaksi:
    def __init__(self, id_trx, nama_pelanggan, total):
        self.id_trx = id_trx
        self.nama_pelanggan = nama_pelanggan
        self.total = total

    def __str__(self):
        return f"[{self.id_trx}] {self.nama_pelanggan} - Rp{self.total:,}"


class KasirDenganRiwayat(Kasir):
    def __init__(self, nama_kasir, shift):
        super().__init__(nama_kasir, shift)
        self._riwayat = []
        self._counter_trx = 0

    def _buat_riwayat(self, nama_pelanggan, total):
        self._counter_trx += 1
        id_trx = f"TRX-{self._counter_trx:04d}"
        trx = RiwayatTransaksi(id_trx, nama_pelanggan, total)
        self._riwayat.append(trx)

    def terima_pembayaran(self, pesanan):
        super().terima_pembayaran(pesanan)
        self._buat_riwayat(pesanan.nama_pelanggan, pesanan.total_bayar)

    def cetak_riwayat(self):
        print(f"\nRiwayat transaksi kasir {self.nama_kasir}:")
        for trx in self._riwayat:
            print(f"  {trx}")


if __name__ == "__main__":
    print("=" * 60)
    print("SISTEM PENDATAAN MENU DI RESTORAN SUSHI")
    print("=" * 60)

    print("\n--- 1. Membuat Objek MenuSushi & Subclass-nya ---")
    menu_umum = MenuSushi("Edamame", 15000, 30, "Side Dish")
    nigiri1 = SushiNigiri("Salmon Nigiri", 35000, 20, "Salmon", is_premium=True)
    nigiri2 = SushiNigiri("Tuna Nigiri", 30000, 15, "Tuna")
    roll1 = SushiRoll("Dragon Roll", 55000, 10, 8, "Spicy Mayo")
    roll2 = SushiRoll("California Roll", 45000, 12, 6, "Wasabi")

    menu_umum.tampilkan_info()
    nigiri1.tampilkan_info()
    nigiri2.tampilkan_info()
    roll1.tampilkan_info()
    roll2.tampilkan_info()

    print("\n--- 2. Method Unik Subclass ---")
    nigiri1.cek_kualitas()
    nigiri2.cek_kualitas()
    roll1.bagi_potongan(4)
    roll2.bagi_potongan(3)

    print("\n--- 3. Class Method & Static Method ---")
    print(f"Total menu terdaftar: {MenuSushi.total_menu_terdaftar}")
    print(f"Pajak awal: {MenuSushi.pajak_persen}%")
    MenuSushi.ubah_pajak(15)
    print(f"Pajak setelah diubah: {MenuSushi.pajak_persen}%")
    print(f"Cek kode internal 'ST-INTERNAL-001': {MenuSushi.cek_kode_internal('ST-INTERNAL-001')}")
    print(f"Cek kode internal 'salah': {MenuSushi.cek_kode_internal('salah')}")
    print(f"Validasi nama 'Salmon': {MenuSushi.validasi_nama_menu('Salmon')}")
    print(f"Validasi nama 'ab': {MenuSushi.validasi_nama_menu('ab')}")

    print("\n--- 4. Agregasi: DaftarMenu ---")
    daftar = DaftarMenu("Menu Utama")
    daftar.tambah_menu(menu_umum)
    daftar.tambah_menu(nigiri1)
    daftar.tambah_menu(nigiri2)
    daftar.tambah_menu(roll1)
    daftar.tambah_menu(roll2)
    daftar.tampilkan_semua()
    print(f"Total harga semua menu: Rp{daftar.total_harga_semua:,}")
    daftar.hapus_menu("Edamame")
    daftar.tampilkan_semua()

    print("\n--- 5. Asosiasi: Pesanan ---")
    pesanan1 = Pesanan("Andi", nigiri1, 2)
    pesanan2 = Pesanan("Budi", roll1, 1)

    pesanan1.proses_pesanan()
    pesanan2.proses_pesanan()
    pesanan1.hitung_total()
    pesanan2.hitung_total()
    pesanan1.tampilkan_pesanan()
    pesanan2.tampilkan_pesanan()

    print("\n--- 6. Komposisi: Kasir & RiwayatTransaksi ---")
    kasir = KasirDenganRiwayat("Siti", "Pagi")
    kasir.terima_pembayaran(pesanan1)
    kasir.terima_pembayaran(pesanan2)
    kasir.tampilkan_saldo()
    kasir.cetak_riwayat()

    print("\n--- 7. Uji Getter & Setter ---")
    print(f"Stok awal nigiri1: {nigiri1.stok}")
    nigiri1.stok = 30
    print(f"Stok setelah set valid (30): {nigiri1.stok}")

    try:
        nigiri1.stok = -5
    except ValueError as e:
        print(f"Error set stok -5: {e}")

    print(f"Saldo kas awal: {kasir.saldo_kas}")
    kasir.saldo_kas = 500000
    print(f"Saldo setelah set valid: {kasir.saldo_kas}")

    try:
        kasir.saldo_kas = -50000
    except ValueError as e:
        print(f"Error set saldo -50000: {e}")

    print("\n--- 8. Cek Pewarisan ---")
    print(f"nigiri1 adalah MenuSushi? {isinstance(nigiri1, MenuSushi)}")
    print(f"nigiri1 adalah SushiRoll? {isinstance(nigiri1, SushiRoll)}")
    print(f"SushiNigiri subclass MenuSushi? {issubclass(SushiNigiri, MenuSushi)}")
    print(f"SushiRoll subclass MenuSushi? {issubclass(SushiRoll, MenuSushi)}")

    print("\n" + "=" * 60)
    print("PROGRAM SELESAI")
    print("=" * 60)