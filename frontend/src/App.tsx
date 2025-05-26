import React from "react";
import { Routes, Route } from "react-router-dom";

// component imports
import LeftNav from "./components/nav/LeftNav";
import RoomListing from "./components/RoomListing";
import RoomDetails from "./components/RoomDetails";

function App() {
  return (
    <div className="flex h-screen">
      <LeftNav />
      <div className="pl-[61px] pt-[35px] pr-[23px] w-full overflow-x-auto">
        <Routes>
          <Route path="/" element={<RoomListing />} />
          <Route path="/rooms" element={<RoomDetails />} />
          <Route path="/rooms/:id" element={<RoomDetails />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
