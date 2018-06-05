let currSelected ="#general_btn";
let statistics=""
let chartType=""
let graphWidth=600;
let graphHeight=300;
$(document).ready(function(){
	firstRender();
	addBtnFunctions();

});
/********************** UTILITY FUNCTIONS)***********************/
function addBtnFunctions(){
	$('#general_btn').click(function(e){
  		e.preventDefault();
  		fillSelected(this, "#general_btn");
  		renderGeneralStatistics();

  	})

	$('#lottery_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#lottery_btn");
		renderLotteryStatistics();
	})

	$('#bid_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#bid_btn");
		console.log("here")
		renderBidStatistics();
	})

	$('#buyout_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#buyout_btn");
		renderBuyoutStatistics();
	})
}

//Grabs statistics via ajax Get request
//Waits for success, then renders general statistics page
function firstRender(){
	$.ajax({
		url: '/api/statistics', 
		method: 'GET', 
		success: function(data){
			statistics = data[0]
			renderGeneralStatistics();
		}, 
		error: function(data){
			console.log('error');
	}
  })
}

function fillSelected(button, name){
	$(currSelected).removeClass('btn btn-secondary');
	$(currSelected).addClass('btn btn-outline-secondary');
	$(button).removeClass('btn btn-outline-secondary');
	$(button).addClass('btn btn-secondary');
	currSelected = name;
}

/************************GENERAL STATISTICS FUNCTIONS**************/
//Main rendering of general stats
function renderGeneralStatistics(){
	renderGeneralMaxEarnings();
	renderGeneralTotalEarnings();
	renderGeneralAverageEarnings();
	renderGeneralNumEvents();


	chartType="join"
	renderChart();
	chartType="join_event"
	renderChart();
	chartType="star"
	renderChart();
	chartType="star_event"
	renderChart();
}

function renderChart(){
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawJoinChart);
	google.charts.setOnLoadCallback(drawJoinEventChart);
	google.charts.setOnLoadCallback(drawStarChart);
	google.charts.setOnLoadCallback(drawStarEventChart);
}

//renders average profit data
function renderGeneralAverageEarnings(){
	let general_average_earnings_display = parseFloat(statistics.general_average_earnings).toFixed(2);
	$('#stat_description3').text("Average event earnings: ");
	$('#average_earnings_val').text("$"+general_average_earnings_display);
}

//renders max profit data
function renderGeneralTotalEarnings(){
	let total_earnings_display = parseFloat(statistics.total_earnings).toFixed(2);
	$('#stat_description2').text("Total event earnings: ");
	$('#total_earnings_val').text("$"+total_earnings_display);
}
//renders total_profit data
function renderGeneralMaxEarnings(){
	let max_profit_display = parseFloat(statistics.max_profit).toFixed(2);
	$('#stat_description1').text("Max event earnings: ");
	$('#max_earnings_val').text("$"+max_profit_display);
}
function renderGeneralNumEvents(){
	$('#stat_description4').text("Number of general events: ");
	$('#num_events_val').text(statistics.total_num_events);
}

/************************LOTTERY STATISTICS FUNCTIONS**************/
function renderLotteryStatistics(){
	renderLotteryTotalEarnings();
	renderLotteryAverageEarnings();
	renderLotteryTotalParticipants();
	renderLotteryNumEvents();

	renderChart();
}

function renderLotteryNumEvents(){
	$('#stat_description4').text("Number of lottery events: ");
	$('#num_events_val').text(statistics.lottery_num_events);
}
//renders average profit data
function renderLotteryAverageEarnings(){
	let lottery_average_earnings_display = parseFloat(statistics.lottery_average_earnings).toFixed(2);
	$('#stat_description3').text("Average lottery earnings: ");
	$('#average_earnings_val').text("$"+lottery_average_earnings_display);
}

//renders max profit data
function renderLotteryTotalEarnings(){
	let lottery_total_earnings_display = parseFloat(statistics.lottery_total_earnings).toFixed(2);
	$('#stat_description2').text("Total lottery earnings: ");
	$('#total_earnings_val').text("$"+lottery_total_earnings_display);
}
//renders total_profit data
function renderLotteryTotalParticipants(){
	 $('#stat_description1').text("Total lottery participants: ");
	 $('#max_earnings_val').text(statistics.lottery_total_participants);
}
/************************BID STATISTICS FUNCTIONS**************/
function renderBidStatistics(){
	renderBidTotalEarnings();
	renderBidAverageEarnings();
	renderBidMaxBid();
	renderBidNumEvents();

	renderChart()
}
function renderBidNumEvents(){
	$('#stat_description4').text("Number of bid events: ");
	$('#num_events_val').text(statistics.bid_num_events);
}
//renders average profit data
function renderBidAverageEarnings(){
	let bid_average_earnings_display = parseFloat(statistics.bid_average_earnings).toFixed(2);
	$('#stat_description3').text("Average bid earnings: ");
	$('#average_earnings_val').text("$"+bid_average_earnings_display);
}
//renders max profit data
function renderBidTotalEarnings(){
	let bid_total_earnings_display = parseFloat(statistics.bid_total_earnings).toFixed(2);
	$('#stat_description2').text("Total bid earnings: ");
	$('#total_earnings_val').text("$"+bid_total_earnings_display);
}
//renders total_profit data
function renderBidMaxBid(){
	let bid_max_bid_display = parseFloat(statistics.max_bid_event).toFixed(2);
	 $('#stat_description1').text("Maximum amount bid: ");
	 $('#max_earnings_val').text(bid_max_bid_display);
}
/************************BUYOUT STATISTICS FUNCTIONS**************/
function renderBuyoutStatistics(){
	renderBuyoutTotalEarnings();
	renderBuyoutAverageEarnings();
	renderBuyoutRemoveExtra();
	renderBuyoutNumEvents();

	renderChart();
}
//renders average profit data
function renderBuyoutAverageEarnings(){
	let buyout_average_earnings_display = parseFloat(statistics.buyout_average_earnings).toFixed(2);
	$('#stat_description3').text("Average buyout earnings: ");
	$('#average_earnings_val').text("$"+buyout_average_earnings_display);
}
//renders max profit data
function renderBuyoutTotalEarnings(){
	let buyout_total_earnings_display = parseFloat(statistics.buyout_total_earnings).toFixed(2);
	$('#stat_description2').text("Total buyout earnings: ");
	$('#total_earnings_val').text("$"+buyout_total_earnings_display);
}
//renders total_profit data
function renderBuyoutRemoveExtra(){
	let bid_max_bid_display = parseFloat(statistics.max_bid_event).toFixed(2);
	 $('#stat_description1').text("");
	 $('#max_earnings_val').text("");
}
function renderBuyoutNumEvents(){
	$('#stat_description4').text("Number of buy events: ");
	$('#num_events_val').text(statistics.buyout_num_events);
}

///////////////////////////CHART RENDERING FUNCTIONS////////////////////////
function drawJoinChart() {
	let array;
	let graphTitle = "Join Time";
	let graphDiv = "join_time";
	let graphAction = "Joins";

	if(currSelected=="#general_btn"){
		array = statistics.general_join_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_join_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_join_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_join_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
		data.addColumn('timeofday', 'Time');
		data.addColumn('number', graphAction);
		let i;
		let t = "am"
		let time = 0;
		for(i = 0; i<24;i++){
			console.log(array[i*2]+" "+array[i*2+1]);
			data.addRow([{v: [i*2/2, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
			if(time==12){
				time=0;
				t="pm"
			}
			time++;
		}

      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

      chart.draw(data, options);
}
function drawJoinEventChart() {
	let array;
	let graphTitle = "Join Event Time";
	let graphDiv = "join_event_time";
	let graphAction = "Joins";

	if(currSelected=="#general_btn"){
		array = statistics.general_join_event_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_join_event_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_join_event_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_join_event_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
		data.addColumn('timeofday', 'Time');
		data.addColumn('number', graphAction);
		let i;
		let t = "am"
		let time = 0;
		for(i = 0; i<24;i++){
			console.log(array[i*2]+" "+array[i*2+1]);
			data.addRow([{v: [i*2/2, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
			if(time==12){
				time=0;
				t="pm"
			}
			time++;
		}

      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

      chart.draw(data, options);
}
function drawStarChart() {
	let array;
	let graphTitle = "Star Time";
	let graphDiv = "star_time";
	let graphAction = "Stars";

	if(currSelected=="#general_btn"){
		array = statistics.general_star_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_star_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_star_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_star_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
		data.addColumn('timeofday', 'Time');
		data.addColumn('number', graphAction);
		let i;
		let t = "am"
		let time = 0;
		for(i = 0; i<24;i++){
			console.log(array[i*2]+" "+array[i*2+1]);
			data.addRow([{v: [i*2/2, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
			if(time==12){
				time=0;
				t="pm"
			}
			time++;
		}

      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

      chart.draw(data, options);
}
function drawStarEventChart() {
	let array;
	let graphTitle = "Star Event Time";
	let graphDiv = "star_event_time";
	let graphAction = "Stars";

	if(currSelected=="#general_btn"){
		array = statistics.general_star_event_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_star_event_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_star_event_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_star_event_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
		data.addColumn('timeofday', 'Time');
		data.addColumn('number', graphAction);
		let i;
		let t = "am"
		let time = 0;
		for(i = 0; i<24;i++){
			console.log(array[i*2]+" "+array[i*2+1]);
			data.addRow([{v: [i*2/2, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
			if(time==12){
				time=0;
				t="pm"
			}
			time++;
		}

      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

      chart.draw(data, options);
}