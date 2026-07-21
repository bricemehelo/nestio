// src/components/__tests__/FilterPanel.test.tsx
//
// PURPOSE: Tests for the FilterPanel component.
// Verifies filter controls render correctly and update global atoms on change.

import { render, screen, fireEvent } from "@testing-library/react";
import { Provider } from "jotai";
import FilterPanel from "../FilterPanel";

// Wrap with Jotai Provider so atoms work in tests
const renderFilterPanel = () => {
  return render(
    <Provider>
      <FilterPanel />
    </Provider>,
  );
};

describe("FilterPanel", () => {
  test("renders all filter controls", () => {
    renderFilterPanel();

    expect(screen.getByText("All Cities")).toBeInTheDocument();
    expect(screen.getByText("All Types")).toBeInTheDocument();
    expect(screen.getByText("All Statuses")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Min Price")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Max Price")).toBeInTheDocument();
    expect(screen.getByText("Reset Filters")).toBeInTheDocument();
  });

  test("reset button resets all filters", () => {
    renderFilterPanel();

    // Change city filter
    fireEvent.change(screen.getByDisplayValue("All Cities"), {
      target: { value: "Lagos" },
    });

    // Click reset
    fireEvent.click(screen.getByText("Reset Filters"));

    // City should be back to default
    expect(screen.getByDisplayValue("All Cities")).toBeInTheDocument();
  });

  test("selecting a city updates the dropdown", () => {
    renderFilterPanel();

    fireEvent.change(screen.getByDisplayValue("All Cities"), {
      target: { value: "Lagos" },
    });

    expect(screen.getByDisplayValue("Lagos")).toBeInTheDocument();
  });

  test("selecting a property type updates the dropdown", () => {
    renderFilterPanel();

    fireEvent.change(screen.getByDisplayValue("All Types"), {
      target: { value: "apartment" },
    });

    expect(screen.getByDisplayValue("Apartment")).toBeInTheDocument();
  });

  test("selecting a status updates the dropdown", () => {
    renderFilterPanel();

    fireEvent.change(screen.getByDisplayValue("All Statuses"), {
      target: { value: "for_sale" },
    });

    expect(screen.getByDisplayValue("For Sale")).toBeInTheDocument();
  });

  test("entering min price updates the input", () => {
    renderFilterPanel();

    fireEvent.change(screen.getByPlaceholderText("Min Price"), {
      target: { value: "1000000" },
    });

    expect(screen.getByDisplayValue("1000000")).toBeInTheDocument();
  });
});
