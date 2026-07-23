// src/components/Map.tsx
//
// PURPOSE: Renders the interactive MapLibre GL JS map with property markers.
// Markers are derived from the filtered properties list.
// Clicking a marker updates selectedPropertyIdAtom — which highlights
// the matching PropertyCard in the left panel.
//
// PATTERN: Observer — the map watches selectedPropertyIdAtom and flies
// to the selected property's coordinates when it changes.

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useAtom } from "jotai";
import { selectedPropertyIdAtom } from "../store/propertyAtoms";
import { useFilteredProperties } from "../hooks/useProperties";
import type { Property } from "../types/property";

const Map = () => {
  //mapContainer is a ref to the DOM element Maplibre will render into
  const mapContainer = useRef<HTMLDivElement>(null);

  //map ref to the map instance
  //we use ref so that changing the map will not trigger a re render
  const map = useRef<maplibregl | null>(null);

  // markers ref
  const markers = useRef<maplibregl.Marker[]>([]);

  const [selectedPropertyId, setSelectedPropertyId] = useAtom(
    selectedPropertyIdAtom,
  );

  // Get filtered properties - same data as propertyList
  const { data } = useFilteredProperties();

  //initialise the maponce on mount
  useEffect(() => {
    if (map.current || !mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      // free tile provider , no api key
      style: "https://tiles.openfreemap.org/styles/liberty",
      center: [3.3792, 6.5244], // lagos coordinates
      zoom: 11,
    });
  });
};

export default Map;
