function [accelDataRotated, gyroData] = cgsPreprocessedData(accelData, rotData, gyroData, fs,...
    isPostQuat, isAndroid)

%% Convert acceleration units to m/sec/sec
accelData                           = accelData .* 9.8;

%% Correct for orientation <X-ML, Y-AP, Z-Verticle>
if isAndroid
    accelDataRotated = accelData;
    % Use the quiet period from the initial 2 sec segment as reference
    initialToReference = quat2rotm(median(rotData(fs+1:(1.5*fs), :)));
    referenceToInitial = initialToReference';
    gUser = accelDataRotated(1, :);
    zVector = -gUser;
    initialToXArbitZVerticle = gravity2rotm(zVector);
    referenceToXArbitZVerticle = initialToXArbitZVerticle * referenceToInitial;
    
    for i=1:length(accelDataRotated)
        frameToReference            = quat2rotm(rotData(i, :));
        frameToToXArbitZVerticle    = referenceToXArbitZVerticle * frameToReference;
        correctedSample             = frameToToXArbitZVerticle*(accelDataRotated(i,:)');
        accelDataRotated(i,:)       = correctedSample;
    end
else
    if isPostQuat
        accelDataRotated = accelData;
        for i=1:length(accelDataRotated)
            rotMat                  = quat2rotm(rotData(i, :));
            correctedSample         = rotMat*(accelDataRotated(i,:)');
            accelDataRotated(i,:)   = correctedSample;
        end
    else
        accelDataRotated = accelData;
        for i=1:length(accelDataRotated)
            rotMat                  = iOSRotationMatrix(rotData(i, :));
            correctedSample         = rotMat*(accelDataRotated(i,:)');
            accelDataRotated(i,:)   = correctedSample;
        end
    end
end

%% If Android: Remove initial 2 seconds
if isAndroid
    accelDataRotated    = accelDataRotated((2*fs)+1:end, :);
    gyroData            = gyroData((2*fs)+1:end, :);
end
end

