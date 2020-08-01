function progress(timeleft, timetotal, $element) {
    var progressBarWidth = (timetotal-timeleft)/timetotal * $element.width();
    $element.find('div').animate({ width: progressBarWidth }, 50).html(Math.floor(timeleft/10));
    if(timeleft > 0) {
        setTimeout(function() {
            progress(timeleft - 1, timetotal, $element);
        }, 100);
    }
};

progress(300, 590, $('#progressBar'));