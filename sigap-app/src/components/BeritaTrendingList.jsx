import React, { useEffect, useState } from "react";
import BeritaCard from "./BeritaCard";

const BeritaTrendingList = () => {
  const [berita, setBerita] = useState([]);

  useEffect(() => {
    import("../data/BeritaTrendingDummy.json")
      .then((module) => setBerita(module.default))
      .catch((error) =>
        console.error("Gagal mengambil data trending:", error)
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

export default BeritaTrendingList;
