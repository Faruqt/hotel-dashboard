export type RoomResponse = {
  id?: string;
  title: string;
  description: string;
  image_path?: string;
  pdf_path?: string;
  facilities_count?: number;
  facilities_list?: string[];
  created_at_str: string;
  updated_at_str: string;
};

export type Room = {
  id?: string;
  title: string;
  description: string;
  imagePath?: string;
  pdfPath?: string;
  facilities?: string[];
  facilitiesCount?: string;
  createdAt: string;
  updatedAt: string;
};
