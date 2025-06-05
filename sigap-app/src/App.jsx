import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from './pages/Home';
import BeritaTrending from './pages/BeritaTrending';
import BeritaTerkini from './pages/BeritaTerkini';
import Media from './pages/Media';
import Kategori from './pages/Kategori';
import Search from "./pages/Search";
import FilterTrending from './pages/FilterTrending';
import DetailBerita from './pages/DetailBerita';   

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/berita-trending" element={<BeritaTrending />} />
        <Route path="/berita-terkini" element={<BeritaTerkini />} />
        <Route path="/media/:id" element={<Media />} />
        <Route path="/kategori/:kategoriId" element={<Kategori />} />
        <Route path="/search" element={<Search />} />
        <Route path="/filter-trending" element={<FilterTrending />} />
        <Route path="/berita/:slug" element={<DetailBerita />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;

