import { getData } from "./request.js";

export class DebugForm {
  constructor() {
    this.debugCard = document.querySelector(".debug-card");
    this.form = this.debugCard.querySelector(".debug-form");
    this.startButton = this.form.querySelector("button[data-action='start']");
    this.startButton.addEventListener("click", this.handleStartClick.bind(this));
  }

  handleStartClick(event) {
    console.log("Start button clicked")
    event.preventDefault();
    const form = document.querySelector(".send-state");
    form.classList.remove("hidden");
    const endpoint = "/api/ai";
    getData(endpoint, this.showResponse);
  }

  showResponse(data) {
    const debugCard = document.querySelector(".debug-card");
    let field = debugCard.querySelector(".show-id");
    field.innerText = data;
  }
}