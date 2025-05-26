import type { Meta, StoryObj } from "@storybook/react";

// local imports
import LabeledInput from "../LabeledInput";

const meta: Meta<typeof LabeledInput> = {
  title: "Components/LabeledInput",
  component: LabeledInput,
  tags: ["autodocs"],
};
export default meta;

type Story = StoryObj<typeof LabeledInput>;

export const Default: Story = {
  args: {
    label: "Username",
    placeholder: "Enter your username",
  },
};

export const WithValue: Story = {
  args: {
    label: "Email",
    value: "user@example.com",
    readOnly: true,
  },
};

export const Password: Story = {
  args: {
    label: "Password",
    type: "password",
    placeholder: "Enter your password",
  },
};

export const CustomClass: Story = {
  args: {
    label: "Custom",
    placeholder: "Custom styled input",
    className: "border-2 border-blue-500",
  },
};
