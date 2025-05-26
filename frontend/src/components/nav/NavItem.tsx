interface NavItemProps {
    label: string;
    href: string;
    icon: React.ReactNode;
}

function NavItem({ label, href, icon}:  NavItemProps ) {
    return (
        <li className="nav-item">
            <span className="nav-icon">
                {icon}
            </span>
            <a href={href} className="nav-link">
                {label}
            </a>
        </li>
    );
}

export default NavItem;