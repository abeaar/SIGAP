import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchCategory } from "../config/api";
import BeritaCard from "../components/BeritaCard";

const kategoriLabelMap = {
  hukum: "Hukum",
  politik: "Politik",
  sosial: "Sosial",
  ekonomi: "Ekonomi",
  pendidikan: "Pendidikan",
  teknologi: "Teknologi",
  kesehatan:"Kesehatan",
  agama: "Agama",
  hiburan: "Hiburan",
  kriminal: "Kriminal",
  // tambahkan jika ada kategori lain di dropdown
};

const Kategori = () => {
  const { kategoriId } = useParams();
  const [berita, setBerita] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchCategory(kategoriId)
      .then((res) => {
        // Pastikan setiap item punya portal dan id
        const unik = Array.from(
          new Map((res.data || []).map(item => [`${item.portal}-${item.id}`, item])).values()
        );
        setBerita(unik);
        setLoading(false);
      })
      .catch(() => {
        setBerita([]);
        setLoading(false);
      });
  }, [kategoriId]);

  const displayKategori = kategoriLabelMap[kategoriId?.toLowerCase()] || kategoriId;

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Berita Kategori: {displayKategori}</h1>
      {loading ? (
        <p>Loading...</p>
      ) : berita.length > 0 ? (
        <div className="d-flex flex-column gap-3">
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
        <p>Belum ada berita untuk kategori ini.</p>
      )}
    </div>
  );
};

export default Kategori;