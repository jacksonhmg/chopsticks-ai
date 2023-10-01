import { sendForm } from "./request.js";

export class ChopsticksForm {
    constructor() {
        this.activateCreateForm();
    }
    activateCreateForm() {
        console.log("Create form activated")
        const chopsticksForm = document.querySelector(".send-state form");
        new CreateForm(chopsticksForm);
    }
}

class CreateForm{
    constructor(el){
        this.form = el;
        this.sendButton = el.querySelector("button[data-action='send']");
        this.sendButton.addEventListener("click", this.handleSendClick.bind(this));
    }

    handleSendClick(event){
        event.preventDefault();
        sendForm(this.form, "POST", "/api/ai", this.showResponse)    
    }

    showResponse(data){
        const parsedData = JSON.parse(data);
        const debugCard = document.querySelector(".debug-card");
        let field = debugCard.querySelector(".show-state");
        field.innerText = parsedData;
    }
}