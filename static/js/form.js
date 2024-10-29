
   
const WIDTH = 800;
let selectedCompressedFile;

let input = document.getElementById("product_image");

input.addEventListener("change", (event) => {
    let image_file = event.target.files[0];
    
    let reader = new FileReader();
    reader.readAsDataURL(image_file);

    reader.onload = (event) => {
        let image_url = event.target.result;
        
        let image = document.createElement("img");
        image.src = image_url;

        image.onload = (e) => {
            let canvas = document.createElement("canvas");
            let ratio = WIDTH / e.target.width;
            canvas.width = WIDTH;
            canvas.height = e.target.height * ratio;
        
            const context = canvas.getContext("2d");
            context.drawImage(image, 0, 0, canvas.width, canvas.height);
        
            let new_image_url = canvas.toDataURL("image/jpeg", 98);
            let new_image = document.createElement("img");
            new_image.src = new_image_url;
            document.getElementById("wrapper").appendChild(new_image); 
            // console.log("Image URL: ", new_image_url)

            selectedCompressedFile = urlToFile(new_image_url)
            
            
            
        };
    };
});

let urlToFile = (url) => {

    let arr = url.split(",")
    // console.log(arr)
    let mime = arr[0].match(/:(.*?);/)[1]
    let data = arr[1]

    let dataStr = atob(data)
    let n = dataStr.length
    let dataArr = new Uint8Array(n)

    while(n--)
    {
        dataArr[n] = dataStr.charCodeAt(n)
    }

    let file  = new File([dataArr], 'File.jpg', {type: mime})

    return file



}



const formElem = document.getElementById("form");
formElem.onsubmit = async (e) => {  
    e.preventDefault();
    const data=new FormData(formElem)
    data.append('compressedFile', selectedCompressedFile)
    data.delete("image")
    let response = await fetch(window.location.href, {  
      method: 'POST',  
      body: data  ,
      headers: {
        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if necessary
    }
    });  
  
    let result = await response.json();  
    const messages = document.getElementById("messagesPlace")
    if(result["status"] == "error") {
        const newMessage = document.createElement("li")
        newMessage.innerHTML = `<li class="${result['status']}">${result['message']}</li>`
          messages.append(newMessage)
    }else {
        window.location.href = "/add_product/"
        
    }
    Console.log(result);  
  };  


  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}