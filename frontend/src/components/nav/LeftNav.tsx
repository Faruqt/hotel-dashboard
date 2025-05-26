

// component imports
import NavItem from './NavItem';

// static imports
import { ReactComponent as HomeIcon } from '../../assets/icons/home.svg';

function LeftNav() {
    return (
        <div className="left-nav">
        <ul>
            <NavItem label="Home" href="/" icon={<HomeIcon />} />
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
        </div>
    );
    }

export default LeftNav;