import type { Meta, StoryObj } from "@storybook/react";

// local imports
import { PageSpinner } from "../LoadingSpinners";

const meta: Meta<typeof PageSpinner> = {
  title: "Components/PageSpinner",
  component: PageSpinner,
  tags: ["autodocs"],
};
export default meta;

type Story = StoryObj<typeof PageSpinner>;

export const Default: Story = {
  args: {},
};

export const Light: Story = {
  args: {
    color: "light",
  },
};

export const Dark: Story = {
  args: {
    color: "dark",
  },
};
