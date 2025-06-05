import React, { useEffect, useState } from "react";
import BeritaCard from "../components/BeritaCard";
import { fetchTerkini } from "../config/api";

function BeritaTerkini() {
  const [berita, setBerita] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTerkini()
      .then((data) => {
        setBerita(Array.isArray(data.terkini) ? data.terkini : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Gagal mengambil data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Semua Berita Terkini</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="d-flex flex-column">
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
      )}
    </div>
  );
}

export default BeritaTerkini;