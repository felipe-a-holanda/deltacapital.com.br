/*
 *  Creates a progressbar.
 *  @param id the id of the div we want to transform in a progressbar
 *  @param duration the duration of the timer example: '10s'
 *  @param callback, optional function which is called when the progressbar reaches 0.
 */
function createProgressbar(id, duration, callback) {
  // We select the div that we want to turn into a progressbar
  var progressbar = document.getElementById(id);
  progressbar.className = 'progressbar';

  // We create the div that changes width to show progress
  var progressbarinner = document.createElement('div');
  progressbarinner.className = 'innerp';

  // Now we set the animation parameters
  progressbarinner.style.animationDuration = duration;

  // Eventually couple a callback
  if (typeof(callback) === 'function') {
    progressbarinner.addEventListener('animationend', callback);
  }

  // Append the progressbar to the main progressbardiv
  progressbar.appendChild(progressbarinner);

  // When everything is set up we start the animation
  progressbarinner.style.animationPlayState = 'running';
}

