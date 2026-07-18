import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchAllBerita } from "../config/api";

const DetailBerita = () => {
  const { slug } = useParams();
  const [berita, setBerita] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    const lastDash = slug.lastIndexOf("-");
    const portal = slug.substring(0, lastDash);
    const id = slug.substring(lastDash + 1);
    fetchAllBerita().then((all) => {
      const found = all.find(
        (item) => item.portal === portal && String(item.id) === id
      );
      setBerita(found);
      setLoading(false);
    });
  }, [slug]);

  if (loading) return <div className="container my-5">Loading...</div>;
  if (!berita) return <div className="container my-5">Berita tidak ditemukan.</div>;

  return (
    <div className="detail-page-wrapper py-5">
      <div className="container">
        <div className="card shadow-sm p-4 rounded-4 bg-white">
          {/* Tombol kembali */}
          <div className="mb-4">
            <button
              onClick={() => window.history.back()}
              className="btn btn-outline-danger d-inline-flex align-items-center gap-2 px-3 py-2 rounded-pill shadow-sm"
              style={{ fontWeight: 600, fontSize: "1rem" }}
            >
              <i className="bi bi-arrow-left"></i>
              Kembali
            </button>
          </div>

          {/* Gambar utama */}
          <div className="mb-4">
            <img
              src={
                !berita.image && !berita.image_url
                  ? "/sigap-news.png"
                  : (berita.image_url || berita.image).includes("blank.png")
                  ? "/sigap-news.png"
                  : berita.image_url || berita.image
              }
              alt={berita.title}
              className="img-fluid rounded-3 w-100"
              style={{ maxHeight: "400px", objectFit: "cover" }}
            />
          </div>

          {/* Judul dan sumber */}
          <h2 className="fw-bold mb-2">{berita.title}</h2>
          <p className="text-muted mb-4">
            {berita.portal} • {berita.time_published}
          </p>

          {/* Isi berita */}
          <p className="fs-5" style={{ lineHeight: 1.7 }}>
            {berita.content || berita.description}
          </p>

          {/* Box Solusi */}
          {berita.solution && (
            <div className="solution-box mt-5 p-4 rounded-4">
              <div className="d-flex align-items-center mb-3">
                <img
                  src="/logo-sigap.png"
                  alt="Logo Bid TIK"
                  style={{ height: "30px" }}
                  className="me-2"
                />
                <img
                  src="/name-sigap.png"
                  alt="SIGAP Text"
                  style={{ height: "22px" }}
                />
              </div>
              <h5 className="fw-bold mb-3">SIGAP AI</h5>
              <p className="mb-0">{berita.solution}</p>
            </div>
          )}

          {/* Link ke berita asli */}
          {berita.url && (
            <div className="mt-4 text-center">
              <a
                href={berita.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-danger btn-lg px-5 d-inline-flex align-items-center gap-2 rounded-pill shadow"
                style={{ fontWeight: 600, fontSize: "1.1rem", letterSpacing: "0.5px" }}
              >
                <i className="bi bi-box-arrow-up-right"></i>
                Lihat Berita Asli
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DetailBerita;