import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import logoIcon from "../assets/logo-sigap.png";
import logoText from "../assets/name-sigap.png";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [date, setDate] = useState("");
  const [showNav, setShowNav] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    const keyword = e.target.keyword.value.trim();
    if (keyword) {
      navigate(`/search?keyword=${encodeURIComponent(keyword)}`);
    }
  };

  const handleDateChange = (e) => {
    const selectedDate = e.target.value;
    setDate(selectedDate);
    if (selectedDate) {
      navigate(`/filter-trending?date=${selectedDate}`);
    }
  };

  return (
    <>
      {/* Bagian Atas - Logo dan Search + Filter Date */}
      <div className="navbar-top-bg py-2 px-2 px-md-4">
        <div className="row align-items-center">
          <div className="col-12 col-md-6 d-flex align-items-center justify-content-center justify-content-md-start mb-2 mb-md-0">
            <img src={logoIcon} alt="SIGAP Icon" width="60" height="60" className="me-2" />
            <img src={logoText} alt="SIGAP Text" height="40" />
          </div>
          <div className="col-12 col-md-6 d-flex gap-2 align-items-center justify-content-center justify-content-md-end">
            <form onSubmit={handleSearch} className="position-relative w-100" style={{ maxWidth: 250 }}>
              <input
                type="text"
                name="keyword"
                className="form-control pe-5"
                placeholder="Cari berita..."
                aria-label="Search"
              />
              <button
                type="submit"
                className="btn position-absolute top-50 end-0 translate-middle-y me-2 p-0 text-secondary"
                style={{ zIndex: 2 }}
              >
                <i className="bi bi-search fs-5"></i>
              </button>
            </form>
            <input
              type="date"
              className="form-control"
              value={date}
              onChange={handleDateChange}
              style={{ maxWidth: 150 }}
            />
          </div>
        </div>
      </div>

      {/* Bagian Menu - Navigation Links */}
      <nav className="navbar navbar-expand-lg navbar-dark sticky-top shadow-sm">
        <div className="container-fluid">
          <button
            className="navbar-toggler"
            type="button"
            onClick={() => setShowNav(!showNav)}
            aria-controls="navbarNav"
            aria-expanded={showNav}
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className={`collapse navbar-collapse${showNav ? " show" : ""}`} id="navbarNav">
            <ul className="navbar-nav mx-auto justify-content-center">
              {/* Link Biasa */}
              <li className="nav-item">
                <Link className={`nav-link fw-semibold fs-5 ${location.pathname === "/" ? "active" : ""}`} to="/">Beranda</Link>
              </li>
              <li className="nav-item">
                <Link className={`nav-link fw-semibold fs-5 ${location.pathname === "/berita-terkini" ? "active" : ""}`} to="/berita-terkini">Berita Terkini</Link>
              </li>
              <li className="nav-item">
                <Link className={`nav-link fw-semibold fs-5 ${location.pathname === "/berita-trending" ? "active" : ""}`} to="/berita-trending">Berita Trending</Link>
              </li>
              {/* Dropdown Media */}
              <li className="nav-item dropdown">
                <Link
                  className={`nav-link dropdown-toggle fw-semibold fs-5 ${location.pathname.startsWith("/media") ? "active" : ""}`}
                  to="#"
                  id="mediaDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Media
                </Link>
                <ul className="dropdown-menu" aria-labelledby="mediaDropdown">
                  <li><Link className={`dropdown-item ${location.pathname === "/media/kedaulatanrakyat" ? "active" : ""}`} to="/media/kedaulatanrakyat">KRJogja</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/media/detik" ? "active" : ""}`} to="/media/detik">detikJogja</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/media/idntimes" ? "active" : ""}`} to="/media/idntimes">IDNTimesJogja</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/media/times" ? "active" : ""}`} to="/media/times">TIMESJogja</Link></li>
                </ul>
              </li>
              {/* Dropdown Kategori */}
              <li className="nav-item dropdown">
                <Link
                  className={`nav-link dropdown-toggle fw-semibold fs-5 ${location.pathname.startsWith("/kategori") ? "active" : ""}`}
                  to="#"
                  id="kategoriDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Kategori
                </Link>
                <ul className="dropdown-menu" aria-labelledby="kategoriDropdown">
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/hukum" ? "active" : ""}`} to="/kategori/hukum">Hukum</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/politik" ? "active" : ""}`} to="/kategori/politik">Politik</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/sosial" ? "active" : ""}`} to="/kategori/sosial">Sosial</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/ekonomi" ? "active" : ""}`} to="/kategori/ekonomi">Ekonomi</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/pendidikan" ? "active" : ""}`} to="/kategori/pendidikan">Pendidikan</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/teknologi" ? "active" : ""}`} to="/kategori/teknologi">Teknologi</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/kesehatan" ? "active" : ""}`} to="/kategori/kesehatan">Kesehatan</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/kriminal" ? "active" : ""}`} to="/kategori/kriminal">Kriminal</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/agama" ? "active" : ""}`} to="/kategori/agama">Agama</Link></li>
                  <li><Link className={`dropdown-item ${location.pathname === "/kategori/hiburan" ? "active" : ""}`} to="/kategori/Hiburan">Hiburan</Link></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;