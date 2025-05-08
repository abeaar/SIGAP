import React from "react";
import BeritaCard from "../components/BeritaCard";
import BeritaTerkiniDummy from "../data/BeritaTerkiniDummy.json";

function BeritaTerkini() {
  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Semua Berita Terkini</h1>
      <div className="d-flex flex-column">
        {BeritaTerkiniDummy.map((item, index) => (
          <BeritaCard key={index} {...item} layout="vertical" />
        ))}
      </div>
    </div>
  );
}

export default BeritaTerkini;
