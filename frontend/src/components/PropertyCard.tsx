// src/components/PropertyCard.tsx
//
// PURPOSE: Displays a single property listing as a card.
// Pure presentational component — receives data via props, renders UI only.
//
// PATTERN: Presentational Component — no API calls, no global state.
// Data comes in via props, events go out via callback props.
// This separation makes the component reusable and easy to test.

import { useSetAtom } from "jotai";
import { selectedPropertyIdAtom } from "../store/propertyAtoms";
import type { Property } from "../types/property";

// Props interface - Typescript ensures the component receives the correct data shape

interface PropertyCardProps {
  property: Property;
  isSelected?: boolean;
}

// helper - formats price as readable currency string
// 50000 -> "N5,000,000"

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat("en-NG", {
    style: "currency",
    currency: "NGN",
    minimumFractionDigits: 0,
  }).format(price);
};

//Helper - formats status from snake_case to readable label
//for_sale -> "For Sale"
const formatStatus = (status: string): string => {
  return status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
};

const PropertyCard = ({ property, isSelected = false }: PropertyCardProps) => {
  // We only need the setter this component doesn't read the selectedPropertyIdAtom, it just sets it on click
  const setSelectedPropertyId = useSetAtom(selectedPropertyIdAtom);

  const handleClick = () => {
    //Update global atom , MapLibre map will react to this change
    setSelectedPropertyId(property.id);
  };
  return (
    <div
      onClick={handleClick}
      style={{
        border: isSelected ? "2px solid #2D6A4F" : "1px solid #DEE2E6",
        borderRadius: "8px",
        padding: "16px",
        marginBottom: "12px",
        cursor: "pointer",
        backgroundColor: isSelected ? "#D8F3DC" : "#FFFFFF",
        transition: "all 0.2s ease",
      }}
    >
      {/* Property title */}
      <h3 style={{ margin: "0 0 8px 0", fontSize: "16px", color: "#1E1E2E" }}>
        {property.title}
      </h3>
      {/* Property price */}
      <p
        style={{
          margin: "0 0 8px 0",
          fontSize: "18px",
          fontWeight: "bold",
          color: "#2D6A4F",
        }}
      >
        {formatPrice(Number(property.price))}
      </p>
      {/* Location */}
      <p style={{ margin: "0 0 4px 0", fontSize: "14px", color: "#6C757D" }}>
        📍 {property.address}, {property.city}
      </p>
      {/*  Type and Status */}
      <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
        <span
          style={{
            padding: "4px 8px",
            borderRadius: "4px",
            fontSize: "12px",
            backgroundColor: "#E9ECEF",
            color: "#495057",
            textTransform: "capitalize",
          }}
        >
          {property.property_type}
        </span>
        <span
          style={{
            padding: "4px 8px",
            borderRadius: "4px",
            fontSize: "12px",
            backgroundColor:
              property.status === "for_sale" ? "#D8F3DC" : "#FFF3CD",
            color: property.status === "for_sale" ? "#2D6A4F" : "#856404",
          }}
        >
          {formatStatus(property.status)}
        </span>
      </div>
    </div>
  );
};

export default PropertyCard;
