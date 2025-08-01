import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import BeritaCard from "../components/BeritaCard";
import { fetchTerkini, fetchTerpopuler } from "../config/api";

// Fungsi bantu untuk menyamakan format tanggal ke "YYYY-MM-DD"
const formatDate = (dateStr) => {
  if (!dateStr) return "";
  if (/^\d{4}-\d{2}-\d{2}/.test(dateStr)) return dateStr.slice(0, 10);
  if (/^\d{4}-\d{2}-\d{2}T/.test(dateStr)) return dateStr.slice(0, 10);
  const parts = dateStr.split(" ");
  if (parts.length === 3) {
    const day = parseInt(parts[0], 10);
    const year = parseInt(parts[2], 10);
    const monthNames = {
      januari: 0, februari: 1, maret: 2, april: 3, mei: 4, juni: 5,
      juli: 6, agustus: 7, september: 8, oktober: 9, november: 10, desember: 11
    };
    const month = monthNames[parts[1].toLowerCase()];
    if (!isNaN(day) && month !== undefined && !isNaN(year)) {
      const date = new Date(year, month, day);
      const yyyy = date.getFullYear();
      const mm = String(date.getMonth() + 1).padStart(2, "0");
      const dd = String(date.getDate()).padStart(2, "0");
      return `${yyyy}-${mm}-${dd}`;
    }
  }
  const date = new Date(dateStr);
  if (!isNaN(date.getTime())) {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, "0");
    const dd = String(date.getDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  }
  return "";
};

const FilterTrending = () => {
  const [searchParams] = useSearchParams();
  const selectedDate = searchParams.get("date");
  const [berita, setBerita] = useState([]);

  useEffect(() => {
    Promise.all([fetchTerkini(), fetchTerpopuler()]).then(([terkiniRes, trendingRes]) => {
      const terkini = Array.isArray(terkiniRes.terkini) ? terkiniRes.terkini : [];
      const trending = Array.isArray(trendingRes.terpopuler) ? trendingRes.terpopuler : [];
      // Gabungkan semua berita
      const all = [...terkini, ...trending];
      // Hilangkan duplikat berdasarkan portal-id
      const unik = Array.from(
        new Map(all.map(item => [`${item.portal}-${item.id}`, item])).values()
      );
      // Filter berdasarkan tanggal yang dipilih
      const filtered = unik.filter(
        (item) => formatDate(item.time_published) === selectedDate
      );
      setBerita(filtered);
    });
  }, [selectedDate]);

  return (
    <div className="container filter-wrapper">
      <h2 className="filter-heading">Trending & Terkini Tanggal: {selectedDate}</h2>
      {berita.length > 0 ? (
        <div className="filter-berita">
          {berita.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`}
              {...item}
              layout="horizontal"
              pageType="page"
            />
          ))}
        </div>
      ) : (
        <p className="text-muted">Tidak ada berita trending/terkini untuk tanggal ini.</p>
      )}
    </div>
  );
};

export default FilterTrending;