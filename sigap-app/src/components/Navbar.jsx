import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import logoIcon from "../assets/logo-sigap.png";
import logoText from "../assets/name-sigap.png";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [date, setDate] = useState("");

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
      <div className="d-flex justify-content-between align-items-center px-5 py-3">
        <div className="d-flex align-items-center">
          <img src={logoIcon} alt="SIGAP Icon" width="80" height="80" className="me-2" />
          <img src={logoText} alt="SIGAP Text" height="55" />
        </div>

        <div className="d-flex gap-2 align-items-center">
          <form onSubmit={handleSearch} className="position-relative">
            <input
              type="text"
              name="keyword"
              className="form-control pe-5"
              placeholder="Cari"
            />
            <button
              type="submit"
              className="btn btn-link position-absolute end-0 top-0 mt-2 me-2 p-0"
              style={{ zIndex: 2 }}
            >
              <i className="bi bi-search"></i>
            </button>
          </form>

          <input
            type="date"
            className="form-control"
            value={date}
            onChange={handleDateChange}
          />
        </div>
      </div>

      {/* Bagian Menu - Navigation Links */}
      <nav className="navbar navbar-expand-lg navbar-dark sticky-top shadow-sm">
        <div className="container-fluid">
          <ul className="navbar-nav d-flex flex-row flex-wrap gap-3 mx-auto justify-content-center">

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
                <li><Link className={`dropdown-item ${location.pathname === "/media/krjogja" ? "active" : ""}`} to="/media/krjogja">KRJogja</Link></li>
                <li><Link className={`dropdown-item ${location.pathname === "/media/detikjogja" ? "active" : ""}`} to="/media/detikjogja">detikJogja</Link></li>
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
                <li><Link className={`dropdown-item ${location.pathname === "/kategori/olahraga" ? "active" : ""}`} to="/kategori/olahraga">Olahraga</Link></li>
                <li><Link className={`dropdown-item ${location.pathname === "/kategori/kriminalitas" ? "active" : ""}`} to="/kategori/kriminalitas">Kriminalitas</Link></li>
                <li><Link className={`dropdown-item ${location.pathname === "/kategori/bisnis" ? "active" : ""}`} to="/kategori/bisnis">Bisnis</Link></li>
                <li><Link className={`dropdown-item ${location.pathname === "/kategori/seni" ? "active" : ""}`} to="/kategori/seni">Seni</Link></li>
              </ul>
            </li>

          </ul>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
