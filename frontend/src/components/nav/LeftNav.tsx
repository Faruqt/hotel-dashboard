// component imports
import NavItem from "./NavListItem";

// static imports
import { ReactComponent as HomeIcon } from "../../assets/icons/home.svg";
import { ReactComponent as LogoIcon } from "../../assets/icons/logo.svg";

function LeftNav() {
  return (
    <div className="bg-dark pt-[31px] w-[200px] min-w-[200px]">
      <div className="pl-[22px] mb-[38px]">
        <LogoIcon />
      </div>
      <ul>
        <NavItem label="Rooms" href="/" icon={<HomeIcon />} />
      </ul>
    </div>
  );
}

export default LeftNav;
