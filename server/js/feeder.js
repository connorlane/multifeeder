 document.addEventListener("DOMContentLoaded", function(event) {
	  var feeder1_gauge = new JustGage({
			id: "feeder1_value",
			title: "Steel",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "RPM", value: 25,
			min: 0,
			max: 30,
			donut: false,
			decimals: 2,
			gaugeWidthScale: 0.5,
			levelColorsGradient: false,
			customSectors: [{
			  color : "#CC0000",
			  lo : 0,
			  hi : 0.5
			},{
			  color : "#00CC00",
			  lo : 0.5,
			  hi : 20
			}, {
			  color : "#CC0000",
			  lo : 20,
			  hi : 30
			}],
			counter: true
	  });

	  var feeder2_gauge = new JustGage({
			id: "feeder2_value",
			title: "Ti-64",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "RPM",
			value: 25,
			min: 0,
			max: 30,
			donut: false,
			decimals: 2,
			gaugeWidthScale: 0.5,
			levelColorsGradient: false,
			customSectors: [{
			  color : "#CC0000",
			  lo : 0,
			  hi : 0.5
			},{
			  color : "#00CC00",
			  lo : 0.5,
			  hi : 20
			}, {
			  color : "#CC0000",
			  lo : 20,
			  hi : 30
			}],
			counter: true
	  });

	  var feeder3_gauge = new JustGage({
			id: "feeder3_value",
			title: "Stainless",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "RPM",
			value: 25,
			min: 0,
			max: 30,
			donut: false,
			decimals: 2,
			gaugeWidthScale: 0.5,
			levelColorsGradient: false,
			customSectors: [{
			  color : "#CC0000",
			  lo : 0,
			  hi : 0.5
			},{
			  color : "#00CC00",
			  lo : 0.5,
			  hi : 20
			}, {
			  color : "#CC0000",
			  lo : 20,
			  hi : 30
			}],
			counter: true
	  });

	  var heater1_gauge = new JustGage({
			id: "heater1_value",
			title: "Steel",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "Degrees Celcius",
			value: 25,
			min: 0,
			max: 200,
			donut: false,
			gaugeWidthScale: 0.5,
			customSectors: [{
			  color : "#00CC00",
			  lo : 0,
			  hi : 50, 
			},{
			  color : "#CCCC00",
			  lo : 50,
			  hi : 150
			}, {
			  color : "#CC0000",
			  lo : 150,
			  hi : 200
			}],
			levelColorsGradient: false,
			counter: true
	  });

	  var heater2_gauge = new JustGage({
			id: "heater2_value",
			title: "Ti-64",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "Degrees Celcius",
			value: 25,
			min: 0,
			max: 200,
			donut: false,
			gaugeWidthScale: 0.5,
			customSectors: [{
			  color : "#00CC00",
			  lo : 0,
			  hi : 50
			},{
			  color : "#CCCC00",
			  lo : 50,
			  hi : 150
			}, {
			  color : "#CC0000",
			  lo : 150,
			  hi : 200
			}],
		levelColorsGradient: false,
			counter: true
	  });

	  var heater3_gauge = new JustGage({
			id: "heater3_value",
			title: "Stainless",
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "Degrees Celcius",
			value: 25,
			min: 0,
			max: 200,
			donut: false,
			gaugeWidthScale: 0.5,
			customSectors: [{
			  color : "#00CC00",
			  lo : 0,
			  hi : 50
			},{
			  color : "#CCCC00",
			  lo : 50,
			  hi : 150
			}, {
			  color : "#CC0000",
			  lo : 150,
			  hi : 200
			}],
	levelColorsGradient: false,
			counter: true
	  });

	var interval = 1000
	setInterval(function poll(){
		$.ajax({ 
			url: "data", 
			success: 
				function(data){
					heater1_gauge.refresh(data.heater1);
					heater2_gauge.refresh(data.heater2);
					heater3_gauge.refresh(data.heater3);
					feeder1_gauge.refresh(data.wheel1);
					feeder2_gauge.refresh(data.wheel2);
					feeder3_gauge.refresh(data.wheel3);
				}, 
			dataType: "json", 
			timeout: interval 
		});
	}, interval);

	$('.temp-keyboard')
        .keyboard({
			maxLength: "4",
        layout: 'custom',
        customLayout: {
            'default': ['7 8 9', '4 5 6', '1 2 3', '0 . {b}', '{accept} {cancel}']
        },
		  restrictInput: true
    });

	setInterval(refreshSettings, interval);

	});

function setButton(button, value) {
	if (value == "true") {
		button.removeClass( "btn-danger" );
		button.addClass( "btn-success" );
		button.val("true");
		button.html("ON");
	} else if (value == "false") {
		button.removeClass( "btn-success" );
		button.addClass( "btn-danger" );
		button.val("false");
		button.html("OFF");
	}
}

function refreshSettings() {
	$.ajax({ 
		url: "update", 
		success: function (data) {
				setButton($("#feeder1_on"), data.feeder1_on);
				setButton($("#feeder2_on"), data.feeder2_on);
				setButton($("#feeder3_on"), data.feeder3_on);

				setButton($("#heater1_on"), data.heater1_on);
				setButton($("#heater2_on"), data.heater2_on);
				setButton($("#heater3_on"), data.heater3_on);

				$("#feeder1_setpoint").innerHTML = data.feeder1_setpoint;
				$("#feeder2_setpoint").innerHTML = data.feeder2_setpoint;
				$("#feeder3_setpoint").innerHTML = data.feeder3_setpoint;

				$("#heater1_setpoint").innerHTML = data.heater1_setpoint;
				$("#heater2_setpoint").innerHTML = data.heater2_setpoint;
				$("#heater3_setpoint").innerHTML = data.heater3_setpoint;
			},
		dataType: "json",
		timeout: 5000
	});
}

$(document).ready(function(){
	$(".powerbuttons").click(function(){
		var newButtonCommand = (this.value == "true") ? "false" : "true";

		var dataToSend = {}
		dataToSend[this.id] =  newButtonCommand;

		$.ajax({
			url: "update",
			type: "POST",
			dataType: "json",
			data: dataToSend,
			timeout: 4000,
			context: this,
			success: function(data) {
					setButton($(this), data[this.id]);
				}
		});
	});
});

