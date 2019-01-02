// this function checks to see if lottery had been selected as the event type 
// if it has, it makes the max_entrants piece visible. otherwise, its hidden.
// it only gets called on the create event page.
function check_event_type(type) {
  // if the event is a lottery
  if(type == 1) {
    // the id tells us where our change is supposed to occur
    // this unhides the max entrants field
    toggleField("#id_max_entrants", false)
    // this hides the minimum bid field
    toggleField("#id_minimum_bid", true)
    // this unhides the number of winners field
    toggleField("#id_num_possible_winners", false)
    // this sets the text for the num winners field
    $("label[for=id_num_possible_winners]").text('Number of possible winners*');
    // this sets the text for cost
    $("label[for=id_cost]").text('Cost ($)*');
  // if the event is an auction
  } else if (type == 2) {
    // this hides the max entrants field
    toggleField("#id_max_entrants", true)
    // this unhides the number of winners field
    toggleField("#id_num_possible_winners", false)
    // this sets the text for the num winners field
    $("label[for=id_num_possible_winners]").text('Number of possible winners*');
     // this sets the text for cost
    $("label[for=id_cost]").text('Starting Bid ($)*');
  // if the event is a buy
  } else if (type == 3) {
    // this hides the max entrants field
    toggleField("#id_max_entrants", true)
    // this hides the minimum bid field
    toggleField("#id_minimum_bid", true)
    // this unhides the number of winners field
    toggleField("#id_num_possible_winners", false)
    // this sets the text for the num winners field
    $("label[for=id_num_possible_winners]").text('Number of purchases available*');
     // this sets the text for cost
    $("label[for=id_cost]").text('Cost ($)*');
  } else {
    // this hides the max entrants field
    toggleField("#id_max_entrants", true)
    // this hides the number of winners field
    toggleField("#id_num_possible_winners", true)
  }
}

function toggleField(field, isShown){
    $(field).prop('hidden', isShown);
    $('label[for=' + field.replace('#', '') + ']').prop('hidden', isShown);
}