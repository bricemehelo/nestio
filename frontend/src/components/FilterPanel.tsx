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
  const [city, setCity] = useAtome(selectedCityAtom);
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

  // const selectStyle = {
  //     width
  // }
};

export default FilterPanel;
