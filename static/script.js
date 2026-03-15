window.onload=function(){

document.getElementById("scanTime").innerText=
new Date().toLocaleTimeString()

}


function processTransaction(){

document.getElementById("loader").style.display="block"
document.getElementById("scanStatus").innerText="SCANNING..."

let amount=document.getElementById("amount").value
let location=document.getElementById("location").value
let card=document.getElementById("card").value
let category=document.getElementById("category").value


fetch("/process",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

amount:amount,
location:location,
card:card,
category:category

})

})

.then(res=>res.json())

.then(data=>{


document.getElementById("total").innerText=data.total
document.getElementById("fraud").innerText=data.fraud
document.getElementById("risk").innerText=data.avg_risk.toFixed(0)+"%"



document.getElementById("totalCheck").innerText=data.total
document.getElementById("fraudCheck").innerText=data.fraud
document.getElementById("legitCount").innerText=data.total-data.fraud



let level=document.getElementById("riskLevel")

let avgRisk=data.avg_risk

if(avgRisk>=70){

level.innerText="HIGH RISK"
level.className="risk-badge high-risk"

}
else if(avgRisk>=40){

level.innerText="MEDIUM RISK"
level.className="risk-badge medium-risk"

}
else{

level.innerText="LOW RISK"
level.className="risk-badge low-risk"

}



let t=data.transaction



/* Risk Analysis */

let amountRisk=0
let locationRisk=0
let categoryRisk=0
let frequencyRisk=20
let timeRisk=30
let cardRisk=0


if(t.amount<2000) amountRisk=20
else if(t.amount<5000) amountRisk=40
else if(t.amount<10000) amountRisk=70
else amountRisk=100


let indian=["Delhi","Mumbai","Noida","Meerut","Lucknow"]

if(indian.includes(t.location))
locationRisk=20
else
locationRisk=100


if(category=="Grocery") categoryRisk=20
else if(category=="Shopping") categoryRisk=40
else if(category=="Travel") categoryRisk=70
else categoryRisk=90


if(card=="RuPay") cardRisk=20
else if(card=="Visa") cardRisk=40
else cardRisk=50


document.getElementById("amountRisk").innerText=amountRisk
document.getElementById("locationRisk").innerText=locationRisk
document.getElementById("categoryRisk").innerText=categoryRisk
document.getElementById("frequencyRisk").innerText=frequencyRisk
document.getElementById("timeRisk").innerText=timeRisk
document.getElementById("cardRisk").innerText=cardRisk

document.getElementById("finalRisk").innerText=t.risk+"%"



let feed=document.getElementById("activityFeed")

let item=document.createElement("li")

item.innerText=t.time+" - ₹"+t.amount+" ("+t.status+")"

feed.prepend(item)



if(t.status=="Fraud"){

let reason=""

if(amountRisk>=90) reason+="• High Transaction Amount\n"
if(locationRisk>=90) reason+="• Foreign Location\n"
if(categoryRisk>=70) reason+="• High Risk Category\n"

alert("⚠ Fraud Detected\n\nReason:\n"+reason+"\nRisk Score: "+t.risk+"%")

}



document.getElementById("loader").style.display="none"

document.getElementById("scanStatus").innerText="COMPLETED"

document.getElementById("scanTime").innerText=
new Date().toLocaleTimeString()

})

}



function clearDashboard(){

document.getElementById("total").innerText=0
document.getElementById("fraud").innerText=0
document.getElementById("risk").innerText="0%"

document.getElementById("totalCheck").innerText=0
document.getElementById("fraudCheck").innerText=0
document.getElementById("legitCount").innerText=0

document.getElementById("riskLevel").innerText="LOW RISK"

document.getElementById("activityFeed").innerHTML=""

document.getElementById("amountRisk").innerText="-"
document.getElementById("locationRisk").innerText="-"
document.getElementById("categoryRisk").innerText="-"
document.getElementById("frequencyRisk").innerText="-"
document.getElementById("timeRisk").innerText="-"
document.getElementById("cardRisk").innerText="-"

document.getElementById("finalRisk").innerText="0%"

alert("Dashboard Cleared")

}