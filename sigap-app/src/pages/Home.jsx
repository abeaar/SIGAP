import React from 'react';
import { Carousel } from 'react-bootstrap';
import { Link } from "react-router-dom";

import poldaImage from '../assets/polda.png';
// import sigapImage from '../assets/carousel-sigap.png ';
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
            <Carousel.Caption className="carousel-caption text-center px-2 px-md-4">
              <h1 className="text-white fw-bold display-6 display-md-4 display-lg-3 mb-2" style={{ fontSize: 'clamp(1.5rem, 5vw, 2.8rem)' }}>
                SIGAP
              </h1>
              <p className="text-white fs-6 fs-md-5" style={{ fontSize: 'clamp(1rem, 3vw, 1.3rem)' }}>
                Sistem Informasi dan Analisis Pemberitaan BID TIK POLDA DIY
              </p>
            </Carousel.Caption>
          </div>
        </Carousel.Item>
        {/* <Carousel.Item>
          <img className="d-block w-100" src={sigapImage} alt="SIGAP" />
        </Carousel.Item> */}
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

    <div className="container my-4">
      <div className="row g-4">
        {/* Kolom kiri: Berita Terkini */}
        <div className="col-12 col-lg-8">
          <section>
            <Link to="/berita-terkini" className="text-dark text-decoration-none">
              <h2 className="fw-bold">Berita Terkini Hari Ini</h2>
            </Link>
            <BeritaTerkiniList />
          </section>
        </div>
        {/* Kolom kanan: Grafik */}
        <div className="col-12 col-lg-4">
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
