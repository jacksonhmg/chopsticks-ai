import { DebugForm } from "./debug.js";
import { ChopsticksForm } from "./formStuff.js";

console.log("index.js loaded")

function main() {
    new ChopsticksForm()
    if (document.querySelector(".debug-card")) {
        console.log("Debug card found")
        const debug = new DebugForm();
        debug.showResponse("");
    }

}

main();