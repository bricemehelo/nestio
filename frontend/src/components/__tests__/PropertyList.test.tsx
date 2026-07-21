// src/components/__tests__/PropertyList.test.tsx
//
// PURPOSE: Tests for the PropertyList component.
// Verifies loading, error, empty, and populated states render correctly.

import { render, screen } from "@testing-library/react";
import { Provider } from "jotai";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import PropertyList from "../PropertyList";

// Mock useFilteredProperties hook — we don't want real API calls in tests
vi.mock("../../hooks/useProperties", () => ({
  useFilteredProperties: vi.fn(),
}));

import { useFilteredProperties } from "../../hooks/useProperties";

// Helper — creates a fresh QueryClient for each test
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

// Helper — wraps component with all required providers
const renderPropertyList = () => {
  return render(
    <QueryClientProvider client={createTestQueryClient()}>
      <Provider>
        <PropertyList />
      </Provider>
    </QueryClientProvider>,
  );
};

const mockProperty = {
  id: 1,
  title: "3 Bedroom Flat in Lekki",
  description: "Spacious flat",
  price: "5000000.00",
  address: "12 Admiralty Way",
  city: "Lagos",
  latitude: 6.4281,
  longitude: 3.4219,
  property_type: "apartment" as const,
  status: "for_sale" as const,
  created_at: "2026-06-16T08:27:40.326862+01:00",
  updated_at: "2026-06-16T08:27:40.326862+01:00",
};

describe("PropertyList", () => {
  test("shows loading state", () => {
    (useFilteredProperties as any).mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    });

    renderPropertyList();

    expect(screen.getByText("Loading properties...")).toBeInTheDocument();
  });

  test("shows error state", () => {
    (useFilteredProperties as any).mockReturnValue({
      data: undefined,
      isLoading: false,
      error: new Error("Failed"),
    });

    renderPropertyList();

    expect(screen.getByText("Failed to load properties.")).toBeInTheDocument();
  });

  test("shows empty state when no properties found", () => {
    (useFilteredProperties as any).mockReturnValue({
      data: { total: 0, properties: [] },
      isLoading: false,
      error: null,
    });

    renderPropertyList();

    expect(screen.getByText("No properties found.")).toBeInTheDocument();
  });

  test("renders property cards when data is available", () => {
    (useFilteredProperties as any).mockReturnValue({
      data: { total: 1, properties: [mockProperty] },
      isLoading: false,
      error: null,
    });

    renderPropertyList();

    expect(screen.getByText("3 Bedroom Flat in Lekki")).toBeInTheDocument();
  });

  test("shows correct total count", () => {
    (useFilteredProperties as any).mockReturnValue({
      data: { total: 10, properties: [mockProperty] },
      isLoading: false,
      error: null,
    });

    renderPropertyList();

    expect(screen.getByText("Showing 1 of 10 properties")).toBeInTheDocument();
  });
});
