import React, { useEffect, useState } from "react";
import { fetchPortal } from "../config/api";
import BeritaCard from "../components/BeritaCard";
import { useParams } from "react-router-dom";
const Media = () => {
  const { portal } = useParams(); // portal: 'krjogja', 'detikjogja', dst
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

useEffect(() => {
    if (!portal) return;
    fetchPortal(portal)
      .then((res) => {
        setData(res.data); // res.data dari API backend
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [portal]);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Berita dari {portal}</h1>
      {data.length > 0 ? (
        <div className="d-flex flex-column gap-3">
          {data.map((item) => (
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
        <p className="text-muted">Tidak ada berita dari media ini.</p>
      )}
    </div>
  );
};

export default Media;