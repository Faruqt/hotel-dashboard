// library imports
import { useState, useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate, useParams } from "react-router-dom";

// components import
import ButtonElement from "./Buttons";
import LabeledInput from "./LabeledInput";
import requestApi from "../lib/axios";
import ToastConfig from "../utils/toastConfig";
import { PageSpinner } from "./LoadingSpinners";
import Modal from "./PopUpModal";

// static imports
import { ChevronLeft, TrashIcon } from "lucide-react";
import { ReactComponent as PlusIcon } from "../assets/icons/plusIcon.svg";
import { ReactComponent as DeleteIcon } from "../assets/icons/deleteIcon.svg";
import { ReactComponent as DownloadIcon } from "../assets/icons/download.svg";

// type imports
import { RoomResponse, Room } from "../types/room";

function RoomDetails() {
  const API_ENDPOINT = "/rooms";

  const navigate = useNavigate();

  const { id } = useParams<{ id: string }>();
  const emptyRoom: Room = {
    title: "",
    description: "",
    imagePath: "",
    createdAt: "",
    updatedAt: "",
  };
  const [room, setRoom] = useState<Room | null>(id ? null : emptyRoom);
  const [facilities, setFacilities] = useState<string[]>([""]);
  const [loading, setLoading] = useState<boolean>(false);
  const [pdfPath, setPdfPath] = useState<string>("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);

  useEffect(() => {
    if (id) {
      setLoading(true);
      const url = `${API_ENDPOINT}/${id}`;
      fetchRoom(url);
    }
  }, []);

  const handleBackClick = () => {
    navigate("/");
  };

  const handleAddFacility = () => {
    setFacilities((prev) => [...prev, ""]);
  };

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { value, name } = event.target;
    setRoom((prevData) => {
      if (!prevData) return prevData;
      return {
        ...prevData,
        [name]: value,
      } as Room;
    });
  };

  const handleFacilityRemoval = (index: number) => {
    setFacilities((prev) =>
      prev.length > 1 ? prev.filter((_, i) => i !== index) : prev
    );
  };

  const handleFacilityChange =
    (index: number, value: string) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const newFacilities = [...facilities];
      newFacilities[index] = event.target.value;
      setFacilities(newFacilities);
    };

  const updateRoomState = (roomData: RoomResponse) => {
    setRoom({
      id: roomData.id,
      title: roomData.title,
      description: roomData.description,
      imagePath: roomData.image_path,
      createdAt: roomData.created_at_str,
      updatedAt: roomData.updated_at_str,
    });
    setFacilities(roomData.facilities_list || []);
    setPdfPath(roomData.pdf_path || "");
  };

  const fetchRoom = async (url: string) => {
    requestApi({
      method: "GET",
      url: url,
    })
      .then((response) => {
        const room: RoomResponse = response.data;
        updateRoomState(room);
      })
      .catch((error) => {
        if (error.response && error.response.status === 404) {
          toast.error("Room not found.", ToastConfig);
          // route to rooms page
          navigate("/");
        } else {
          toast.error("An error occurred while fetching rooms.", ToastConfig);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setImageFile(file ?? null);
  };

  const handleCreateRoom = async () => {
    if (!room) {
      toast.error("Room data is not available.", ToastConfig);
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("title", room.title);
    formData.append("description", room.description || "");
    formData.append("facilities", JSON.stringify(facilities));
    formData.append("image", imageFile || "");

    requestApi({
      method: "POST",
      url: API_ENDPOINT,
      data: formData,
    })
      .then((response) => {
        toast.success("Room created successfully.", ToastConfig);
        const createdRoom: RoomResponse = response.data;
        updateRoomState(createdRoom);
        toast.info("Pdf generation in progress");
        //  then call generate pdf endpoint
        if (createdRoom.id) {
          handlePDFGeneration(createdRoom.id);
        }

        // navigate to details page
        navigate(`/rooms/${createdRoom.id}`);
      })
      .catch((error) => {
        const errMsg =
          typeof error?.response?.data?.detail === "string"
            ? error.response.data.detail
            : "An error occurred while creating rooms.";
        if (error.response && error.response.status === 400) {
          toast.error(errMsg, ToastConfig);
        } else if (error.response && error.response.status === 422) {
          toast.error(
            "Invalid data provided. Please check your input and ensure an image is also provided.",
            ToastConfig
          );
        } else {
          toast.error(errMsg, ToastConfig);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleUpdateRoom = async () => {
    if (!room) {
      toast.error("Room data is not available.", ToastConfig);
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("title", room.title);
    formData.append("description", room.description || "");
    formData.append("facilities", JSON.stringify(facilities));

    requestApi({
      method: "PUT",
      url: `${API_ENDPOINT}/${room.id}`,
      data: formData,
    })
      .then((response) => {
        toast.success("Room updated successfully.", ToastConfig);
        const updatedRoom: RoomResponse = response.data;
        updateRoomState(updatedRoom);
        toast.info("Pdf generation in progress");
        //  then call generate pdf endpoint

        if (room.id) {
          handlePDFGeneration(room.id);
        }
      })
      .catch((error) => {
        const errMsg =
          typeof error?.response?.data?.detail === "string"
            ? error.response.data.detail
            : "An error occurred while updating rooms.";
        if (error.response && error.response.status === 400) {
          toast.error(errMsg, ToastConfig);
        } else {
          toast.error(errMsg, ToastConfig);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handlePDFGeneration = async (id: string) => {
    // clear all toasts before generating PDF
    toast.dismiss();

    if (!room) {
      toast.error("Room data is not available.", ToastConfig);
      return;
    }
    setLoading(true);
    requestApi({
      method: "POST",
      url: `${API_ENDPOINT}/${id}/pdf`,
    })
      .then((response) => {
        const updatedRoom: RoomResponse = response.data;
        updateRoomState(updatedRoom);
        toast.success("PDF generated successfully.", ToastConfig);
      })
      .catch((error) => {
        toast.error("An error occurred while generating the PDF.", ToastConfig);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleDeleteRoom = async () => {
    if (!room || !room.id) {
      toast.error("Room data is not available.", ToastConfig);
      return;
    }
    setLoading(true);
    requestApi({
      method: "DELETE",
      url: `${API_ENDPOINT}/${room.id}`,
    })
      .then(() => {
        toast.success("Room deleted successfully.", ToastConfig);
        // navigate to rooms page
        navigate("/");
      })
      .catch((error) => {
        const errMsg =
          typeof error?.response?.data?.detail === "string"
            ? error.response.data.detail
            : "An error occurred while deleting the room.";
        if (error.response && error.response.status === 400) {
          toast.error(errMsg, ToastConfig);
        } else {
          toast.error(errMsg, ToastConfig);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="min-w-[1060px]">
      {loading && (
        <div className="fixed px-4 py-4 w-full h-full bg-overlay/40 z-[1000] top-0 left-0 isolate cursor-wait backdrop-blur-xs">
          <div className="h-full w-full flex items-center justify-center">
            <PageSpinner />
          </div>
        </div>
      )}
      <ToastContainer />
      <div className="items-cente mb-[51px]">
        <div className="font-karla text-[40px] font-medium text-dark">
          Room details
        </div>
        <div
          className="flex items-center cursor-pointer text-button font-merriweather"
          onClick={handleBackClick}
        >
          <ChevronLeft height={20} width={20} className="mr-1" />
          <span>back to rooms</span>
        </div>
      </div>

      <div className="flex justify-between mb-[51px]">
        <div className="font-karla">
          <div className="flex justify-between items-center mb-[23px] w-[600px]">
            <div className="text-xl font-medium text-dark">Room details</div>
            {id && (
              <div
                className="flex items-center gap-2 cursor-pointer text-button text-xs underline font-inter"
                onClick={() => setShowDeleteModal(true)}
              >
                <DeleteIcon width={15} height={15} className="mr-[3px]" />
                <span>DELETE ROOM</span>
              </div>
            )}
          </div>
          <div className="flex flex-col mb-[20px]">
            <span className="font-semibold text-xs mb-[7px]">Title</span>
            <input
              type="text"
              placeholder="Room title"
              value={room && room.title ? room.title : ""}
              name="title"
              onChange={handleChange}
              className="bg-input w-[600px] h-[44px] p-[15px] text-dark"
            />
          </div>
          <div className="flex flex-col mb-[30px]">
            <span className="font-semibold text-xs mb-[7px]">Description</span>
            <textarea
              placeholder="Room description"
              value={room && room.description ? room.description : ""}
              name="description"
              cols={15}
              onChange={handleChange}
              className="bg-input w-[600px] p-[15px] text-dark"
            />
          </div>
          <div className="flex flex-col mb-[20px]">
            <span className="font-semibold text-xs mb-[11px]">Image</span>
            {room && room.imagePath ? (
              <img
                src={room.imagePath ? room.imagePath : ""}
                alt="Room"
                className="w-[218px] h-[121px] object-cover"
              />
            ) : (
              <>
                <label className="flex items-center gap-2 cursor-pointer text-button text-xs underline font-inter mt-[9px] w-[165px]">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                  <PlusIcon width={15} height={15} className="mr-[3px]" />
                  <span>ADD IMAGE</span>
                </label>
                {imageFile ? (
                  <span className="mt-3 text-xs text-dark">
                    {imageFile.name}
                  </span>
                ) : null}
              </>
            )}
          </div>
          <div className="font-karla mt-[48px]">
            <div className="text-xl font-medium text-dark mb-[23px]">
              Facilities
            </div>
            <div className="flex flex-col mb-[20px]">
              {facilities.map((facility, index) => (
                <div className="flex items-center gap-2 mb-[10px]" key={index}>
                  <LabeledInput
                    label="Facility"
                    type="text"
                    placeholder="Facility detail"
                    value={facility}
                    name="facility"
                    onChange={handleFacilityChange(index, facility)}
                  />
                  <button
                    className="text-button text-xs underline font-inter mt-[9px] cursor-pointer"
                    onClick={() => handleFacilityRemoval(index)}
                  >
                    <TrashIcon width={15} height={15} className="mr-[3px]" />
                  </button>
                </div>
              ))}
            </div>

            <div
              className="flex items-center gap-2 cursor-pointer text-button text-xs underline font-inter mt-[9px]"
              onClick={handleAddFacility}
            >
              <PlusIcon width={15} height={15} className="mr-[3px]" />
              <span>ADD FACILITY</span>
            </div>
          </div>

          <div className="w-[278px] mt-[51px]">
            <ButtonElement
              label={id ? "Save and generate PDF" : "Create and generate PDF"}
              onClick={id ? handleUpdateRoom : handleCreateRoom}
            />
          </div>
        </div>
        <div className="w-[395px]">
          <div className="w-full h-[153px] bg-overlay pt-[27px] pl-[25px] pr-[78px] font-karla">
            <div className="text-xl font-medium text-dark mb-[27px]">Dates</div>
            <div className="flex justify-between mb-[27px]">
              <div className="flex flex-col justify-between">
                <span className="font-semibold text-xs mb-[7px]">Created</span>
                <span className="font-normal text-[13px] font-merriweather">
                  {room && room.createdAt ? room.createdAt : "-"}
                </span>
              </div>
              <div className="flex flex-col justify-between">
                <span className="font-semibold text-xs mb-[7px]">
                  {" "}
                  Updated{" "}
                </span>
                <span className="font-normal text-[13px] font-merriweather">
                  {room && room.updatedAt ? room.updatedAt : "-"}
                </span>
              </div>
            </div>
          </div>
          {pdfPath && (
            <a
              href={pdfPath}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block w-full mt-[29px]"
              download
            >
              <ButtonElement
                icon={<DownloadIcon width={24} height={24} />}
                label="Download PDF"
              />
            </a>
          )}
        </div>
      </div>

      {showDeleteModal && (
        <Modal
          onConfirm={handleDeleteRoom}
          onClose={() => setShowDeleteModal(false)}
          message="You are deleting a room..."
        />
      )}
    </div>
  );
}
export default RoomDetails;
