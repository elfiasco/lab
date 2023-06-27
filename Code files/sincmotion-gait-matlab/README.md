# Matlab Implementation of the Gait&Balance Gait Analysis Algorithm

This is a minified version of the algorithm. The results may differ slightly from the Gait&Balance app as the app's wavelet-differentiation library is not included here. The library requires platform specific compilation for use with MATLAB. Instead, a third party wavelet-differentiation function is included which uses MATLAB's own implementation of the wavelet-transform.

## Quick Start

Add the sincmotion-gait folder to MATLAB workspace and run the `ComfortableGaitOutcomes.m` script. Select the `walk_hf.csv` file from the `Example Data` folder.

## Data Format

The Gait&Balance app (iPhone) stores data in the following format:

- Timestamp: YYYY-MM-DD HH:MM:SS.sss
- AccelX: Acceleration (g) along the X axis. When the phone falls towards the earth, acceleration is positive.
- AccelY: Acceleration (g) along the Y axis.
- AccelZ: Acceleration (g) along the Z axis.
- GyroX: Counter-clockwise rotation (rad) about the X axis.
- GyroY: Counter-clockwise rotation (rad) about the Y axis.
- GyroZ: Counter-clockwise rotation (rad) about the Z axis.
- [QuatW,QuatX,QuatY,QuatZ]: iPhone pose quaternions with respect to a fixed reference frame. The fixed reference frame is based on the pose of the iPhone at the start of the recording. The fixed pose is calculated as if the iPhone is laying on a flat table.

iPhone sensor system is explained here: [https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data/understanding_reference_frames_and_device_attitude](https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data/understanding_reference_frames_and_device_attitude).

iPhone is worn at the lower back in the vertical orientation which means that for the raw acceleration data, X-axis is nearly aligned with the medio-lateral axis, Y-axis with the vertical axis and Z-axis with the negative anterior-posterior axis. After reference correction using the pose quaternions, the axes are aligned as follows: [X:ML, Y:AP, Z:Vertical].

## Functions

- `ComfortableGaitOutcomes.m`: Script to load a file and run the analysis algorithm.
- `cgCreateSegments.m`: Function to break-up the data into four segments corresponding to four bouts of the comfortable walk tests in the Gait&Balance app.
- `cgOutcomes.m`: Function to compute gait outcomes from steps and step times estimated from four bouts.
- `cgsOutcomes.m`: Function to compute step lengths and step times from a single a bout.
- `cgsPreprocessedData.m`: Function to pre-process the data.
- `footEvents.m`: Function to detect foot events.
- `gsi.m`: Function to compute gait symmetry index.
- `vertMovements.m`: Function to compute step lengths using the double pendulum gait model.

## Third Party Libraries

- `acf.m`: Calvin Price (2023). Autocorrelation Function (ACF) (<https://www.mathworks.com/matlabcentral/fileexchange/30540-autocorrelation-function-acf>), MATLAB Central File Exchange. Retrieved March 25, 2023.

- `derivate_cwt.m`: Jianwen Luo (2023). Numerical differentiation based on wavelet transforms (<https://www.mathworks.com/matlabcentral/fileexchange/13948-numerical-differentiation-based-on-wavelet-transforms>), MATLAB Central File Exchange. Retrieved March 25, 2023.
