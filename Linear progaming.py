import streamlit as st                    # Streamlit untuk UI
import numpy as np                       # Numpy buat matematika
from scipy.optimize import linprog       # linprog buat optimasi LP
import matplotlib.pyplot as plt          # Matplotlib buat grafik

def run_linear_programming():
    st.title("Optimasi Produksi (Linear Programming)")

    # Input fungsi objektif
    st.markdown("### Masukkan Fungsi Objektif (Maksimalkan Z = c1*x + c2*y)")
    c1 = st.number_input("Koefisien x", value=60.0)
    c2 = st.number_input("Koefisien y", value=40.0)

    # Input kendala utama saja (misal: waktu mesin)
    st.markdown("### Masukkan Kendala Utama (misal: 3x + 2y ≤ 210)")
    a1 = st.number_input("Koefisien x (kendala 1)", value=3.0)
    a2 = st.number_input("Koefisien y (kendala 1)", value=2.0)
    b = st.number_input("Nilai batas kanan kendala", value=210.0)

    # Setup model LP
    c = [-c1, -c2]                   # Fungsi objektif (pakai negatif untuk maksimisasi)
    A = [[a1, a2]]                   # Hanya 1 kendala
    B = [b]
    bounds = [(0, None), (0, None)] # x ≥ 0, y ≥ 0

    # Jalankan optimasi
    res = linprog(c, A_ub=A, b_ub=B, bounds=bounds, method='highs')

    if res.success:
        st.success(f"Solusi optimal: x = {res.x[0]:.2f}, y = {res.x[1]:.2f}")
        st.info(f"Nilai maksimum Z = {-res.fun:.2f}")

        # Visualisasi grafik (dengan 1 kendala)
        x_vals = np.linspace(0, b / max(a1, 0.1), 200)        # Range x untuk grafik
        y = (b - a1 * x_vals) / a2                            # Hitung y dari persamaan kendala

        y = np.maximum(0, y)  # Pastikan y tidak negatif
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y, label=f"{a1}x + {a2}y ≤ {b}")     # Plot garis kendala
        plt.fill_between(x_vals, 0, y, color='skyblue', alpha=0.3, label='Wilayah Feasible')
        plt.plot(res.x[0], res.x[1], 'ro', label='Solusi Optimal')  # Titik optimal
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Visualisasi Optimasi Produksi (1 Kendala)')
        plt.legend()
        st.pyplot(plt)
    else:
        st.error("Tidak ditemukan solusi optimal.")
