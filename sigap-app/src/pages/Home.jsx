import React from 'react';
import { Carousel } from 'react-bootstrap';
import { Link } from "react-router-dom";

import poldaImage from '../assets/polda.png';
import 'bootstrap/dist/css/bootstrap.min.css';

import BeritaTrendingList from "../components/BeritaTrendingList";
import BeritaTerkiniList from "../components/BeritaTerkiniList";
import Grafik from "../components/Grafik";

const Home = () => (
  <div className="bg-white">
    {/* Carousel */}
    <div className="position-relative">
      <Carousel>
        <Carousel.Item>
          <div className="carousel-item-container">
            <img className="d-block w-100" src={poldaImage} alt="Polda" />
            <div className="overlay" />
            <Carousel.Caption className="carousel-caption text-center">
              <h1 className="text-white fw-bold">Selamat Datang di SIGAP</h1>
              <p className="text-white">Sistem Informasi dan Analisis Pemberitaan BID TIK Polda DIY</p>
            </Carousel.Caption>
          </div>
        </Carousel.Item>
      </Carousel>
    </div>


    {/* Berita Trending */}
    <section>
      <div className="d-flex align-items-center mb-3">
        <Link to="/berita-trending" className="text-dark text-decoration-none">
          <h2 className="fw-bold">Berita Trending Hari Ini</h2>
        </Link>
      </div>
      <BeritaTrendingList />
    </section>

 <div className="container my-4=">
  <div className="d-flex flex-column flex-lg-row gap-4">
    {/* Kolom kiri: Berita Terkini */}
    <div className="flex-grow-1" style={{ flexBasis: '70%' }}>
      <section>
        <h2>Berita Terkini Hari Ini</h2>
        <BeritaTerkiniList />
      </section>
    </div>

    {/* Kolom kanan: Grafik */}
    <div className="flex-grow-1" style={{ flexBasis: '30%' }}>
      <section>
        <h2>Grafik Berita Terkini per Kategori</h2>
        <Grafik />
      </section>
    </div>
  </div>
</div>

  </div>
);

export default Home;
