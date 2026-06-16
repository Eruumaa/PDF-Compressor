import os
try:
    import fitz  # PyMuPDF
except ImportError:
    print("[ERROR] Modul PyMuPDF belum terinstall!")
    print("Ketik di terminal: pip install PyMuPDF")
    exit()

def compress_pas_1mb():
    # 1. Sesuaikan nama file kamu
    file_input = 'Sertifikat Peserta Seminar Google.pdf' 
    file_output = 'Sertifikat_PAS_1MB.pdf'
    
    # Target TEPAT 1 MB (1.048.576 Bytes di Windows)
    target_bytes = 1048576 

    if not os.path.exists(file_input):
        print(f"[ERROR] File '{file_input}' tidak ditemukan.")
        return

    print(f"[*] Membaca file: {file_input}")
    print("[*] Sedang mencari tingkat kompresi terbaik (Binary Search), mohon tunggu...")
    
    doc_lama = fitz.open(file_input)
    mat = fitz.Matrix(0.8, 0.8) # Resolusi dasar diturunkan sedikit agar aman
    
    # --- PROSES 1: MENCARI KUALITAS TERBAIK ---
    low_q, high_q = 5, 95
    best_q = 5
    
    # Mencari nilai JPEG quality yang menghasilkan ukuran terdekat di bawah 1MB
    while low_q <= high_q:
        mid_q = (low_q + high_q) // 2
        
        doc_baru = fitz.open()
        for page in doc_lama:
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_bytes = pix.tobytes("jpeg", mid_q)
            page_baru = doc_baru.new_page(width=page.rect.width, height=page.rect.height)
            page_baru.insert_image(page.rect, stream=img_bytes)
            
        doc_baru.save(file_output, garbage=4, deflate=True)
        doc_baru.close()
        
        ukuran_temp = os.path.getsize(file_output)
        
        if ukuran_temp == target_bytes:
            best_q = mid_q
            break # Kebetulan sangat beruntung, langsung pas
        elif ukuran_temp < target_bytes:
            best_q = mid_q   # Simpan sebagai yang terbaik sementara
            low_q = mid_q + 1 # Coba naikkan kualitas
        else:
            high_q = mid_q - 1 # Ukuran lebih dari 1MB, turunkan kualitas
            
    # --- PROSES 2: GENERATE FILE DENGAN KUALITAS TERBAIK ---
    doc_baru = fitz.open()
    for page in doc_lama:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes("jpeg", best_q)
        page_baru = doc_baru.new_page(width=page.rect.width, height=page.rect.height)
        page_baru.insert_image(page.rect, stream=img_bytes)
        
    doc_baru.save(file_output, garbage=4, deflate=True)
    doc_baru.close()
    doc_lama.close()
    
    # --- PROSES 3: PENYUNTIKAN DUMMY BYTES (PADDING) ---
    ukuran_sekarang = os.path.getsize(file_output)
    kekurangan_byte = target_bytes - ukuran_sekarang
    
    if kekurangan_byte > 0:
        print(f"[*] Ukuran sementara: {ukuran_sekarang} Bytes.")
        print(f"[*] Menyuntikkan {kekurangan_byte} Bytes dummy data agar pas 1 MB...")
        
        # Membuka file dalam mode 'ab' (Append Binary) untuk menambah data di akhir
        with open(file_output, "ab") as f:
            f.write(b'\0' * kekurangan_byte)
    elif kekurangan_byte < 0:
        print("[WARNING] Resolusi dokumen terlalu besar. Turunkan nilai 'fitz.Matrix(0.8, 0.8)' menjadi (0.6, 0.6)")

    # Pengecekan Akhir
    ukuran_akhir = os.path.getsize(file_output)
    
    print("\n[SUCCESS] File Selesai Diproses!")
    print(f"📄 Target   : 1048576 Bytes")
    print(f"📄 Hasil    : {ukuran_akhir} Bytes")
    
    if ukuran_akhir == target_bytes:
        print("🎯 BINGO! Ukuran file sekarang pas tidak kurang dan tidak lebih!")

if __name__ == '__main__':
    compress_pas_1mb()