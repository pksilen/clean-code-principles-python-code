import { Container } from "noicejs";
import ServicesModule from "./ServicesModule";

const diContainer = Container.from(new ServicesModule());

export default diContainer;
