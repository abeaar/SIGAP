//import BeritaTrendingDummy from "../data/BeritaTrendingDummy.json";
import React, { useEffect, useState } from "react";
import BeritaCard from "../components/BeritaCard";
import { fetchTerpopuler } from "../config/api";

function BeritaTrending() {
  const [berita, setBerita] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTerpopuler()
      .then((data) => {
        setBerita(Array.isArray(data.terpopuler) ? data.terpopuler : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Gagal mengambil data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="overflow-hidden container my-5">
      <h1 className="fw-bold mb-4">Semua Berita Trending</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="d-flex flex-column">
          {berita.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`}
              id={`${item.portal}-${item.id}`}
              {...item}
              layout="vertical"
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default BeritaTrending;