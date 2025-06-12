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
    <div className="d-flex overflow-auto gap-3 px-1 pb-2">
      {data.map((item) => (
        <div style={{ minWidth: 270, flex: "0 0 auto" }} key={`${item.portal}-${item.id}`}>
          <BeritaCard {...item} />
        </div>
      ))}
    </div>
  );
};

export default BeritaTrendingList;