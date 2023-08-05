// Define the original 2D path coordinates
const originalPathData = 'M100,100 L200,100 L200,200 L100,200 Z';

// Create an SVG path element
const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

// Set the d attribute of the path to the original path data
path.setAttribute('d', originalPathData);

// Get the total length of the path
const pathLength = path.getTotalLength();

// Define the perspective factor (adjust as needed)
const perspective = 100;

// Create a new path string for the transformed path
let transformedPathData = '';

// Iterate through the path and apply perspective transformation
for (let i = 0; i < pathLength; i++) {
  // Get the current point on the path
  const point = path.getPointAtLength(i);

  // Apply perspective transformation
  const transformedX = point.x + (perspective / (perspective + point.y)) * (point.x - point.x);
  const transformedY = point.y;

  // Append transformed point to the new path string
  transformedPathData += (i === 0 ? 'M' : 'L') + transformedX + ',' + transformedY;
}

// Close the transformed path
transformedPathData += ' Z';

console.log(transformedPathData);