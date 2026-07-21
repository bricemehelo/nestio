// src/api/properties.ts
//
// PURPOSE: All API calls for the Property resource in one place.
// Components never call Axios directly — they call these typed functions.
//
// This mirrors the Repository pattern from the backend — all data access
// behind a clean interface, typed end to end.

import { apiClient } from "./client";
import type {
  Property,
  PropertyCreate,
  PropertyFilters,
  PropertyListResponse,
} from "../types/property";

export const propertiesApi = {
  // Fetch all properties with optional filters
  // Mirrors GET /api/properties/
  getAll: async (
    filters: PropertyFilters = {},
  ): Promise<PropertyListResponse> => {
    const { data } = await apiClient.get<PropertyListResponse>(
      "/api/properties/",
      { params: filters },
    );
    return data;
  },

  //Fetch a single property by ID
  // Mirrors GET /api/properties/{id}
  getById: async (id: number): Promise<Property> => {
    const { data } = await apiClient.get<Property>(`/api/properties/${id}`);
    return data;
  },

  //Create a new property
  // Mirrors POST /api/properties/
  create: async (property: PropertyCreate): Promise<Property> => {
    const { data } = await apiClient.post<Property>(
      "/api/properties/",
      property,
    );
    return data;
  },

  // Delete a property by ID
  // Mirrors DELETE /api/properties/{id}
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/properties/${id}`);
  },
};
