
    print("\n--- 5. Method Unik Subclass ---")
    nigiri1.cek_kualitas()
    nigiri2.cek_kualitas()
    roll1.bagi_potongan(4)
    roll2.bagi_potongan(3)

    print("\n--- 6. Class Method & Static Method ---")
    print(f"Total menu terdaftar: {MenuSushi.total_menu_terdaftar}")
    print(f"Pajak awal: {MenuSushi.pajak_persen}%")
    MenuSushi.ubah_pajak(15)