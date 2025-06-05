const BASE_API_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchTerkini = async () => {
  const res = await fetch(`${BASE_API_URL}/terkini`);
  return res.json();
};

export const fetchTerpopuler = async () => {
  const res = await fetch(`${BASE_API_URL}/terpopuler`);
  return res.json();
};

export const fetchAllBerita = async () => {
  const [terkini, terpopuler] = await Promise.all([
    fetchTerkini(),
    fetchTerpopuler(),
  ]);
  // Ambil array dari objek jika perlu
  const arrTerkini = Array.isArray(terkini.terkini) ? terkini.terkini : [];
  const arrTerpopuler = Array.isArray(terpopuler.terpopuler) ? terpopuler.terpopuler : [];
  return [...arrTerkini, ...arrTerpopuler];
};