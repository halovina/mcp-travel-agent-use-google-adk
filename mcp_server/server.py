import sqlite3
import os
from fastmcp import FastMCP

# ==========================================
# 1. SETUP DATABASE
# ==========================================
DB_NAME = "travel.db"

def init_db():
    """Inisialisasi database SQLite dan populate data awal jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Cek apakah tabel hotels sudah ada
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hotels'")
    if cursor.fetchone() is None:
        print("[System] Menginisialisasi tabel database...")
        cursor.execute("""
            CREATE TABLE hotels(
                id            INTEGER NOT NULL PRIMARY KEY,
                name          VARCHAR NOT NULL,
                location      VARCHAR NOT NULL,
                price_tier    VARCHAR NOT NULL,
                checkin_date  DATE    NOT NULL,
                checkout_date DATE    NOT NULL,
                booked        INTEGER NOT NULL
            )
        """)
        
        # Menggunakan integer 0 untuk representasi bit/boolean di SQLite
        initial_data = [
            (1, 'Hilton Basel', 'Basel', 'Luxury', '2024-04-20', '2024-04-22', 0),
            (2, 'Marriott Zurich', 'Zurich', 'Upscale', '2024-04-14', '2024-04-21', 0),
            (3, 'Hyatt Regency Basel', 'Basel', 'Upper Upscale', '2024-04-02', '2024-04-20', 0),
            (4, 'Radisson Blu Lucerne', 'Lucerne', 'Midscale', '2024-04-05', '2024-04-24', 0),
            (5, 'Best Western Bern', 'Bern', 'Upper Midscale', '2024-04-01', '2024-04-23', 0),
            (6, 'InterContinental Geneva', 'Geneva', 'Luxury', '2024-04-23', '2024-04-28', 0),
            (7, 'Sheraton Zurich', 'Zurich', 'Upper Upscale', '2024-04-02', '2024-04-27', 0),
            (8, 'Holiday Inn Basel', 'Basel', 'Upper Midscale', '2024-04-09', '2024-04-24', 0),
            (9, 'Courtyard Zurich', 'Zurich', 'Upscale', '2024-04-03', '2024-04-13', 0),
            (10, 'Comfort Inn Bern', 'Bern', 'Midscale', '2024-04-04', '2024-04-16', 0)
        ]
        
        cursor.executemany("""
            INSERT INTO hotels(id, name, location, price_tier, checkin_date, checkout_date, booked)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, initial_data)
        conn.commit()
        print("[System] Database berhasil diinisialisasi.")
    
    conn.close()

# ==========================================
# 2. DEFINISI FASTMCP TOOLS
# ==========================================
# Membuat instance FastMCP. File ini dapat juga di-serve ke MCP Client lain jika diperlukan.
mcp = FastMCP("TravelAgent")

@mcp.tool()
def search_hotels(location: str) -> dict:
    print("masuk search_hotels")
    """
    Mengembalikan daftar hotel di lokasi tertentu yang status booked-nya adalah 0.
    
    Args:
        location: Nama kota (misalnya: 'Basel', 'Zurich').
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Pencarian case-insensitive (huruf besar/kecil tidak masalah)
    cursor.execute("""
        SELECT id, name, price_tier, checkin_date, checkout_date 
        FROM hotels 
        WHERE LOWER(location) = LOWER(?) AND booked = 0
    """, (location,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"Tidak ditemukan hotel yang tersedia di {location}."
    
    result = f"Hotel tersedia di {location}:\n"
    for r in rows:
        result += f"- ID: {r[0]} | Nama: {r[1]} | Kelas: {r[2]} | Tersedia: {r[3]} s/d {r[4]}\n"
    return {
        "result": result
    }

@mcp.tool()
def book_hotel(hotel_id: int) -> dict:
    print("masuk book_hotel")
    """
    Mengubah status pemesanan hotel menjadi 1 (booked) untuk hotel_id tersebut.
    
    Args:
        hotel_id: ID dari hotel yang ingin dipesan.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT booked, name FROM hotels WHERE id = ?", (hotel_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return f"Gagal: Hotel dengan ID {hotel_id} tidak ditemukan di sistem."
    
    is_booked, hotel_name = row
    if is_booked == 1:
        conn.close()
        return f"Gagal: Hotel '{hotel_name}' (ID: {hotel_id}) sudah dipesan."
    
    cursor.execute("UPDATE hotels SET booked = 1 WHERE id = ?", (hotel_id,))
    conn.commit()
    conn.close()
    
    return {
        "result": f"Berhasil: Hotel '{hotel_name}' (ID: {hotel_id}) telah sukses dipesan."
    }




if __name__ == "__main__":
    init_db()
    # Menjalankan server MCP
    mcp.run(transport="http", host="127.0.0.1", port=9000)