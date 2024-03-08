import { Module } from "noicejs";
import FakeTodoService from "../../todo/service/FakeTodoService";

export default class ServicesModule extends Module {
  override async configure(): Promise<void> {
    this.bind("todoService").toInstance(new FakeTodoService());
  }
}
