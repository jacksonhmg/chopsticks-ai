import { getData } from "./request.js";

export class DebugForm {
  constructor() {
    this.debugCard = document.querySelector(".debug-card");
    this.form = this.debugCard.querySelector(".debug-form");
    this.clearButton = this.form.querySelector("button[data-action='clear']");
    this.clearButton.addEventListener(
      "click",
      this.handleClearClick.bind(this)
    );
    this.sendButton = this.form.querySelector("button[data-action='read']");
    this.sendButton.addEventListener("click", this.handleSendClick.bind(this));
  }

  handleClearClick(event) {
    console.log("Clear button clicked")
    event.preventDefault();
    let code = this.debugCard.querySelector(".show-id");
    code.innerText = "";
  }

  handleSendClick(event) {
    console.log("Send button clicked")
    event.preventDefault();
    const endpoint = "/api/ai";
    getData(endpoint, this.showResponse);
  }

  showResponse(data) {
    const debugCard = document.querySelector(".debug-card");
    let field = debugCard.querySelector(".show-id");
    field.innerText = data;
  }
}