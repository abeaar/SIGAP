import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from './pages/Home';
import BeritaTrending from './pages/BeritaTrending';
import BeritaTerkini from './pages/BeritaTerkini';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/berita-trending" element={<BeritaTrending />} />
        <Route path="/berita-terkini" element={<BeritaTerkini />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;

