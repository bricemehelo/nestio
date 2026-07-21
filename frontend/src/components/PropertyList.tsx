// src/components/PropertyList.tsx
//
// PURPOSE: Renders the list of properties returned by React Query.
// Reads selectedPropertyIdAtom to highlight the currently selected property.
// Connects useFilteredProperties hook to PropertyCard components.

import { useAtomValue } from "jotai";
import { selectedPropertyIdAtom } from "../store/propertyAtoms";
import { useFilteredProperties } from "../hooks/useProperties";
import PropertyCard from "./PropertyCard";

const PropertyList = () => {
  //Read filtered properties from React Query
  const { data, isLoading, error } = useFilteredProperties();

  // Read selected property ID to highlight the correct card
  const selectedPropertyId = useAtomValue(selectedPropertyIdAtom);

  if (isLoading) {
    return (
      <p style={{ color: "#6C757D", textAlign: "center" }}>
        Loading properties...
      </p>
    );
  }

  if (error) {
    return (
      <p style={{ color: "#DC3545", textAlign: "center" }}>
        Failed to load properties.
      </p>
    );
  }

  if (!data || data.properties.length === 0) {
    return (
      <p style={{ color: "#6C757D", textAlign: "center" }}>
        No properties found.
      </p>
    );
  }

  return (
    <div>
      {/* Total count */}
      <p style={{}}>
        Showing {data.properties.length} of {data.total} properties
      </p>
      {data.properties.map((property) => (
        <PropertyCard
          key={property.id}
          property={property}
          isSelected={property.id === selectedPropertyId}
        />
      ))}
    </div>
  );
};
export default PropertyList;
