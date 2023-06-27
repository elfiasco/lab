function [accelData, rotData, timeVect, gyroData] = loadGBExportedFilePostQuat(fs, filePath)


if nargin < 2

    text = fileread('next_sample.txt');
    % File selection
    %[fileName, folderName]  = uigetfile('*.csv', 'Pick a CSV file exported from innerEar');
    
    % Load Data
    %fileData                = importfilePostQuat(fullfile(folderName, fileName));
    fileData=importfilePostQuat(text);
    display(text);
    
else
    
    % Load Data
    fileData                = importfilePostQuat(filePath);
  
end


% Convert first column to double time vector
fileData.Timestamp          = seconds(fileData.Timestamp - fileData.Timestamp(1)) + 1/fs;

%% Do Preprocessing
accelData                   = [fileData.AccelX fileData.AccelY fileData.AccelZ];

rotData                     = [fileData.QuatW fileData.QuatX fileData.QuatY fileData.QuatZ];
timeVect                    = fileData.Timestamp;

gyroData                    = [fileData.GyroX fileData.GyroY fileData.GyroZ];

end

