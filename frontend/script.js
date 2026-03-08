let chatMemory = []


// Load papers into dropdown
async function loadPapers(){

const res = await fetch("/papers")
const data = await res.json()

let select = document.getElementById("paperSelect")

select.innerHTML = ""

data.papers.forEach(p => {

let option = document.createElement("option")
option.value = p
option.text = p

select.appendChild(option)

})

}

loadPapers()


// Ask summarizer question
async function askQuestion(){

let question = document.getElementById("questionBox").value
let paper = document.getElementById("paperSelect").value

const res = await fetch("/ask",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
question:question,
selected_paper:paper
})

})

const data = await res.json()

if(data.out_of_context){

document.getElementById("summaryResult").innerText = data.message
document.getElementById("confidenceScore").innerText = "Low"

}else{

document.getElementById("summaryResult").innerText = data.summary
document.getElementById("confidenceScore").innerText = data.confidence + "%"

}

}



// Chat UI message
function addMessage(sender,text){

let div = document.createElement("div")

div.classList.add("message")

if(sender === "user"){
div.classList.add("user")
}else{
div.classList.add("bot")
}

div.innerText = sender + ": " + text

document.getElementById("chatHistory").appendChild(div)

}



// Chat discussion
async function sendChat(){

let input = document.getElementById("chatInput")

let question = input.value

if(question.trim() === ""){
return
}

addMessage("user",question)

chatMemory.push(question)

let paper = document.getElementById("paperSelect").value

const res = await fetch("/ask",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

question:chatMemory.join(" "),
selected_paper:paper

})

})

const data = await res.json()

addMessage("bot",data.summary)

chatMemory.push(data.summary)

input.value = ""

}



// Upload PDF
async function uploadPDF(){

let file = document.getElementById("pdfUpload").files[0]

let formData = new FormData()

formData.append("file",file)

await fetch("/upload_pdf",{

method:"POST",

body:formData

})

alert("PDF uploaded and processed!")

loadPapers()

}