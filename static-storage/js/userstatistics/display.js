let currSelected ="#general_btn";
let statistics=""
let chartType=""
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
	google.charts.setOnLoadCallback(drawChart);
}

function drawChart() {
	let array;
	if(currSelected=="#general_btn"){
		if(chartType=="join"){
			array = statistics.lottery_join_time
		}
		else if(chartType=="join_event"){
			array = statistics.lottery_join_time
		}
		else if(chartType=="star"){
			array = statistics.lottery_join_time
		}
		else if(chartType=="star_event"){
			array = statistics.lottery_join_time
		}
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_join_time
	}
	else if(currSelected=="#buyout_btn"){

	}
	else if(currSelected=="#bid_btn"){

	}
	else{
		return;
	}
	array = statistics.lottery_join_time
	var data = new google.visualization.DataTable();
		data.addColumn('timeofday', 'Time');
		data.addColumn('number', 'Joins');
		data.addRows([
		[{v: [0, 1], f: '12:00 am'}, array[0]],
		[{v: [1, 2], f: '12:30 am'}, array[1]],
		[{v: [2, 3], f:'1:00 am'}, array[2]],
		[{v: [3, 4], f: '1:30 am'}, array[3]],
		[{v: [4, 5], f: '2:00 am'}, array[4]],
		[{v: [5, 6], f: '2:30 am'}, array[5]],
		[{v: [6, 7], f: '3:00 am'}, array[6]],
		[{v: [7, 8], f: '3:30 am'}, array[7]],
		[{v: [8, 9], f: '4:00 am'}, array[8]],
		[{v: [9, 10], f: '4:30 am'}, array[9]],
		[{v: [10, 0], f: '5:00 am'}, array[10]],
		[{v: [11, 0], f: '5:30 am'}, array[11]],
		[{v: [12, 0], f: '6:00 am'}, array[12]],
		[{v: [13, 0], f:'6:30 am'}, array[13]],
		[{v: [14, 0], f: '7:00 am'}, array[14]],
		[{v: [15, 0], f: '7:30 am'}, array[15]],
		[{v: [16, 0], f: '8:00 am'}, array[16]],
		[{v: [17, 0], f: '8:30 am'}, array[17]],
		[{v: [18, 0], f: '9:00 am'}, array[18]],
		[{v: [19, 0], f: '9:30 am'}, array[19]],
		[{v: [20, 0], f: '10:00 am'}, array[20]],
		[{v: [21, 0], f: '10:30 am'}, array[21]],
		[{v: [22, 0], f: '11:00 am'}, array[22]],
		[{v: [23, 0], f: '11:30 am'}, array[23]],
		[{v: [24, 0], f: '12:00 pm'}, array[24]],
		[{v: [25, 0], f: '12:30 pm'}, array[25]],
		[{v: [26, 0], f:'1:00 pm'}, array[26]],
		[{v: [27, 0], f: '1:30 pm'}, array[27]],
		[{v: [28, 0], f: '2:00 pm'}, array[28]],
		[{v: [29, 0], f: '2:30 pm'}, array[29]],
		[{v: [30, 0], f: '3:00 pm'}, array[30]],
		[{v: [31, 0], f: '3:30 pm'}, array[31]],
		[{v: [32, 0], f: '4:00 pm'}, array[32]],
		[{v: [33, 0], f: '4:30 pm'}, array[33]],
		[{v: [34, 0], f: '5:00 pm'}, array[34]],
		[{v: [35, 0], f: '5:30 pm'}, array[35]],
		[{v: [36, 0], f: '6:00 pm'}, array[36]],
		[{v: [37, 0], f:'6:30 pm'}, array[37]],
		[{v: [38, 0], f: '7:00 pm'}, array[38]],
		[{v: [39, 0], f: '7:30 pm'}, array[39]],
		[{v: [40, 0], f: '8:00 pm'}, array[40]],
		[{v: [41, 0], f: '8:30 pm'}, array[41]],
		[{v: [42, 0], f: '9:00 pm'}, array[42]],
		[{v: [43, 0], f: '9:30 pm'}, array[43]],
		[{v: [44, 0], f: '10:00 pm'}, array[44]],
		[{v: [45, 0], f: '10:30 pm'}, array[45]],
		[{v: [46, 0], f: '11:00 pm'}, array[46]],
		[{v: [47, 0], f: '11:30 pm'}, array[47]]
	]);

      var options = {
        title: 'User join times',
        width:800,
        height:400,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [47, 15]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById('graphic_display'));

      chart.draw(data, options);
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