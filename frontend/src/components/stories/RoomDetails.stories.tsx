import type { Meta, StoryObj } from "@storybook/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";

// local imports
import RoomDetails from "../RoomDetails";

// Mock data for edit mode
const mockRoomId = "123";
const mockRoomData = {
  id: mockRoomId,
  title: "Deluxe Suite",
  description: "A luxurious suite with a sea view.",
  imagePath: "https://via.placeholder.com/218x121",
  createdAt: "2024-05-26",
  updatedAt: "2024-05-27",
  facilities: ["WiFi", "Air Conditioning", "Mini Bar"],
  pdfPath: "/mock/path/to/room.pdf",
};

const meta: Meta<typeof RoomDetails> = {
  title: "Components/RoomDetails",
  component: RoomDetails,
  decorators: [
    (Story, context) => (
      <MemoryRouter initialEntries={["/rooms"]}>
        <Routes>
          {/* For create mode */}
          <Route path="/rooms" element={<Story />} />
        </Routes>
      </MemoryRouter>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof RoomDetails>;

// --- Create Mode ---
export const Create: Story = {
  args: {
    // No id param, so RoomDetails will be in create mode
    initialEntries: ["/rooms"],
  },
};
