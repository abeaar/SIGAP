import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import BeritaCard from "../components/BeritaCard";
import { fetchAllBerita } from "../config/api";

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
      return date.toISOString().split("T")[0];
    }
  }

  const date = new Date(dateStr);
  if (!isNaN(date.getTime())) {
    return date.toISOString().split("T")[0];
  }

  return "";
};

const FilterTrending = () => {
  const [searchParams] = useSearchParams();
  const selectedDate = searchParams.get("date");
  const [berita, setBerita] = useState([]);

  useEffect(() => {
    if (!selectedDate) return;

    fetchAllBerita().then((all) => {
      const hasil = all.filter(item => {
        const tanggal = formatDate(item.scrape_time);
        return tanggal === selectedDate;
      });
      setBerita(hasil);
    });
  }, [selectedDate]);

  return (
    <div className="container filter-wrapper my-5">
      <h2 className="filter-heading mb-4">
        Trending & Terkini Tanggal: <span className="text-danger">{selectedDate}</span>
      </h2>
      {berita.length > 0 ? (
        <div className="filter-berita d-flex flex-column gap-3">
          {berita.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`}
              id={`${item.portal}-${item.id}`}
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
 