// src/App.tsx
//
// PURPOSE: Root component — assembles the full layout of Nestio.
// Left panel: SearchBar + FilterPanel + PropertyList
// Right panel: MapLibre GL JS interactive map

import SearchBar from "./components/SearchBar";
import FilterPanel from "./components/FilterPanel";
import PropertyList from "./components/PropertyList";
import Map from "./components/Map";

function App() {
  return (
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
          height: "100vh",
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

      {/* Right Panel — Map */}
      <div style={{ flex: 1, height: "100vh" }}>
        <Map />
      </div>
    </div>
  );
}

export default App;
