// src/components/__tests__/Map.test.tsx
//
// PURPOSE: Tests for the Map component.
// MapLibre GL JS relies on WebGL which is unavailable in jsdom.
// We mock MapLibre entirely and test only our component's behaviour —
// does it mount, does it react to selected property changes.

import { render } from '@testing-library/react'
import { Provider } from 'jotai'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Map from '../Map'
import { useFilteredProperties } from '../../hooks/useProperties'

const { MapMock, NavigationControlMock, MarkerMock, PopupMock } = vi.hoisted(() => {
  const MapMock = vi.fn().mockImplementation(() => ({
    addControl: vi.fn(),
    remove: vi.fn(),
    flyTo: vi.fn(),
    on: vi.fn(),
  }))

  const NavigationControlMock = vi.fn().mockImplementation(() => ({}))

  const MarkerMock = vi.fn().mockImplementation(() => ({
    setLngLat: vi.fn().mockReturnThis(),
    setPopup: vi.fn().mockReturnThis(),
    addTo: vi.fn().mockReturnThis(),
    remove: vi.fn(),
  }))

  const PopupMock = vi.fn().mockImplementation(() => ({
    setHTML: vi.fn().mockReturnThis(),
  }))

  return { MapMock, NavigationControlMock, MarkerMock, PopupMock }
})

vi.mock('maplibre-gl', () => ({
  Map: MapMock,
  NavigationControl: NavigationControlMock,
  Marker: MarkerMock,
  Popup: PopupMock,
}))

vi.mock('maplibre-gl/dist/maplibre-gl.css', () => ({}))

vi.mock('../../hooks/useProperties', () => ({
  useFilteredProperties: vi.fn().mockReturnValue({
    data: {
      total: 1,
      properties: [
        {
          id: 1,
          title: '3 Bedroom Flat in Lekki',
          description: 'Spacious flat',
          price: '5000000.00',
          address: '12 Admiralty Way',
          city: 'Lagos',
          latitude: 6.4281,
          longitude: 3.4219,
          property_type: 'apartment',
          status: 'for_sale',
          created_at: '2026-06-16T08:27:40.326862+01:00',
          updated_at: '2026-06-16T08:27:40.326862+01:00',
        },
      ],
    },
    isLoading: false,
    error: null,
  }),
}))

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })

const renderMap = () => {
  const queryClient = createTestQueryClient()
  return render(
    <QueryClientProvider client={queryClient}>
      <Provider>