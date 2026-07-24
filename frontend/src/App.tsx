import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import "./App.css";
import Map from "./components/Map"; // Replace the placeholder div

// src/App.tsx
//
// PURPOSE: Root component — assembles the full layout of the application.
// Left panel: SearchBar + FilterPanel + PropertyList
// Right panel: Map (MapLibre GL JS — next phase)

import SearchBar from "./components/SearchBar";
import FilterPanel from "./components/FilterPanel";
import PropertyList from "./components/PropertyList";

function App() {
  return (
    <>
      <section id="center">
        <div className="hero">
          {/* <img src={heroImg} className="base" width="170" height="179" alt="" /> */}
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1> 🏠 Nestio</h1>
          <p>
            Find the best Accomodation in the country <code>HMR</code>
          </p>
        </div>
      </section>

      <div className="ticks"></div>
      <div
        style={{
          display: "flex",
          height: "100vh",
          fontFamily: "Arial, sans-serif",
        }}
      >
        {/* Left Panel — Search, Filters, Property List */}
        <div
          style={{
            width: "380px",
            minWidth: "380px",

            overflowY: "auto",
            padding: "20px",
            borderRight: "1px solid #DEE2E6",
            backgroundColor: "#F8F9FA",
          }}
        >
          <h1
            style={{ margin: "0 0 20px 0", fontSize: "22px", color: "#1E1E2E" }}
          >
            🏠 Nestio
          </h1>
          <SearchBar />
          <FilterPanel />
          <PropertyList />
        </div>

        {/* Right Panel — Map placeholder for now */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#E9ECEF",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#6C757D",
            fontSize: "18px",
          }}
        >
          <div style={{ flex: 1, height: "100vh" }}>
            <Map />
          </div>
          {/* 🗺️ Map coming next — MapLibre GL JS */}
        </div>
      </div>
      <section id="spacer"></section>
      <section id="next-steps">
        <div id="docs">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#documentation-icon"></use>
          </svg>
          <h2>Documentation</h2>
          <p>Your questions, answered</p>
          <ul>
            <li>
              <a href="https://vite.dev/" target="_blank">
                <img className="logo" src={viteLogo} alt="" />
                Explore Vite
              </a>
            </li>
            <li>
              <a href="https://react.dev/" target="_blank">
                <img className="button-icon" src={reactLogo} alt="" />
                Learn more
              </a>
            </li>
          </ul>
        </div>
        <div id="social">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#social-icon"></use>
          </svg>
          <h2>Connect with us</h2>
          <p>Join the Vite community</p>
          <ul>
            <li>
              <a href="https://github.com/vitejs/vite" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
            <li>
              <a href="https://chat.vite.dev/" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#discord-icon"></use>
                </svg>
                Discord
              </a>
            </li>
            <li>
              <a href="https://x.com/vite_js" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#x-icon"></use>
                </svg>
                X.com
              </a>
            </li>
            <li>
              <a href="https://bsky.app/profile/vite.dev" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#bluesky-icon"></use>
                </svg>
                Bluesky
              </a>
            </li>
          </ul>
        </div>
      </section>
    </>
  );
}

export default App;
