import React from 'react';
import logo from '../assets/logo-sigap.png';

const Footer = () => {
    return (
        <footer>
            <div className="container py-3 d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
                <div className="text-center text-md-start flex-shrink-0">
                    <img src={logo} alt="Logo TIK POLDA" style={{ width: 120, height: 'auto', marginBottom: 12 }} />
                </div>
                <div className="text-center text-md-start">
                    <p className="mb-0 fw-bold fs-5">
                        <a
                            href="https://jogja.polri.go.id/polda/satker/bid-tik.html"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-dark text-decoration-none"
                        >
                            TIK POLDA DIY
                        </a>
                    </p>
                    <p className="mb-0 fs-6">
                        <a
                            href="https://maps.app.goo.gl/5jkiGwjur564wAYX7"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-dark text-decoration-none"
                        >
                            Jl. Ring Road Utara, Sanggrahan, Condongcatur, Kec. Depok, Kabupaten Sleman
                        </a>
                    </p>
                    <p className="mb-0 fs-6">Daerah Istimewa Yogyakarta 55283</p>
                    <p className="mb-0 fs-6">(0274) 884444</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;