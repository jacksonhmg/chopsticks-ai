export function getData(endpoint, callback) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {
      if (request.readyState === 4) {
        callback(request.response);
      }
    };
    request.open("GET", endpoint);
    request.send();
  }

  export function sendForm(form, action, endpoint, callback){
    const formData = new FormData(form);
    console.log([...formData.entries()]);
    let dataObject = Object.fromEntries(formData);
    dataObject.arrayInput = [...formData.getAll('arrayInput[]')];


    const debugCard = document.querySelector(".debug-card");
    let field = debugCard.querySelector(".show-id");
    const id = Number(field.innerText.trim());

    dataObject.id = id;

    dataObject = {
        id: dataObject.id,
        state: dataObject.arrayInput.map(Number)
    };

    const dataJSON = JSON.stringify(dataObject);

    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {
        if (request.readyState === 4) {
                callback(request.response);
            }
        };
    request.open(action, endpoint);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(dataJSON);
  }