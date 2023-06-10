let navbarLinks      = ''
let toggleButtonMenu = ''
let addDevice        = ''
let addDeviceStat    = false

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); 
    template.innerHTML = html;
    return template.content.firstChild;
}


document.addEventListener("DOMContentLoaded",()=>{

addDevice        = document.getElementById("addDevice");
toggleButtonMenu = document.getElementsByClassName("toggle-button-menu")[0];
navbarLinks      = document.getElementsByClassName("navbar-links")[0]
toggleButtonMenu.addEventListener("click",()=>{ navbarLinks.classList.toggle("active")});

if((window.location.href).includes("deviceList"))
setInterval(()=>{
    
    
    fetch(`/deviceListUpdated/${document.getElementsByClassName("heading")[0].getAttribute("data-attr")}`,{
        method: 'GET',
    }).then((response)=>{ if(response.ok) return response.json(); else return null; }).then((response)=>{

                response.forEach((device)=>{

                     if (device["usage"] === "bool"){
                             if(device["modeOperation"] === "INPUT")
                                document.querySelectorAll(`[data-comm="${device["pinNumber"]}"]`)[0].innerHTML=`${device["state"] === true ? 1 : 0}`;
                             else{
                               titems= document.querySelectorAll(`[data-comm="${device["pinNumber"]}"]`)
                                    if(titems[0].tagName === "TD"){
                                        titems[0].innerHTML = `${device["state"] === true ? 1 : 0}`;
                                        titems[1].checked = device["state"];
                                    }
                                    else{
                                         titems[0].checked = device["state"];
                                         titems[1].innerHTML = `${device["state"] === true ? 1 : 0}`;
                                    }
                             }
                     }
                     else
                      document.querySelectorAll(`[data-comm="${device["pinNumber"]}"]`)[0].innerHTML=`${ parseFloat(device["floatValue"]) } ${device["unit"]}`;
                             

                     

                })
    });
     
 },4000);

addDevice.addEventListener("click",(e)=>{
       
       addDeviceStat = !addDeviceStat
       console.log(e.target)
       if(addDeviceStat){   e.target.style.display = "none"
     
          formDiv = document.getElementById("DeviceRegForm");
          formDiv.style.display = "block";
    
       }
       else{this.style.display = "block"}
});

 document.querySelectorAll("[data-delete]").forEach((elm)=>{
        
       elm.addEventListener("click",(e)=>{
        
           button = e.target.tagName === 'I' ? e.target.parentNode : e.target
           console.log(button)
        fetch(`/delete/${document.getElementsByClassName("heading")[0].getAttribute("data-attr")}`,{
            method: 'DELETE',
            body:JSON.stringify({
                 PIN:button.getAttribute("data-pin"),
            })
        }).then((resp)=>{if(resp.ok){
             
             document.querySelectorAll("[data-target").forEach((targ)=>{ 
                if(targ.getAttribute("data-target") == button.getAttribute("data-pin")){
                    targ.remove();
                    
                }
              })
        }})
  
       })

 });


document.querySelectorAll("[data-label=Toggle]").forEach((effector)=>{

         if(effector.getAttribute("type") === "number"){

             effector.addEventListener("keypress",(e)=>{
                         
                   if(e.key === "Enter"){
                      

                    elm = document.getElementById(this.target.getAttribute("data-id"));
                    fetch(`/deviceList/${document.getElementsByClassName("heading")[0].getAttribute("data-attr")}`,{
                     method: 'PUT',
                     body:JSON.stringify({
                          PIN:`${this.target.getAttribute("data-pin")}`,
                          VAL: this.target.value,
                          USAGE:"float",
                     })
                    }).then((response)=>{ if(response.ok) {elm.innerHTML = this.target.value + ' ' + elm.getAttribute("data-unit") ;}else{}});
                   }   
                 
             });
              
         }




});

document.querySelectorAll(".activeRow").forEach((row)=>{ 

        if(row.className == "activeRow"){
               row.addEventListener("click",(e)=>{
                     target = e.target;
                     while(target.getAttribute("data-label") !== "Toggle" && target.className !== "activeRow")
                        target = target.parentNode;

                     if(target.getAttribute("data-label") === "Toggle" && target.getAttribute("type") === "checkbox"){
                            elm =  document.getElementById(target.getAttribute("data-id"))
                            if(target.checked)
                                  elm.innerHTML=1;
                            else
                                 elm.innerHTML=0;  
                          
                            fetch(`/deviceList/${document.getElementsByClassName("heading")[0].getAttribute("data-attr")}`,{
                                method: 'PUT',
                                body:JSON.stringify({
                                     PIN:`${target.getAttribute("data-pin")}`,
                                     VAL: elm.innerHTML == 0 ? false : true,
                                     USAGE:"bool",
                                })
                            }) //remind
                     
                     }  
               })
        }
        else{

        }

 })


    
    
    
   

});
