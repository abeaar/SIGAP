import React, { useEffect, useState } from "react";
import { fetchTerkini } from "../config/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

const Grafik = () => {
  const [kategoriData, setKategoriData] = useState([]);

  useEffect(() => {
    fetchTerkini().then((res) => {
      const berita = Array.isArray(res.terkini) ? res.terkini : [];
      const count = {};
      berita.forEach((item) => {
        if (item.category) {
          count[item.category] = (count[item.category] || 0) + 1;
        }
      });
      // Ubah ke array untuk recharts
      const dataArr = Object.entries(count).map(([kategori, jumlah]) => ({
        kategori,
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