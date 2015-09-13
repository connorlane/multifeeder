 document.addEventListener("DOMContentLoaded", function(event) {
          var feederGauge = {
			titleFontColor: "#1A1A1A",
			titleMinFontSize: "15px",			
			label: "cm^3/s", 
			value: 0,
			min: 0,
			max: 300,
			donut: false,
			decimals: 2,
			gaugeWidthScale: 0.5,
			levelColorsGradient: false,
			customSectors: [{
			  color : "#CC0000",
			  lo : 0,
			  hi : 5
			},{
			  color : "#00CC00",
			  lo : 5,
			  hi : 200
			}, {
			  color : "#CC0000",
			  lo : 200,
			  hi : 300
			}],
			counter: false,
			startAnimationTime: 1,
			startAnimationType: "linear",
			refreshAnimationTime: 1,
			refreshAnimationType: "linear"  
	  };

	var heaterGauge = {
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
			counter: false,
			startAnimationTime: 1,
			startAnimationType: "linear",
			refreshAnimationTime: 1,
			refreshAnimationType: "linear"  
	  };

	var feeder1_gauge = new JustGage($.extend({}, feederGauge, {id: "feeder1_value", title: "Steel"}));
	var feeder2_gauge = new JustGage($.extend({}, feederGauge, {id: "feeder2_value", title: "Ti-64"}));
	var feeder3_gauge = new JustGage($.extend({}, feederGauge, {id: "feeder3_value", title: "Stainless"}));

	var heater1_gauge = new JustGage($.extend({}, heaterGauge, {id: "heater1_value", title: "Steel"}));
	var heater2_gauge = new JustGage($.extend({}, heaterGauge, {id: "heater2_value", title: "Ti-64"}));
	var heater3_gauge = new JustGage($.extend({}, heaterGauge, {id: "heater3_value", title: "Stainless"}));

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
					hideCommError();
				}, 
			dataType: "json", 
			timeout: 4000,
			error: showCommError
		});
	}, interval);

	$('.feeder-keyboard')
        .keyboard({
		maxLength: "4",
		layout: 'custom',
		customLayout: {
		    'default': ['7 8 9', '4 5 6', '1 2 3', '0 . {b}', '{accept} {cancel}']
		},
		restrictInput: true,
		accepted:
		function (event, keyboard, el) {
			checkAndPost(el, {lessThan: 300});
		}
	});

	$('.heater-keyboard')
        .keyboard({
		maxLength: "4",
		layout: 'custom',
		customLayout: {
		    'default': ['7 8 9', '4 5 6', '1 2 3', '0 . {b}', '{accept} {cancel}']
		},
		restrictInput: true,
		accepted:
		function (event, keyboard, el) {
			checkAndPost(el, {lessThan: 150});
		}
	});

	setInterval(refreshSettings, interval);
});

function checkAndPost(el, specs)
{
	var dataToSend = {}
	if (validate.single(el.value, {numericality: specs})) {
		el.value = "0.00";
		showInvalidSetpoint();
	} else {
		hideInvalidSetpoint();
		el.value = parseFloat(el.value).toFixed(1);
		dataToSend[el.id] =  el.value;
		$.ajax({
			url: "update",
			type: "POST",
			dataType: "json",
			data: dataToSend,
			timeout: 4000,
			error: function() {
				el.value = "0.00";
				showCommError();	
			},
			success: hideCommError
		});
	}
}

function showInvalidSetpoint() {
	$("#invalidFeederSetpoint").show();
}

function hideInvalidSetpoint() {
	$("#invalidFeederSetpoint").hide();
}

function showCommError() {
	$("#communicationError").show();
}

function hideCommError() {
	$("#communicationError").hide();
}

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

				$("#feeder1_setpoint").val(data.feeder1_setpoint);
				$("#feeder2_setpoint").val(data.feeder2_setpoint);
				$("#feeder3_setpoint").val(data.feeder3_setpoint);
				$("#heater1_setpoint").val(data.heater1_setpoint);
				$("#heater2_setpoint").val(data.heater2_setpoint);
				$("#heater3_setpoint").val(data.heater3_setpoint);
			},
		dataType: "json",
		timeout: 4000
	});
}

$(document).ready(function(){
	$(".powerbuttons").click(function(){
		var newButtonCommand = (this.value == "true") ? "false" : "true";

		var dataToSend = {}
		dataToSend[this.id] = newButtonCommand;

		$.ajax({
			url: "update",
			type: "POST",
			dataType: "json",
			data: dataToSend,
			timeout: 4000,
			context: this,
			success: function(data) {
					setButton($(this), data[this.id]);
					hideCommError();
				},
			error: showCommError
		});
	});
});

