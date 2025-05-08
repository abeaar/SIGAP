import React from 'react';
import BeritaTrending from './BeritaTrending';
import BeritaTerkini from './BeritaTerkini';
import { Carousel } from 'react-bootstrap'; // Import Bootstrap Carousel
import poldaImage from '../assets/polda.png'; // Pastikan gambarnya diimport
import 'bootstrap/dist/css/bootstrap.min.css'; // Pastikan sudah import stylesheet Bootstrap
import { Link } from "react-router-dom";
import BeritaCard from "../components/BeritaCard";
import BeritaTrendingList from "../components/BeritaTrendingList";
import BeritaTerkiniList from "../components/BeritaTerkiniList";

const Home = () => (
  <div className="bg-white">
    {/* Carousel Full Width, Tinggi 50% Layar */}
    <div className="position-relative">
      <Carousel>
        <Carousel.Item>
          <div className="carousel-item-container">
            <img
              className="d-block w-100"
              src={poldaImage}
              alt="Polda"
            />
            {/* Overlay hitam transparan */}
            <div className="overlay" />
            {/* Teks tengah */}
            <Carousel.Caption className="position-absolute top-50 start-50 translate-middle text-center">
              <h1 className="text-white fw-bold">Selamat Datang di SIGAP</h1>
              <p className="text-white">Sistem Informasi dan Analisis Pemberitaan BID TIK Polda DIY</p>
            </Carousel.Caption>
          </div>
        </Carousel.Item>
      </Carousel>
    </div>

    {/* Berita Trending Section */}
    <section>
      <div className="d-flex align-items-center mb-3">
        <Link to="/berita-trending" className="text-dark text-decoration-none">
          <h2 className="fw-bold">Berita Trending Hari Ini</h2>
        </Link>
      </div>
      <BeritaTrendingList />
    </section>

    {/* Berita Terkini Section */}
    <section>
      <div className="d-flex align-items-center mb-3">
        <Link to="/berita-terkini" className="text-dark text-decoration-none">
          <h2 className="fw-bold">Berita Terkini</h2>
        </Link>
      </div>
      <BeritaTerkiniList />
    </section>

    {/* Grafik Berita Trending (Placeholder) */}
    <div className="container mt-5">
      <h4 className="fw-bold">Grafik Berita Trending</h4>
      <div className="bg-light p-5 text-center">
        {/* Chart Placeholder */}
        <p>Grafik Berita Trending akan ditampilkan di sini</p>
      </div>
    </div>

  </div>
);

export default Home;