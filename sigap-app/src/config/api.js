const BASE_API_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchTerkini = async () => {
  const res = await fetch(`${BASE_API_URL}/terkini?`);
  return res.json();
};

export const fetchTerpopuler = async () => {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/terpopuler`);
  return res.json();
};


export async function fetchPortal(portal) {
  const res = await fetch(`${BASE_API_URL}/news/${portal}`);
  return res.json();
};

export async function fetchCategory(category) {
  const res = await fetch(`${BASE_API_URL}/category/${category}`);
  if (!res.ok) throw new Error("Kategori tidak ditemukan");
  return await res.json();
}

export const fetchAllBerita = async () => {
  const resTerkini = await fetch(`${import.meta.env.VITE_API_BASE_URL}/terkini?include_all=true`);
  const resTerpopuler = await fetch(`${import.meta.env.VITE_API_BASE_URL}/terpopuler?include_all=true`);

  const terkini = await resTerkini.json();
  const terpopuler = await resTerpopuler.json();

  const arrTerkini = Array.isArray(terkini.terkini) ? terkini.terkini : [];
  const arrTerpopuler = Array.isArray(terpopuler.terpopuler) ? terpopuler.terpopuler : [];

  return [...arrTerkini, ...arrTerpopuler];
};
