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
    <div className="d-flex overflow-auto gap-3 px-1 pb-2">
      {data.map((item) => (
        <div style={{ minWidth: 270, flex: "0 0 auto" }} key={`${item.portal}-${item.id}`}>
          <BeritaCard {...item} />
        </div>
      ))}
    </div>
  );
};

export default BeritaTerkiniList;