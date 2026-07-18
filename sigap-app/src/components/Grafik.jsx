import React, { useEffect, useState } from "react";
import { fetchTerkini } from "../config/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
//import { PieChart, Pie, Cell, Legend } from "recharts";

// Jika ingin menggunakan warna berbeda untuk setiap kategori, bisa uncomment bagian ini (PieChart)
//const COLORS = ["#b91c1c", "#f59e42", "#3b82f6", "#10b981", "#6366f1", "#f43f5e", "#fbbf24", "#22d3ee", "#a3e635", "#f472b6", "#64748b"];

// Daftar kategori valid sesuai dropdown (pakai lowercase)
const kategoriDropdown = [
  "hukum", "politik", "sosial", "ekonomi", "pendidikan",
  "teknologi", "kesehatan", "kriminal", "agama", "hiburan"
];

// Fungsi untuk menampilkan label dengan huruf depan kapital
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Fungsi normalisasi kategori: lowercase, hapus simbol, trim spasi
function normalizeKategori(str) {
  if (!str) return "lainnya";
  let lower = str.toLowerCase().trim();
  if (lower.startsWith("tidak")) return "lainnya";
  // Jika ada spasi, underscore, atau dash, masukkan ke lainnya
  if (/[ _-]/.test(lower)) return "lainnya";
  // Hapus simbol selain huruf dan angka
  const norm = lower.replace(/[^a-z0-9]/gi, "");
  return norm || "lainnya";
}

const Grafik = () => {
  const [kategoriData, setKategoriData] = useState([]);

  useEffect(() => {
    fetchTerkini().then((res) => {
      const berita = Array.isArray(res.terkini) ? res.terkini : [];
      const count = {};
      berita.forEach((item) => {
        let kategoriNorm = normalizeKategori(item.category);
        // Jika kategori tidak ada di dropdown, masukkan ke "lainnya"
        if (!kategoriDropdown.includes(kategoriNorm)) {
          kategoriNorm = "lainnya";
        }
        count[kategoriNorm] = (count[kategoriNorm] || 0) + 1;
      });
      // Ubah ke array untuk recharts, label capitalize (Lainnya tetap kapital)
      const dataArr = Object.entries(count).map(([kategori, jumlah]) => ({
        kategori: kategori === "lainnya" ? "Lainnya" : capitalize(kategori),
        jumlah,
      }));
      setKategoriData(dataArr);
    });
  }, []);

  // Jika ingin menggunakan BarChart dengan layout vertikal, bisa uncomment bagian ini
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

  // Grafik dengan layout horizontal
  // return (
  //   <div>
  //     <ResponsiveContainer width="100%" height={350}>
  //       <BarChart data={kategoriData} layout="vertical">
  //         <CartesianGrid strokeDasharray="3 3" />
  //         <XAxis type="number" allowDecimals={false} />
  //         <YAxis dataKey="kategori" type="category" />
  //         <Tooltip />
  //         <Bar dataKey="jumlah" fill="#b91c1c" />
  //       </BarChart>
  //     </ResponsiveContainer>
  //   </div>
  // );

  // Jika ingin menggunakan PieChart, bisa uncomment bagian ini
  //   return (
  //   <div>
  //     <ResponsiveContainer width="100%" height={350}>
  //       <PieChart>
  //         <Pie
  //           data={kategoriData}
  //           dataKey="jumlah"
  //           nameKey="kategori"
  //           cx="50%"
  //           cy="50%"
  //           outerRadius={120}
  //           fill="#b91c1c"
  //           label
  //         >
  //           {kategoriData.map((entry, index) => (
  //             <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
  //           ))}
  //         </Pie>
  //         <Legend />
  //       </PieChart>
  //     </ResponsiveContainer>
  //   </div>
  // );
};

export default Grafik;