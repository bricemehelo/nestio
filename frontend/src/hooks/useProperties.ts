// src/hooks/useProperties.ts
//
// PURPOSE: Custom React Query hooks for all property data fetching.
// Components call these hooks instead of calling the API directly.
//
// WHY HOOKS: React Query handles caching, loading, error states automatically.
// A component just calls useProperties() and gets data, isLoading, error back —
// no useEffect, no manual state management needed.

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { propertiesApi } from "../api/properties";
import type { PropertyFilters } from "../types/property";
// Add this import at the top
import { useAtomValue } from "jotai";
import {
  activeFiltersAtom,
  selectedPropertyIdAtom,
} from "../store/propertyAtoms";

// Query key factory — centralises cache keys so invalidation is consistent
// When we delete a property, we invalidate ['properties'] to refetch the list

const PROPERTY_KEYS = {
  all: ["properties"] as const,
  filtered: (filters: PropertyFilters) => ["properties", filters] as const,
  detail: (id: number) => ["properties", id] as const,
};

// Fetch all properties with optional filters
// isLoading is true while fetching, data is undefined until resolved

export const useProperties = (filters: PropertyFilters = {}) => {
  return useQuery({
    queryKey: PROPERTY_KEYS.filtered(filters),
    queryFn: () => propertiesApi.getAll(filters),
  });
};

// Fetch a single property by ID
// Only runs when id is defined — prevents fetching with undefined id
export const useProperty = (id: number | null) => {
  return useQuery({
    queryKey: PROPERTY_KEYS.detail(id!),
    queryFn: () => propertiesApi.getById(id!),
    enabled: id !== null,
  });
};

// Delete a property — mutation because it changes server state
// On success, invalidates the properties list cache to trigger a refetch
export const useDeleteProperty = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => propertiesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROPERTY_KEYS.all });
    },
  });
};

// Connects Jotai filter state directly to React Query
// When any filter atom changes, this automatically fires a new API call
export const useFilteredProperties = () => {
  const filters = useAtomValue(activeFiltersAtom);
  return useProperties(filters);
};
