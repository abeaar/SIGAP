import React from "react";
import BeritaCard from "../components/BeritaCard";
import BeritaTrendingDummy from "../data/BeritaTrendingDummy.json";

function BeritaTrending() {
  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Semua Berita Trending</h1>
      <div className="d-flex flex-column">
        {BeritaTrendingDummy.map((item, index) => (
          <BeritaCard key={index} {...item} layout="vertical" />
        ))}
      </div>
    </div>
  );
}

export default BeritaTrending;
