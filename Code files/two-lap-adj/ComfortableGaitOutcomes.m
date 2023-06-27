%% Setup

clear
close all
clc

%% Constants
FS                              = 100;
IS_POST_QUAT                    = 1;                                       % Android always has POST_QUAT ON
IS_ANDROID                      = 0;                                       % Must check
DEBUG_FLAG                      = 0;

%% Load data
if IS_POST_QUAT; [accelData, rotData, timeVect, gyroData]   = loadGBExportedFilePostQuat(FS);
else [accelData, rotData, timeVect, gyroData]               = loadGBExportedFile(FS);end
%% Plot data
%% Plot raw data

%%plot(timeVect(1:length(accelData)), detrend(accelData))
%%ylabel('Acceleration (g/sec/sec)')
%%title('Detrended raw data')

%% Compute and print outcomes
personHeight                    = 1.52;         % Meters
[outcomes, outcomeString]       = cgOutcomes(timeVect, accelData, rotData, gyroData, FS, personHeight, IS_POST_QUAT, IS_ANDROID, DEBUG_FLAG);

disp(outcomeString)

fileID = fopen('test.txt','w');
fprintf(fileID,outcomeString);
fclose(fileID);