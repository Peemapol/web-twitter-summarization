$(document).ready(function () {
    $('#submit-main-form').click(function() {
        var checked = $("input[type=checkbox]:checked").length;
        var fromDate = new Date($("#tweet_date_early").val());
        var toDate = new Date($("#tweet_date_later").val());
        console.log("from date" + fromDate);
        console.log("to date" + toDate);
        if ((isNaN(fromDate) && !isNaN(toDate)) || (!isNaN(fromDate) && isNaN(toDate))) {
            alert('Please provide values for both "from" and "to" dates or Input the same date to scrape data only that day.');
            return false;
        }
        
        // Check if both dates are valid and not in the future
        if (!isNaN(fromDate) && !isNaN(toDate)) {
            const currentDate = new Date();
        
            if (fromDate > toDate || fromDate > currentDate || toDate > currentDate) {
              alert('Invalid date range. "From" date must be before "To" date, and both dates cannot be in the future.');
              return false;
            }
        }
        if(!checked) {
            alert("You must check at least one checkbox.");
            return false;
        }
        if(checked == 2){
            alert("You must check only one checkbox.");
            return false;
        }
    });
});