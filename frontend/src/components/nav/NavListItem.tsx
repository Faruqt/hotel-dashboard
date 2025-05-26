// library imports
import { useLocation } from "react-router-dom";

interface NavItemProps {
    label: string;
    href: string;
    icon: React.ReactNode;
}

function NavItem({ label, href, icon}:  NavItemProps ) {
    const location = useLocation();
    const isActive = location.pathname === href;

    return (
        <li className="flex items-center gap-2 p-2 pl-[22px] hover:bg-overlay relative mb-4">
            {isActive && <span className="absolute left-0 w-[4px] h-[24px] bg-button mr-[18px]"></span>}
            <span className="mr-[11px]">
                {icon}
            </span>
            <a href={href} className="text-light font-inter">
                {label}
            </a>
        </li>
    );
}

export default NavItem;