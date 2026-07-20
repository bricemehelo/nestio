// src/store/propertyAtoms.ts
//
// PURPOSE: Global state atoms for property search, filtering, and selection.
// These atoms are the single source of truth for all UI filter state.
//
// PATTERN: Observer — any component reading an atom automatically re-renders
// when that atom changes. No prop drilling, no manual subscriptions needed.
//
// WHY JOTAI: Atomic state means only components consuming a specific atom
// re-render on change — not the entire component tree like React Context.

import { atom } from "jotai";
import type {
  PropertyFilters,
  PropertyStatus,
  PropertyType,
} from "../types/property";

//Search term
// Empty string means no search term is applied
export const searchAtom = atom<string>("");

//selected property type
// null means no city filter applied
export const selectedPropertyTypeAtom = atom<PropertyType | null>(null);

//Selected property type
// null mean so type filter
export const selectedCityAtom = atom<string | null>(null);

// Selected status atom e.g: "for sale", "for rent", or null for no filter
//null means no status filter applied
export const selectedStatusAtom = atom<PropertyStatus | null>(null);

//Price range atoms - min and max price filters
// null means no price filter applied
export const minPriceAtom = atom<number | null>(null);
export const maxPriceAtom = atom<number | null>(null);

//Selected property ID atom - set when user clicks a map marker or property card to view details
// null means no property is selected
export const selectedPropertyIdAtom = atom<number | null>(null);

// Derived atom — combines all filter atoms into a single PropertyFilters object
// React Query reads this atom to know what filters to apply to the API call
// This is a computed atom — it reads other atoms and derives a new value
// When any filter atom changes, this atom updates automatically

export const activeFilterAtom = atom<PropertyFilters>((get) => {
  const search = get(searchAtom);
  const city = get(selectedCityAtom);
  const property_type = get(selectedPropertyTypeAtom);
  const status = get(selectedStatusAtom);
  const min_price = get(minPriceAtom);
  const max_price = get(maxPriceAtom);

  // Build the filters object — only include non-null, non-empty values
  // Sending null or empty string to the API would break the query
  return {
    ...(search && { search }),
    ...(city && { city }),
    ...(property_type && { property_type }),
    ...(status && { status }),
    ...(min_price !== null && { min_price }),
    ...(max_price !== null && { max_price }),
    limit: 100,
  };
});
