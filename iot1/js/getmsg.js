// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("alert");
  client.subscribe("power");
  client.subscribe("pressure");
  client.subscribe("temp_desktop");
  client.subscribe("humi_desktop");
  client.subscribe("temp_floor");
  client.subscribe("humi_floor");
  client.subscribe("temp_window");
  client.subscribe("humi_window");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString+" DestName="+message.destinationName);
  if (message.payloadString == "red") {
	  console.log("red");
          draw_red()
  }
  if (message.payloadString == "green") {
	  console.log("green");
          draw_green()
  }

  if (message.destinationName == "pressure") {
      console.log(message.payloadString);
      $("#gauge1").gauge(Number(message.payloadString), {min: 0, max: 1100, color: "#8BC34A", unit: " HPa", font: "80px verdana"});
  }

  if (message.destinationName == "power") {
      console.log(message.payloadString);
      draw_text(message.payloadString);
      $("#gauge2").gauge(Number(message.payloadString), {min: 0, max: 700, color: "#C38B4A", unit: " WHr", font: "80px verdana"});
  }

  if (message.destinationName == "temp_desktop") {
      console.log(message.payloadString);
      $("#gauge3").gauge(Number(message.payloadString), {min: 0, max: 45, color: "#8BC34A", unit: " C", font: "80px verdana" ,type: "halfcircle"});
  }

  if (message.destinationName == "temp_window") {
      console.log(message.payloadString);
      $("#gauge4").gauge(Number(message.payloadString), {min: 0, max: 45, color: "#8BC34A", unit: " C", font: "80px verdana" ,type: "halfcircle"});
  }

  if (message.destinationName == "temp_floor") {
      console.log(message.payloadString);
      $("#gauge5").gauge(Number(message.payloadString), {min: 0, max: 45, color: "#8BC34A", unit: " C", font: "80px verdana" ,type: "halfcircle"});
  }


  if (message.destinationName == "humi_desktop") {
      console.log(message.payloadString);
      $("#gauge6").gauge(Number(message.payloadString), {min: 0, max: 100, color: "#8080AA", unit: " %", font: "80px verdana" ,type: "halfcircle"});
  }

  if (message.destinationName == "humi_window") {
      console.log(message.payloadString);
      $("#gauge7").gauge(Number(message.payloadString), {min: 0, max: 100, color: "#8080AA", unit: " %", font: "80px verdana" ,type: "halfcircle"});
  }

  if (message.destinationName == "humi_floor") {
      console.log(message.payloadString);
      $("#gauge8").gauge(Number(message.payloadString), {min: 0, max: 100, color: "#8080AA", unit: " %", font: "80px verdana" ,type: "halfcircle"});
  }

}

