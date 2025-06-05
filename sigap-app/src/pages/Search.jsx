import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { fetchAllBerita } from "../config/api";
import BeritaCard from "../components/BeritaCard";

const Search = () => {
  const [searchParams] = useSearchParams();
  const [hasil, setHasil] = useState([]);
  const keyword = searchParams.get("keyword")?.toLowerCase() || "";

  useEffect(() => {
    fetchAllBerita().then((all) => {
      const hasilPencarian = all.filter(
        (item) =>
          item.title?.toLowerCase().includes(keyword) ||
          item.content?.toLowerCase().includes(keyword) ||
          item.description?.toLowerCase().includes(keyword)
      );
      setHasil(hasilPencarian);
    });
  }, [keyword]);

  return (
    <div className="container my-5">
      <h1 className="fw-bold mb-4">Hasil Pencarian: "{keyword}"</h1>
      {hasil.length > 0 ? (
        <div className="d-flex flex-column gap-3">
          {hasil.map((item) => (
            <BeritaCard
              key={`${item.portal}-${item.id}`}
              id={`${item.portal}-${item.id}`}
              {...item}
              layout="horizontal"
              pageType="page"
            />
          ))}
        </div>
      ) : (
        <p className="text-muted">Tidak ditemukan hasil untuk kata kunci tersebut.</p>
      )}
    </div>
  );
};

export default Search;