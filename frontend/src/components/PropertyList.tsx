// src/components/PropertyList.tsx
//
// PURPOSE: Renders the list of properties returned by React Query.
// Reads selectedPropertyIdAtom to highlight the currently selected property.
// Connects useFilteredProperties hook to PropertyCard components.

import { useAtomValue } from "jotai";
