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
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useAtom } from "jotai";
import { selectedPropertyIdAtom } from "../store/propertyAtoms";
import { useFilteredProperties } from "../hooks/useProperties";
import type { Property } from "../types/property";

const Map = () => {
  // mapContainer is a ref to the DOM element MapLibre will render into
  const mapContainer = useRef<HTMLDivElement>(null);

  // map is a ref to the MapLibre instance — we use a ref not state because
  // changing the map instance should not trigger a React re-render
  const map = useRef<maplibregl.Map | null>(null);

  // markers ref stores all current markers so we can remove them before re-adding
  const markers = useRef<maplibregl.Marker[]>([]);

  const [selectedPropertyId, setSelectedPropertyId] = useAtom(
    selectedPropertyIdAtom,
  );

  // Get filtered properties — same data as PropertyList, driven by Jotai atoms
  const { data } = useFilteredProperties();

  // Initialise the map once on mount
  useEffect(() => {
    if (map.current || !mapContainer.current) return;

    // Small delay to ensure the container has a rendered height before MapLibre initialises
    const timeout = setTimeout(() => {
      console.log("Container:", mapContainer.current);
      console.log("Container height:", mapContainer.current?.clientHeight);

      if (!mapContainer.current) {
        console.log("Container is null — map cannot initialise");
        return;
      }

      map.current = new maplibregl.Map({
        container: mapContainer.current!,
        style: {
          version: 8,
          sources: {
            "raster-tiles": {
              type: "raster",
              tiles: [
                `https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=${import.meta.env.VITE_MAPTILER_API_KEY}`,
              ],
              tileSize: 256,
            },
          },
          layers: [
            {
              id: "raster-layer",
              type: "raster",
              source: "raster-tiles",
            },
          ],
        },
        center: [3.3792, 6.5244],
        zoom: 11,
      });

      map.current.on("load", () => {
        console.log("Map loaded successfully");
        console.log(
          "Map size:",
          map.current?.getCanvas().width,
          map.current?.getCanvas().height,
        );
      });

      map.current.addControl(new maplibregl.NavigationControl(), "top-right");

      map.current.on("error", (e) => {
        if (e.error?.message?.includes("WebGL2")) {
          const container = mapContainer.current;
          if (container) {
            container.innerHTML = `
            <div style="display:flex;align-items:center;justify-content:center;height:100%;background:#f8f9fa;flex-direction:column;gap:12px;padding:24px;text-align:center;">
              <span style="font-size:48px;">🗺️</span>
              <strong style="font-size:16px;">Map unavailable</strong>
              <p style="color:#6c757d;font-size:14px;margin:0;">
                Your browser doesn't support WebGL2 which is required to render the map.
                Try Chrome or Firefox with hardware acceleration enabled.
              </p>
            </div>
          `;
          }
        }
      });
    }, 100);

    return () => {
      clearTimeout(timeout);
      map.current?.remove();
      map.current = null;
    };
  }, []);

  // Add markers whenever properties data changes
  useEffect(() => {
    if (!map.current || !data?.properties) return;

    // Remove all existing markers before adding new ones
    // Prevents duplicate markers when filters change
    markers.current.forEach((marker) => marker.remove());
    markers.current = [];

    // Add a marker for each property
    data.properties.forEach((property: Property) => {
      // Create a custom marker element so we can style it
      const el = document.createElement("div");
      el.style.cssText = `
        width: 32px;
        height: 32px;
        background-color: ${property.id === selectedPropertyId ? "#1E1E2E" : "#2D6A4F"};
        border: 2px solid #FFFFFF;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: background-color 0.2s ease;
      `;
      el.innerHTML = "🏠";

      // Create popup with basic property info
      const popup = new maplibregl.Popup({ offset: 20 }).setHTML(`
        <div style="font-family: Arial, sans-serif; padding: 4px;">
          <strong style="font-size: 13px;">${property.title}</strong><br/>
          <span style="color: #2D6A4F; font-weight: bold;">
            ₦${Number(property.price).toLocaleString("en-NG")}
          </span><br/>
          <span style="font-size: 12px; color: #6C757D;">${property.city}</span>
        </div>
      `);

      // Create and add the marker to the map
      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([property.longitude, property.latitude])
        .setPopup(popup)
        .addTo(map.current!);

      // Clicking a marker updates the global selected property atom
      // This highlights the matching PropertyCard in the left panel
      el.addEventListener("click", () => {
        setSelectedPropertyId(property.id);
      });

      markers.current.push(marker);
    });
  }, [data?.properties, selectedPropertyId]);

  // Fly to selected property when selectedPropertyIdAtom changes
  // This triggers when user clicks a PropertyCard in the left panel
  useEffect(() => {
    if (!map.current || !selectedPropertyId || !data?.properties) return;

    const selected = data.properties.find((p) => p.id === selectedPropertyId);
    if (!selected) return;

    // Smoothly animate the map to the selected property's coordinates
    map.current.flyTo({
      center: [selected.longitude, selected.latitude],
      zoom: 14,
      duration: 1000, // Animation duration in milliseconds
    });
  }, [selectedPropertyId]);

  return <div ref={mapContainer} style={{ width: "100%", height: "100%" }} />;
};

export default Map;
