import React, { useEffect, useState } from "react";
import { fetchTerkini } from "../config/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

// Fungsi untuk menampilkan label dengan huruf depan kapital
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Fungsi normalisasi kategori: lowercase, hapus simbol, trim spasi
function normalizeKategori(str) {
  if (!str) return "unknown";
  let lower = str.toLowerCase().trim();
  if (lower.startsWith("tidak")) return "unknown";
  // Jika ada spasi, underscore, atau dash, masukkan ke unknown
  if (/[ _-]/.test(lower)) return "unknown";
  // Hapus simbol selain huruf dan angka
  const norm = lower.replace(/[^a-z0-9]/gi, "");
  return norm || "unknown";
}

const Grafik = () => {
  const [kategoriData, setKategoriData] = useState([]);

  useEffect(() => {
    fetchTerkini().then((res) => {
      const berita = Array.isArray(res.terkini) ? res.terkini : [];
      const count = {};
      berita.forEach((item) => {
        let kategoriNorm = normalizeKategori(item.category);
        if (!kategoriNorm) {
          kategoriNorm = "unknown";
        }
        count[kategoriNorm] = (count[kategoriNorm] || 0) + 1;
      });
      // Ubah ke array untuk recharts, label capitalize (Unknown tetap kapital)
      const dataArr = Object.entries(count).map(([kategori, jumlah]) => ({
        kategori: kategori === "unknown" ? "Unknown" : capitalize(kategori),
        jumlah,
      }));
      setKategoriData(dataArr);
    });
  }, []);

  return (
    <div>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={kategoriData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="kategori" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="jumlah" fill="#b91c1c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Grafik;