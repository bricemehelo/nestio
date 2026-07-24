// src/components/__tests__/Map.test.tsx
//
// PURPOSE: Tests for the Map component.
// MapLibre GL JS relies on WebGL which is unavailable in jsdom.
// We mock MapLibre entirely and test only our component's behaviour —
// does it mount, does it react to selected property changes.

import { render, screen } from "@testing-library/react";
import { Provider } from "jotai";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Map from "../Map";

// Mock MapLibre entirely — WebGL is not available in jsdom test environment
// We replace the real library with a lightweight fake that satisfies our component
vi.mock("maplibre-gl", () => ({
  Map: vi.fn().mockImplementation(() => ({
    addControl: vi.fn(),
    remove: vi.fn(),
    flyTo: vi.fn(),
    on: vi.fn(),
  })),
  NavigationControl: vi.fn().mockImplementation(() => ({})),
  Marker: vi.fn().mockImplementation(() => ({
    setLngLat: vi.fn().mockReturnThis(),
    setPopup: vi.fn().mockReturnThis(),
    addTo: vi.fn().mockReturnThis(),
    remove: vi.fn(),
  })),
  Popup: vi.fn().mockImplementation(() => ({
    setHTML: vi.fn().mockReturnThis(),
  })),
}));
