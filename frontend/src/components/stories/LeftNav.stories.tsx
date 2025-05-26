import type { Meta, StoryObj } from "@storybook/react";
import { MemoryRouter } from "react-router-dom";

// local imports
import LeftNav from "../nav/LeftNav";

const meta: Meta<typeof LeftNav> = {
  title: "Nav/LeftNav",
  component: LeftNav,
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof LeftNav>;

export const Default: Story = {};
