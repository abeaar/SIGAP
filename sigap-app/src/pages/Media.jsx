import React, { useEffect, useState } from "react";
import { fetchPortal } from "../config/api";
import BeritaCard from "../components/BeritaCard";
import { useParams } from "react-router-dom";

// Mapping label media untuk tampilan judul
const mediaLabelMap = {
  kedaulatanrakyat: "KRJogja",
  detik: "detikJogja",
  idntimes: "IDNTimesJogja",
  times: "TIMESJogja",
  // tambahkan jika ada media lain
};

const Media = () => {
  const { portal } = useParams(); // portal: 'krjogja', 'detikjogja', dst
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!portal) return;
    fetchPortal(portal)
      .then((res) => {
        // Tambahkan portal jika belum ada di setiap item
        const withPortal = (res.data || []).map(item => ({
          ...item,
          portal: item.portal || portal, // fallback ke param portal dari URL
        }));
        // Filter duplikat
        const unik = Array.from(
          new Map(withPortal.map((item) => [`${item.portal}-${item.id}`, item])).values()
        );
        setData(unik);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [portal]);

  const displayName = mediaLabelMap[portal?.toLowerCase()] || portal;

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Berita dari {displayName}</h1>
      {data.length > 0 ? (
        <div className="d-flex flex-column gap-3">
          {data.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`}
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