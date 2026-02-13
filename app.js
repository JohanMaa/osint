function save(){
  const min=document.getElementById("min").value
  const max=document.getElementById("max").value
  const messages=document.getElementById("messages").value.split("\n")
  const activity=document.getElementById("activity").value.split("\n")

  const data={
    delay_min:Number(min),
    delay_max:Number(max),
    branch:"main",
    messages:messages.filter(Boolean),
    activity_text:activity.filter(Boolean)
  }

  fetch("config.json",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify(data,null,2)
  })

  document.getElementById("status").innerText="Config updated"
}
