function [stepLengths, leftStepLengths, rightStepLengths, distance] = vertMovements(aVert, lLength, fLength, fs, tStride, ICs, isLeftIC, debugFlag)

OPTIMAL_K       = 0.584830;


v               = cumsum(-aVert./fs);

v               = v - movmean(v, tStride);

dp              = cumsum(v./fs);

dp              = dp - movmean(dp, tStride);

d_appended      = [flip(dp);dp;flip(dp)];
d_appended      = filterStream(d_appended, fs, 2, 45, 0.1, 1);

d               = d_appended(length(dp) + 1 : end - length(dp));



leftICs         = ICs(isLeftIC);
rightICs        = ICs(~isLeftIC);

if debugFlag
    figure
    plot(d)
    hold on;
    plot(leftICs, d(leftICs), 'bo');
    plot(rightICs, d(rightICs), 'ro');
    hold off;
    xlabel('Sample no.');
    ylabel('Vertical displacement m/sec/sec');
end


hs              = ones(1, length(ICs)-1);
hsLeft          = [];
hsRight         = [];

for i=2:min(length(ICs), length(isLeftIC))
    H           = d(ICs(i-1):ICs(i));
    hs(i-1)     = max(H) - (H(1) + H(end))/2;

    if isLeftIC(i)
        hsLeft  = [hsLeft, hs(i-1)];
    else
        hsRight = [hsRight, hs(i-1)];
    end
end

stepLengths             = 2.*sqrt(2.*lLength.*hs-hs.^2)             + OPTIMAL_K.*fLength;
leftStepLengths         = 2.*sqrt(2.*lLength.*hsLeft-hsLeft.^2)     + OPTIMAL_K.*fLength;
rightStepLengths        = 2.*sqrt(2.*lLength.*hsRight-hsRight.^2)   + OPTIMAL_K.*fLength;

distance                = sum(stepLengths) + 2*median(stepLengths);

if iscolumn(stepLengths)
    stepLengths         = stepLengths';
    leftStepLengths     = leftStepLengths';
    rightStepLengths    = rightStepLengths';
end
end

