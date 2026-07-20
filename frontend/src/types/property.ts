// src/types/property.ts
//
// PURPOSE: TypeScript type definitions for the Property resource.
// These mirror the Pydantic schemas on the backend — single source of truth
// for what a property looks like across the entire frontend.
//
// WHY TYPES: TypeScript catches mismatches between what the API returns
// and what components expect — at compile time, not runtime.

export type PropertyType =
  | "apartment"
  | "house"
  | "condo"
  | "townhouse"
  | "land"
  | "commercial";
export type PropertyStatus =
  | "for_sale"
  | "for_rent"
  | "sold"
  | "rented"
  | "off_market";

//Matches PropertyResponse schema from the backend

export interface Property {
  id: number;
  title: string;
  price: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  property_type: PropertyType;
  status: PropertyStatus;
  created_at: string;
  updated_at: string;
}

// Matches PropertyListResponse schema from the backend
export interface PropertyListResponse {
  total: number;
  properties: Property[];
}

// Matches PropertyCreate schema from the backend
export interface PropertyCreate {
  title: string;
  description: string;
  price: number;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  property_type: PropertyType;
  status: PropertyStatus;
}

// query params for filtering properties - mirrors the router's query params
export interface PropertyFilters {
  skip?: number;
  limit?: number;
  city?: string;
  property_type?: PropertyType;
  status?: PropertyStatus;
  search?: string;
  min_price?: number;
  max_price?: number;
}
