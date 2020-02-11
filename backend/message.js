function msg(){
	var xhr = new XMLHttpRequest();
	var url = "apply";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var json = JSON.parse(xhr.responseText);
			console.log(json);
			//document.getElementById("counter").value = json.counter;
			alert('Response arrived!');
		}
	};
	var rows = document.getElementById("triggerTable").rows;
	var channels = [];
	for (var j = 1; j < rows.length; j++) {
		var row = rows[j];
		var channelCell = row.cells[1];
		console.log('inner html:' + channelCell.innerHTML);
		console.log('channel cell child:' + channelCell.children[0].innerHTML);
		console.log('option html:' + channelCell.children[0].options[0].innerHTML);
		var options = rows[j].cells[1].children[0].options;
		var selectedIndex = options.selectedIndex;
		console.log('selected index:' + options.selectedIndex);
		var channel = options[selectedIndex].text;
		channels.push(channel);
	};
	console.log('channels:' + channels.toString());
	var data = JSON.stringify({"apply": 1,
										  "channels":  channels.join(" ")});
	xhr.send(data);
}

document.getElementById("counter").value = 1;
var myVar = setInterval(myTimer, 1000);

function myTimer() {
	//document.getElementById("counter").stepUp(1);
	var xhr = new XMLHttpRequest();
	var url = "url";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        //console.log("json:" + json);
//        document.getElementById("counter").value = json.counter;
        var triggers_str = json.triggers.split(",");
		console.log('triggers_str:' + triggers_str);
        var triggers = []
        //var channels = ["ch1", "ch2", "ch3"]
		var channels = []
		if (json.hasOwnProperty('channels')) {
			channels = json.channels.split(", ")
		}
        for (var i = 0; i < 3; i++)   {
            trigger_str = triggers_str[i]
            //console.log("trigger_str:" + trigger_str)
            triggers.push(Number(trigger_str))
            //console.log("triggers:" + triggers)
        }
        for (var i = 1; i <= 3; i++) {
            var channelCell = document.getElementById("triggerTable").rows[i].cells[1];
            var channelList = channelCell.children[0];
            var selectedIndex = channelList.options.selectedIndex;
            var selectedValue = channelList.options[selectedIndex].text;
            //console.log("current channel value:" + selectedValue);
            var optionNodes = Array.prototype.slice.call(channelCell.childNodes[0].childNodes);
            var currentChannels = [];
            optionNodes.forEach(function(optionNode) {
                currentChannels.push(optionNode.text);
            });
            channels.sort();
            currentChannels.sort();
            //console.log("current channels:" + currentChannels + " sample channels:" + channels);
            if (channels.length != 0 && channels.toString() != currentChannels.toString()) {
                cellInnerHtml = "<select>";
				channels.forEach(function (channel) {
					var optionStr = "<option>" + channel+ "</option>";
					if (channel == selectedValue) {
						optionStr = "<option selected>" + channel+ "</option>";
					}
					cellInnerHtml += optionStr;
				});
				cellInnerHtml += "</select>";
				//console.log('cellInnerHtml:' + cellInnerHtml);
				channelCell.innerHTML = cellInnerHtml;
            }
        }
        for (var i = 0; i < 3; i++) {
            document.getElementById("triggerTable").rows[i+1].cells[2].innerHTML = triggers[i];
        }
        //console.log("channel:" + document.getElementById("triggerTable").rows[1].cells[1].innerHTML);
    }
  };
  triggers_str = document.getElementById("triggerTable").rows[1].cells[2].innerHTML;
  for (var i = 2; i <= 3; i++) {
    triggers_str += ", " + document.getElementById("triggerTable").rows[i].cells[2].innerHTML;
  }
  var data = JSON.stringify({"triggers": triggers_str, "counter": document.getElementById("counter").value});
  //console.log("data to send" + data)
  xhr.send(data);
}

function pauseCounter() {
    clearInterval(myVar);
}

function resumeCounter() {
    myVar = setInterval(myTimer, 1000);
}