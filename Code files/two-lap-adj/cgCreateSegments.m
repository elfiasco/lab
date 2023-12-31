function [accelDataSegments, rotDataSegments, gyroDataSegments] = cgCreateSegments(timeVect, accelData, rotData, gyroData)

%% Create four segments of data using timeVect
dataPauseStarts = find(diff(timeVect) > 1);
accelDataSegments = {accelData(1:dataPauseStarts(1), :), ...
    accelData(dataPauseStarts(1) + 1:end, :)...
    };
rotDataSegments = {rotData(1:dataPauseStarts(1), :), ...
    rotData(dataPauseStarts(1) + 1:end, :)...
    };
gyroDataSegments = {gyroData(1:dataPauseStarts(1), :), ...
    gyroData(dataPauseStarts(1) + 1:end, :)...
    };
end

