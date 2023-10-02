import { sendForm } from "./request.js";

export class ChopsticksForm {
    constructor() {
        this.activateCreateForm();
        this.activeStrikeButton();
    }
    activateCreateForm() {
        console.log("Create form activated")
        const chopsticksForm = document.querySelector(".send-state form");
        new CreateForm(chopsticksForm);

        const attackButtons = document.querySelector(".attack-buttons")
        new AttackButtons(attackButtons);

    }

    activeStrikeButton() {
        const strikeButton = document.querySelector("button[data-action='strike']");
        const attackButtons = document.querySelector(".attack-buttons");

        strikeButton.addEventListener('click', function() {
            // Toggle the visibility of the attack buttons
            attackButtons.classList.toggle('hidden');
        });
    }
}

class AttackButtons{
    constructor(buttons){
        this.leftHitsLeft = buttons.querySelector("button[data-action='L-L']");
        this.leftHitsRight = buttons.querySelector("button[data-action='L-R']");
        this.rightHitsLeft = buttons.querySelector("button[data-action='R-L']");
        this.rightHitsRight = buttons.querySelector("button[data-action='R-R']");

        this.leftHitsLeft.addEventListener("click", this.handleLeftHitsLeft.bind(this));
        this.leftHitsRight.addEventListener("click", this.handleLeftHitsRight.bind(this));
        this.rightHitsLeft.addEventListener("click", this.handleRightHitsLeft.bind(this));
        this.rightHitsRight.addEventListener("click", this.handleRightHitsRight.bind(this));
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
        const feedback = document.querySelector(".feedback");
        feedback.innerText = "You hit the AI's left hand with your left hand!";
    }

    handleLeftHitsRight(event){
        event.preventDefault();
        console.log("Left hits right");
        const playerLeft = document.querySelector(".send-state form input.PL");
        const aiLeft = document.querySelector(".send-state form input[class='AR']");
        aiLeft.value = Number(playerLeft.value) + Number(aiLeft.value);
        if (aiLeft.value >= 5){
            aiLeft.value = 0;
        }
        const feedback = document.querySelector(".feedback");
        feedback.innerText = "You hit the AI's right hand with your left hand!";
    }

    handleRightHitsLeft(event){
        event.preventDefault();
        console.log("Right hits left");
        const playerLeft = document.querySelector(".send-state form input.PR");
        const aiLeft = document.querySelector(".send-state form input[class='AL']");
        aiLeft.value = Number(playerLeft.value) + Number(aiLeft.value);
        if (aiLeft.value >= 5){
            aiLeft.value = 0;
        }
        const feedback = document.querySelector(".feedback");
        feedback.innerText = "You hit the AI's right hand with your left hand!";
    }

    handleRightHitsRight(event){
        event.preventDefault();
        console.log("Right hits right");
        const playerLeft = document.querySelector(".send-state form input.PR");
        const aiLeft = document.querySelector(".send-state form input[class='AR']");
        aiLeft.value = Number(playerLeft.value) + Number(aiLeft.value);
        if (aiLeft.value >= 5){
            aiLeft.value = 0;
        }
        const feedback = document.querySelector(".feedback");
        feedback.innerText = "You hit the AI's right hand with your right hand!";
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

    showResponse = (data) => {
        const parsedData = JSON.parse(data);
        console.log("parsedData is ", parsedData)
        // let numbersArray = parsedData.split(',').map(Number);
        const pl = document.querySelector(".send-state form input.PL") 
        pl.value = parsedData[0];
        const pr = document.querySelector(".send-state form input.PR") 
        pr.value = parsedData[1];
        const al = document.querySelector(".send-state form input.AL") 
        al.value = parsedData[2];
        const ar = document.querySelector(".send-state form input.AR") 
        ar.value = parsedData[3];
        this.validateZeros();
        const attackButtons = document.querySelector(".attack-buttons");
        attackButtons.classList.add('hidden');
    }

    validateZeros() {
        const buttons = document.querySelector(".attack-buttons")
        const leftHitsLeft = buttons.querySelector("button[data-action='L-L']");
        const leftHitsRight = buttons.querySelector("button[data-action='L-R']");
        const rightHitsLeft = buttons.querySelector("button[data-action='R-L']");
        const rightHitsRight = buttons.querySelector("button[data-action='R-R']");



        const playerLeftInput = document.querySelector(".send-state form input.PL");
        if (Number(playerLeftInput.value) === 0) {
            leftHitsLeft.disabled = true;
            leftHitsRight.disabled = true;
        }

        const playerRightInput = document.querySelector(".send-state form input.PR");
        if (Number(playerRightInput.value) === 0) {
            rightHitsLeft.disabled = true;
            rightHitsRight.disabled = true;
        }

        const aiLeftInput = document.querySelector(".send-state form input.AL");
        if (Number(aiLeftInput.value) === 0) {
            leftHitsLeft.disabled = true;
            rightHitsLeft.disabled = true;
        }

        const aiRightInput = document.querySelector(".send-state form input.AR");
        if (Number(aiRightInput.value) === 0) {
            leftHitsRight.disabled = true;
            rightHitsRight.disabled = true;
        }
    }
}