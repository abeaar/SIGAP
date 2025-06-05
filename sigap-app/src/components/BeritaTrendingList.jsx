import React, { useEffect, useState } from "react";
import { fetchTerpopuler } from "../config/api";
import BeritaCard from "./BeritaCard";
//import BeritaTrendingDummy from "../data/BeritaTrendingDummy.json"; // Import data dummy
//import BASE_API_URL from "../config/api";

const BeritaTrendingList = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchTerpopuler().then((res) => {
      // Ambil array dari properti 'terpopuler', fallback ke [] jika tidak ada
      setData(Array.isArray(res.terpopuler) ? res.terpopuler : []);
    });
  }, []);

  return (
    <div className="d-flex overflow-auto px-3">
      {(data || []).map((item) => (
        <BeritaCard
          key={`${item.portal}-${item.id}`}
          id={`${item.portal}-${item.id}`}
          {...item}
        />
      ))}
    </div>
  );
};

export default BeritaTrendingList;