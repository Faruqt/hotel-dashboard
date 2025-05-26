// library imports
import { useState, useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";

// components import
import ButtonElement from "./Buttons";
import requestApi from "../lib/axios";
import ToastConfig from "../utils/toastConfig";

// static imports
import { ArrowRight, ArrowLeft } from "lucide-react";

type Room = {
  id: string;
  title: string;
  description: string;
  facilitiesCount: number;
  createdAt: string;
  updatedAt: string;
};

type RoomResponse = {
  id: string;
  title: string;
  description: string;
  facilities_count: number;
  created_at_str: string;
  updated_at_str: string;
};

function Listing() {
  const API_ENDPOINT = "/rooms";

  const navigate = useNavigate();

  const [rooms, setRooms] = useState<Room[]>([]);
  const [pageSize, setPageSize] = useState<number>(20);
  const [nextPage, setNextPage] = useState<number | null>(null);
  const [prevPage, setPrevPage] = useState<number | null>(null);

  useEffect(() => {
    fetchRooms(API_ENDPOINT);
  }, []);

  const handlePageChange = (pageNum: number) => {
    const url = API_ENDPOINT + `?page=${pageNum}&page_size=${pageSize}`;
    fetchRooms(url);
  };

  const handleRoomClick = (roomId: string) => () => {
    navigate(`/rooms/${roomId}`);
  };

  const handleCreateBtnClick = () => {
    navigate(`/rooms/`);
  };

  const fetchRooms = async (url: string) => {
    requestApi({
      method: "GET",
      url: url,
    })
      .then((response) => {
        setRooms(
          Array.isArray(response.data.data)
            ? response.data.data.map((room: RoomResponse) => ({
                id: room.id,
                title: room.title,
                description: room.description,
                facilitiesCount: room.facilities_count,
                createdAt: room.created_at_str,
                updatedAt: room.updated_at_str,
              }))
            : []
        );
        setNextPage(response.data.next_page);
        setPrevPage(response.data.prev_page);
        setPageSize(response.data.page_size);
      })
      .catch((error) => {
        toast.error("An error occurred while fetching rooms.", ToastConfig);
      });
  };

  return (
    <div className="min-w-[1060px]">
      <ToastContainer />
      <div className="flex items-center justify-between mb-[51px]">
        <div className="font-karla text-[40px] font-medium text-dark">
          All rooms
        </div>
        <div className="w-[173px]">
          <ButtonElement label="Create a Room" onClick={handleCreateBtnClick} />
        </div>
      </div>

      <div className="grid grid-cols-[190px_620px_70px_100px_100px] text-xs font-karla border-b py-2 justify-between text-dark">
        <div className="pl-2 pr-3 py-2 font-bold">Room</div>
        <div className="pl-2 pr-2 py-2 font-bold">Description</div>
        <div className="px-2 py-2 font-bold">Facilities</div>
        <div className="px-2 py-2 font-bold">Created</div>
        <div className="px-2 py-2 font-bold">Updated</div>
      </div>

      {rooms && rooms.length > 0 ? (
        rooms.map((room) => (
          <div
            key={room.id}
            className="grid grid-cols-[190px_620px_70px_100px_100px] text-xs font-merriweather border-b py-2 justify-between text-dark cursor-pointer"
            onClick={handleRoomClick(room.id)}
          >
            <div className="pl-2 py-2 pr-3 break-words whitespace-normal">
              {room.title}
            </div>
            <div className="pl-2 py-2 pr-2 break-words whitespace-normal">
              {room.description}
            </div>
            <div className="px-2 py-2">{room.facilitiesCount}</div>
            <div className="px-2 py-2">{room.createdAt || "-"}</div>
            <div className="px-2 py-2">{room.updatedAt || "-"}</div>
          </div>
        ))
      ) : (
        <div className="py-4 text-center text-gray-400">No rooms found.</div>
      )}

      <div className="flex items-center justify-between mt-6">
        <div
          onClick={() => {
            if (prevPage) {
              handlePageChange(prevPage);
            }
          }}
          className={`flex items-center gap-2 cursor-pointer ${
            !prevPage ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          <ArrowLeft />
          <span>Previous</span>
        </div>
        <div
          onClick={() => {
            if (nextPage) {
              handlePageChange(nextPage);
            }
          }}
          className={`flex items-center gap-2 cursor-pointer ${
            !nextPage ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          <span>Next</span>
          <ArrowRight />
        </div>
      </div>
    </div>
  );
}
export default Listing;
