// src/components/FilterPanel.tsx
//
// PURPOSE: Filter controls that update global filter atoms.
// Each dropdown updates its own atom — activeFiltersAtom recomputes automatically
// and React Query fires a new API call with the updated filters

import { useAtom } from "jotai";
import {
  selectedCityAtom,
  selectedPropertyTypeAtom,
  selectedStatusAtom,
  minPriceAtom,
  maxPriceAtom,
} from "../store/propertyAtoms";

import type { PropertyType, PropertyStatus } from "../types/property";

const FilterPanel = () => {
  const [city, setCity] = useAtom(selectedCityAtom);
  const [propertyType, setPropertyType] = useAtom(selectedPropertyTypeAtom);
  const [status, setStatus] = useAtom(selectedStatusAtom);
  const [minPrice, setMinPrice] = useAtom(minPriceAtom);
  const [maxPrice, setMaxPrice] = useAtom(maxPriceAtom);

  //Reset all filters to their default null/empty state
  const handleReset = () => {
    setCity(null);
    setPropertyType(null);
    setStatus(null);
    setMinPrice(null);
    setMaxPrice(null);
  };

  const selectStyle = {
    width: "100%",
    padding: "8px 12px",
    borderRadius: "6px",
    border: "1px solid #DEE2E6",
    fontSize: "14px",
    marginBottom: "10px",
    backgroundColor: "#FFFFFF",
    cursor: "pointer",
  };

  return (
    <div style={{ marginBottom: "16px" }}>
      {/* City Filter */}
      <select
        value={city || ""}
        onChange={(e) => setCity(e.target.value || null)}
        style={selectStyle}
      >
        <option value="">All Cities</option>
        <option value="Lagos">Lagos</option>
        <option value="Abuja">Abuja</option>
        <option value="Port Harcourt">Port Harcourt</option>
        <option value="Ibadan">Ibadan</option>
      </select>

      {/* Property Type Filter */}
      <select
        value={propertyType || ""}
        onChange={(e) =>
          setPropertyType((e.target.value as PropertyType) || null)
        }
        style={selectStyle}
      >
        <option value="">All Types</option>
        <option value="apartment">Apartment</option>
        <option value="house">House</option>
        <option value="land">Land</option>
        <option value="commercial">Commercial</option>
      </select>

      {/* Status Filter */}
      <select
        value={status || ""}
        onChange={(e) => setStatus((e.target.value as PropertyStatus) || null)}
        style={selectStyle}
      >
        <option value="">All Statuses</option>
        <option value="for_sale">For Sale</option>
        <option value="for_rent">For Rent</option>
        <option value="sold">Sold</option>
        <option value="rented">Rented</option>
      </select>

      {/* Price Range */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "10px" }}>
        <input
          type="number"
          placeholder="Min Price"
          value={minPrice || ""}
          onChange={(e) =>
            setMinPrice(e.target.value ? Number(e.target.value) : null)
          }
          style={{ ...selectStyle, marginBottom: 0 }}
        />
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice || ""}
          onChange={(e) =>
            setMaxPrice(e.target.value ? Number(e.target.value) : null)
          }
          style={{ ...selectStyle, marginBottom: 0 }}
        />
      </div>

      {/* Reset Button */}
      <button
        onClick={handleReset}
        style={{
          width: "100%",
          padding: "8px",
          borderRadius: "6px",
          border: "1px solid #DEE2E6",
          backgroundColor: "#F8F9FA",
          cursor: "pointer",
          fontSize: "14px",
          color: "#495057",
        }}
      >
        Reset Filters
      </button>
    </div>
  );
};

export default FilterPanel;
