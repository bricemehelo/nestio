// src/components/__tests__/Map.test.tsx
//
// PURPOSE: Map component testing is limited by jsdom's lack of WebGL support.
// MapLibre GL JS requires a real browser environment to initialise correctly.
// These tests verify the component can be imported without errors.
// Full map integration is verified manually in the browser.
//
// NOTE: For complete map testing, use Playwright or Cypress E2E tests
// which run in a real browser with WebGL support — a future addition.

import Map from "../Map";

vi.mock("maplibre-gl/dist/maplibre-gl.css", () => ({}));

vi.mock("maplibre-gl", () => ({
  Map: vi.fn(),
  NavigationControl: vi.fn(),
  Marker: vi.fn(),
  Popup: vi.fn(),
}));

vi.mock("../../hooks/useProperties", () => ({
  useFilteredProperties: vi.fn().mockReturnValue({
    data: { total: 0, properties: [] },
    isLoading: false,
    error: null,
  }),
}));

describe("Map", () => {
  test("Map component can be imported without errors", () => {
    expect(Map).toBeDefined();
  });
});
