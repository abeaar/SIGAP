import React from "react";
import { useNavigate } from "react-router-dom";

const BeritaCard = ({
  id,
  portal,
  layout = "horizontal",
  pageType = "home", // 'home' (default) or 'page'
  category,
  time_published,
  title,
  description,
  image,
  image_url,
  source,
}) => {
  const navigate = useNavigate();
  const isHorizontal = layout === "horizontal";
  const isFullPage = pageType === "page";
  const gambar = image || image_url;

  const handleClick = () => {
    if (id && portal) {
      navigate(`/berita/${portal}-${id}`);
    } else {
      console.warn("ID atau portal tidak tersedia:", { id, portal });
    }
  };

  // Layout untuk halaman penuh
  if (isHorizontal && isFullPage) {
    return (
      <div
        className="card overflow-hidden mb-4 border-0 shadow-sm"
        style={{ width: "100%", cursor: "pointer" }}
        onClick={handleClick}
      >
        <div className="row g-0">
          <div className="col-md-4">
            <img
              src={gambar}
              alt={title}
              className="img-fluid h-100"
              style={{
                objectFit: "cover",
                borderTopLeftRadius: "0.5rem",
                borderBottomLeftRadius: "0.5rem",
                maxHeight: "220px",
              }}
            />
          </div>
          <div className="col-md-8">
            <div className="card-body">
              {category && <span className="badge bg-danger mb-2">{category}</span>}
              <div className="text-muted mb-1" style={{ fontSize: "0.85rem" }}>
                {source ? `${source} • ` : ""}{time_published}
              </div>
              <h5 className="card-title fw-bold">{title}</h5>
              <p className="card-text" style={{ fontSize: "0.9rem" }}>{description}</p>
              <div className="d-flex gap-3 text-secondary mt-2">
                <i className="bi bi-heart"></i>
                <i className="bi bi-chat"></i>
                <i className="bi bi-share"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Card versi default (beranda)
  return (
    <div
      className={`card shadow-sm border-0 ${isHorizontal ? "me-3" : "mb-3"}`}
      style={{
        minWidth: isHorizontal ? "250px" : "100%",
        maxWidth: isHorizontal ? "250px" : "100%",
        cursor: "pointer",
      }}
      onClick={handleClick}
    >
      <div className={`d-flex ${isHorizontal ? "flex-column" : "flex-row"}`}>
        <img
          src={gambar}
          alt={title}
          className="img-fluid rounded-top"
          style={{ width: "100%", height: "150px", objectFit: "cover" }}
        />
        <div className="card-body d-flex flex-column justify-content-between">
          <div>
            {category && <span className="badge bg-danger mb-2">{category}</span>}
            <h6 className="card-title fw-bold">{title}</h6>
            <small className="text-muted">{source ? `${source} • ` : ""}{time_published}</small>
            <p className="card-text mt-2" style={{ fontSize: "0.85rem" }}>{description}</p>
          </div>
          <div className="d-flex gap-2 mt-2">
            <i className="bi bi-heart"></i>
            <i className="bi bi-chat"></i>
            <i className="bi bi-share"></i>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BeritaCard;
