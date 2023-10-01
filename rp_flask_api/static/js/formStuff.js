import { sendForm } from "./request.js";

export class ChopsticksForm {
    constructor() {
        this.activateCreateForm();
    }
    activateCreateForm() {
        console.log("Create form activated")
        const chopsticksForm = document.querySelector(".send-state form");
        new CreateForm(chopsticksForm);

        const attackButtons = document.querySelector(".attack-buttons")
        new AttackButtons(attackButtons);

    }
}

class AttackButtons{
    constructor(buttons){
        this.leftHitsLeft = buttons.querySelector("button[data-action='L-L']");
        this.leftHitsRight = buttons.querySelector("button[data-action='L-R']");
        this.rightHitsLeft = buttons.querySelector("button[data-action='R-L']");
        this.rightHitsRight = buttons.querySelector("button[data-action='R-R']");

        this.leftHitsLeft.addEventListener("click", this.handleLeftHitsLeft.bind(this));
    }

    handleLeftHitsLeft(event){
        event.preventDefault();
        console.log("Left hits left");
        const playerLeft = document.querySelector(".send-state form input.PL");
        const aiLeft = document.querySelector(".send-state form input[class='AL']");
        aiLeft.value = Number(playerLeft.value) + Number(aiLeft.value);
        if (aiLeft.value >= 5){
            aiLeft.value = 0;
        }
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