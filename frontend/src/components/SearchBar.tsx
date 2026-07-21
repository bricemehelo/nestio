// src/components/SearchBar.tsx
//
// PURPOSE: Search input that updates the global search atom.
// When the user types, the search atom updates, activeFiltersAtom recomputes,
// and React Query automatically fires a new filtered API call.
//
// No API calls here — this component only manages UI input and global state.

import { useAtom } from "jotai";
import { searchAtom } from "../store/propertyAtoms";

const SearchBar = () => {
  //useTome gives us both the value and the setter  - like useState but for global state
  const [search, setSearch] = useAtom(searchAtom);

  return (
    <div style={{ marginBottom: "16px" }}>
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search properties..."
        style={{
          width: "100%",
          padding: "10px 14px",
          borderRadius: "6px",
          border: "1px solid #DEE2E6",
          fontSize: "14px",
          outline: "none",
          boxSizing: "border-box",
        }}
      />
    </div>
  );
};

export default SearchBar;
