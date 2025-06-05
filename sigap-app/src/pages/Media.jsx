import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchAllBerita } from "../config/api";
import BeritaCard from "../components/BeritaCard";

// Mapping nama media pada URL menjadi nilai 'portal' di API
const portalMap = {
  detikjogja: ["detik", "detik_popular"],
  krjogja: ["kedaulatanrakyat", "kedaulatanrakyat_popular"],
  idntimes: ["idntimes", "idntimes_popular"],
  times: ["times", "times_popular"],

  // Tambahkan sesuai media yang tersedia
};
const mediaLabelMap = {
  krjogja: "KRJogja",
  detikjogja: "detikJogja",
  idntimes: "IDNTimesJogja",
  times: "TIMESJogja",
  // tambahkan jika ada media lain
};

const Media = () => {
  const { id } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchAllBerita().then((all) => {
      const mediaParam = id.replace(/-/g, "").toLowerCase(); // normalize
      const portalKeys = portalMap[mediaParam] || [mediaParam];
      const filtered = all.filter(
        (item) => portalKeys.includes(item.portal)
      );
      // filter duplikat berdasarkan ID
      const unik = Array.from(new Map(filtered.map((item) => [item.id, item])).values());
      setData(unik);
    });
  }, [id]);

  const mediaParam = id.replace(/-/g, "").toLowerCase(); // normalize
  const displayName = mediaLabelMap[mediaParam] || "Media";

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Berita dari {displayName}</h1>
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