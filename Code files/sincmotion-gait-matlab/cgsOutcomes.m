function [gSymIndex, stepLengths, leftStepLengths, rightStepLengths,...
    stepTimes, leftStepTimes, rightStepTimes] = cgsOutcomes(accelData, rotData, gyroData, fs,...
    personHeight, isPostQuat, isAndroid, debugFlag)

%% Preprocess data
[accelDataRotated, gyroData] = cgsPreprocessedData(accelData, rotData, gyroData, fs,...
    isPostQuat, isAndroid);

%% Compute outputs

% Symmetry outcomes
[gSymIndex, tStrideSample]  = gsi(accelDataRotated, fs, debugFlag);

% Get unfiltered reference corrected verticle acceleration
% after 1st stride and detrend
aVert                       = accelDataRotated(tStrideSample + 1:end, 3) - mean(accelDataRotated(tStrideSample + 1:end, 3));
gAP                         = gyroData(tStrideSample + 1:end, 3);
% For iOS and Android, Z is the intrinsic AP axis. Counter clock-wise rotations are positive.
% iOS Reference: https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data/understanding_reference_frames_and_device_attitude
% Android Reference: https://developer.android.com/guide/topics/sensors/sensors_overview
% Thus, positive gyro angles correspond to right swing phase. At the right
% heel strike the phone is at its counter-clockwise peak.

height                      = personHeight; % Meters
L                           = height*0.5;   % Meter
fL                          = height*0.16;  % Meter

% Get gait events
[ICs, isLeftIC, ~]          = footEvents(aVert, gAP, fs, debugFlag);

[stepLengths, leftStepLengths,...
    rightStepLengths,...
    ~]                      = vertMovements(aVert, L, fL, fs, tStrideSample, ICs, isLeftIC, debugFlag);

stepTimes                   = diff(ICs)./fs;
leftStepTimes               = stepTimes(isLeftIC(2:end));
rightStepTimes              = stepTimes(~isLeftIC(2:end));
end

