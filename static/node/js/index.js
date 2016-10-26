function Generate(context) {

document.getElementById('demo').innerHTML = Date()
var $myCanvas = $('#MainCanvas');
$myCanvas.drawArc({
  fillStyle: 'steelblue',
  strokeStyle: 'steelblue',
  strokeStyle: 'blue',
  strokeWidth: 4,
  x: context.fromX, y: context.fromY,
  radius: 20,
  // start and end angles in degrees
//  start: 0, end: 360
});
}
// rectangle shape

