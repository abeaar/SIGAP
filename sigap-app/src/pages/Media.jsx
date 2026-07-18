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
  const [loading, setLoading] = useState(true); // Default loading true

  useEffect(() => {
    // Set loading ke true setiap kali portal berubah untuk menunjukkan bahwa data sedang diambil
    setLoading(true);
    if (!portal) {
      // Jika portal tidak ada (misalnya URL tidak valid), hentikan loading dan kosongkan data
      setData([]);
      setLoading(false);
      return;
    }

    fetchPortal(portal)
      .then((res) => {
        // Tambahkan portal jika belum ada di setiap item
        const withPortal = (res.data || []).map(item => ({
          ...item,
          // Gunakan item.portal jika ada, jika tidak gunakan portal dari URL param
          portal: item.portal || portal,
        }));
        // Filter duplikat
        const unik = Array.from(
          new Map(withPortal.map((item) => [`${item.portal}-${item.id}`, item])).values()
        );
        setData(unik);
        setLoading(false); // Set loading ke false setelah data berhasil diambil
      })
      .catch((error) => {
        console.error("Error fetching portal data:", error); // Log error untuk debugging
        setData([]); // Kosongkan data jika ada error
        setLoading(false); // Set loading ke false meskipun ada error
      });
  }, [portal]); // Dependensi: useEffect akan berjalan ulang jika nilai 'portal' berubah

  const displayName = mediaLabelMap[portal?.toLowerCase()] || portal;

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Berita dari {displayName}</h1>
      {loading ? (
        // Tampilkan loading di dalam return JSX
        <p>Loading...</p>
      ) : data.length > 0 ? (
        // Tampilkan data jika sudah tidak loading dan ada data
        <div className="d-flex flex-column gap-3">
          {data.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`} // Pastikan key unik
              {...item}
              layout="horizontal"
              pageType="page"
            />
          ))}
        </div>
      ) : (
        // Tampilkan pesan "tidak ada berita" jika tidak loading dan tidak ada data
        <p className="text-muted">Tidak ada berita dari media ini.</p>
      )}
    </div>
  );
};

export default Media;