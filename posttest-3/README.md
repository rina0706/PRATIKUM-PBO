# Posttest 3 PBO - Sistem Pendataan Menu Restoran Sushi

## Deskripsi Singkat

Program ini adalah program sederhana untuk pendataan menu dan transaksi pada restoran sushi. Program dibuat menggunakan Python dan menerapkan beberapa konsep Pemrograman Berorientasi Objek (PBO).

Konsep yang digunakan dalam program ini disesuaikan dengan soal Posttest 3, yaitu **relasi antar class, abstraction, inheritance, polymorphism, duck typing, dan operator overloading**.

---


### Relasi yang digunakan

#### A. Association: `Pesanan` → `MenuSushi`

`Pesanan` berhubungan dengan `MenuSushi` karena setiap pesanan membutuhkan menu yang dipesan. Pada program, object `MenuSushi` dikirim ke `Pesanan` saat object pesanan dibuat.

Contohnya:

```python
pesanan1 = Pesanan("Andi", nigiri1, 2)
```

Jadi `Pesanan` menggunakan object menu, tetapi menu tersebut tetap bisa berdiri sendiri tanpa adanya `Pesanan`.

---

#### B. Aggregation: `DaftarMenu` → `MenuSushi`

`DaftarMenu` digunakan untuk menyimpan beberapa object `MenuSushi`.

Contohnya:

```python
daftar.tambah_menu(nigiri1)
daftar.tambah_menu(roll1)
```

Relasi ini termasuk **agregasi** karena menu dibuat di luar `DaftarMenu`, lalu dimasukkan ke dalam daftar. Jadi kalau `DaftarMenu` dihapus, object menu yang sebelumnya dibuat masih tetap ada.

Contohnya di program:

```python
daftar.hapus_menu("Edamame")
print(menu_umum.nama)
```

Menu `Edamame` masih bisa digunakan walaupun sudah dihapus dari `DaftarMenu`.

---

#### C. Composition: `KasirDenganRiwayat` → `RiwayatTransaksi`

`KasirDenganRiwayat` memiliki hubungan komposisi dengan `RiwayatTransaksi` karena object `RiwayatTransaksi` dibuat langsung dari dalam class `KasirDenganRiwayat`.

Bagian ini terdapat pada method:

```python
def _buat_riwayat(self, nama_pelanggan, total):
    ...
    trx = RiwayatTransaksi(id_trx, nama_pelanggan, total)
    self._riwayat.append(trx)
```

Jadi riwayat transaksi memang dibuat dan disimpan oleh `KasirDenganRiwayat`. Karena itu relasinya menggunakan **composition**, bukan aggregation.

---

# 2. Abstraksi

## Abstract Class

Pada program ini terdapat abstract class bernama `MenuSushi`.

Class tersebut menggunakan `ABC` dari module `abc`:

```python
from abc import ABC, abstractmethod

class MenuSushi(ABC):
```

Di dalam `MenuSushi` terdapat dua abstract method, yaitu:

```python
@abstractmethod
def tampilkan_info(self):
    pass

@abstractmethod
def cara_sajian(self):
    pass
```

Artinya, setiap subclass dari `MenuSushi` wajib membuat implementasi dari kedua method tersebut.

---

## Subclass

Beberapa subclass yang digunakan adalah:

- `SushiNigiri`
- `SushiRoll`
- `SideDish`

Ketiga class tersebut mewarisi `MenuSushi` dan mengimplementasikan abstract method yang ada.

Contohnya pada `SushiNigiri`:

```python
def tampilkan_info(self):
    ...

def cara_sajian(self):
    ...
```

Hal yang sama juga dilakukan oleh `SushiRoll` dan `SideDish`.

Selain itu, subclass tetap menggunakan:

```python
super().__init__(...)
```

untuk menjalankan constructor dari class induknya.

---

## Method Konkret

Walaupun `MenuSushi` merupakan abstract class, class ini juga mempunyai method biasa yang bisa digunakan oleh semua subclass.

Salah satunya adalah:

```python
def info_lengkap(self):
    self.tampilkan_info()
    print(f"Sajian : {self.cara_sajian()}")
```

Method `info_lengkap()` bisa dipanggil oleh object dari `SushiNigiri`, `SushiRoll`, maupun `SideDish`.

Jadi tidak semua method di abstract class harus berupa abstract method.

---

## Bukti Abstract Class Tidak Bisa Dibuat Langsung

Program juga mencoba membuat object langsung dari `MenuSushi`:

```python
try:
    menu_abstrak = MenuSushi(
        "Menu Abstrak", 10000, 5, "Umum"
    )
except TypeError as e:
    print(f"Error: {e}")
```

Hasilnya akan menghasilkan `TypeError` karena `MenuSushi` masih mempunyai abstract method yang belum diimplementasikan.

Selain itu, program juga membuat subclass yang hanya mengimplementasikan salah satu abstract method:

```python
class MenuTidakLengkap(MenuSushi):
    def tampilkan_info(self):
        print("info")
```

Karena `cara_sajian()` belum dibuat, object dari `MenuTidakLengkap` juga tidak bisa dibuat.

Hal ini menjadi bukti bahwa abstract method pada `MenuSushi` memang wajib diimplementasikan oleh subclass.

---

# 3. Polimorfisme

## A. Polimorfisme melalui Pewarisan

Polimorfisme digunakan pada method `tampilkan_info()`.

Method ini ada pada `MenuSushi`, kemudian di-override oleh subclass seperti:

- `SushiNigiri`
- `SushiRoll`
- `SideDish`

Setiap subclass mempunyai cara menampilkan informasi yang berbeda.

Kemudian semua object tersebut dimasukkan ke dalam satu list:

```python
semua_menu = [
    menu_umum,
    nigiri1,
    nigiri2,
    roll1,
    roll2
]
```

Lalu dipanggil menggunakan satu loop:

```python
for menu in semua_menu:
    menu.tampilkan_info()
```

Walaupun method yang dipanggil sama, hasilnya berbeda sesuai dengan object yang sedang digunakan.

Jadi tidak perlu membuat `if` atau `elif` untuk mengecek jenis object. Masing-masing class sudah menentukan perilakunya sendiri.

---

## B. Duck Typing

Duck typing digunakan pada method `cetak_ringkasan()`.

Beberapa class yang tidak memiliki hubungan inheritance langsung mempunyai method dengan nama yang sama, yaitu:

- `Pesanan`
- `DaftarMenu`
- `Kasir`

Ketiganya mempunyai:

```python
cetak_ringkasan()
```

Kemudian dibuat satu fungsi:

```python
def cetak_laporan(daftar_objek):
    for obj in daftar_objek:
        obj.cetak_ringkasan()
```

Fungsi tersebut dapat menerima object dari class yang berbeda selama object tersebut mempunyai method `cetak_ringkasan()`.

Contohnya:

```python
cetak_laporan([
    pesanan1,
    daftar,
    kasir
])
```

Jadi fungsi tersebut tidak perlu mengecek object tersebut berasal dari class apa.

---

## C. Operator Overloading

Program juga menggunakan operator overloading atau magic method.

Beberapa yang digunakan adalah:

### `__str__`

Digunakan supaya object menu bisa langsung ditampilkan dalam bentuk yang lebih mudah dibaca.

```python
def __str__(self):
    return f"{self.nama} (Rp{self.harga:,})"
```

Contohnya:

```python
print(nigiri1)
```

---

### `__lt__`

Digunakan untuk membandingkan harga antar menu.

```python
def __lt__(self, other):
    return self.harga < other.harga
```

Contohnya:

```python
nigiri2 < nigiri1
```

Operator ini juga membuat object menu bisa digunakan pada:

```python
sorted(semua_menu)
```

sehingga menu dapat diurutkan berdasarkan harga.

---

### `__len__`

Operator ini digunakan pada class `DaftarMenu`.

```python
def __len__(self):
    return len(self._koleksi_menu)
```

Dengan begitu jumlah menu dapat diketahui menggunakan:

```python
len(daftar)
```

---

# 4. Kesimpulan

Dari program ini, konsep PBO yang diminta pada soal sudah diterapkan dalam bentuk program yang saling berhubungan.

Relasi antar class yang digunakan adalah:

| Relasi | Class yang Berhubungan |
|---|---|
| Association | `Pesanan` → `MenuSushi` |
| Aggregation | `DaftarMenu` → `MenuSushi` |
| Composition | `KasirDenganRiwayat` → `RiwayatTransaksi` |

Selain itu, program juga menggunakan **abstract class `MenuSushi`**, inheritance pada beberapa subclass, polymorphism melalui overriding method, duck typing melalui `cetak_ringkasan()`, serta operator overloading menggunakan `__str__`, `__lt__`, dan `__len__`.

Dengan begitu, konsep yang diminta pada Posttest 3 tidak hanya dibuat di diagram, tetapi juga benar-benar diterapkan di dalam kode program.