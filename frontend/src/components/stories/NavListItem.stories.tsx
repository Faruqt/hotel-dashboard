import { MemoryRouter } from "react-router-dom";
import { Home } from "lucide-react";
import type { Meta, StoryObj } from "@storybook/react";

// local imports
import NavItem from "../nav/NavListItem";

const meta: Meta<typeof NavItem> = {
  title: "Nav/NavItem",
  component: NavItem,
  decorators: [
    (Story) => (
      <MemoryRouter initialEntries={["/"]}>
        <ul>
          <Story />
        </ul>
      </MemoryRouter>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof NavItem>;

export const Default: Story = {
  args: {
    label: "Home",
    href: "/",
    icon: <Home />,
  },
};

export const Active: Story = {
  args: {
    label: "Home",
    href: "/",
    icon: <Home />,
  },
  parameters: {
    reactRouter: {
      routePath: "/",
    },
  },
};

export const Inactive: Story = {
  args: {
    label: "Dashboard",
    href: "/dashboard",
    icon: <Home />,
  },
};
