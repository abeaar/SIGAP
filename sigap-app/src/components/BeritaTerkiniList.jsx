import React, { useEffect, useState } from "react";
import BeritaCard from "./BeritaCard";

const BeritaTerkiniList = () => {
  const [berita, setBerita] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/terkini")
      .then((response) => response.json())
      .then((data) => setBerita(data.terkini || []))
      .catch((error) =>
        console.error("Gagal mengambil data terkini:", error)
      );
  }, []);

  return (
    <div className="d-flex overflow-auto px-3">
      {berita.map((item, index) => (
        <BeritaCard key={index} {...item} />
      ))}
    </div>
  );
};

export default BeritaTerkiniList;