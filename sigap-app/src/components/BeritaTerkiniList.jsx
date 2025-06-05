import React, { useEffect, useState } from "react";
import { fetchTerkini } from "../config/api";
import BeritaCard from "./BeritaCard";
//import BeritaTerkiniDummy from "../data/BeritaTerkiniDummy.json";

const BeritaTerkiniList = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchTerkini().then((res) => {
      setData(Array.isArray(res.terkini) ? res.terkini : []);
    });
  }, []);

  return (
    <div className="d-flex overflow-auto px-3">
      {data.map((item) => (
        <BeritaCard
          key={`${item.portal}-${item.id}`}
          id={`${item.portal}-${item.id}`}
          {...item}
        />
      ))}
    </div>
  );
};

export default BeritaTerkiniList;