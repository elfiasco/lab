function [ICs, isLeftIC, FCs] = footEvents(aVert, gAP, fs, debugFlag)

cwt_scale       = 16;

aVertInt        = cumsum(aVert./fs);

dy_olden        = derivative_cwt(aVertInt, 'gaus1', cwt_scale, 1/fs, 0);

% dy              = diff_cwtft(aVertInt', cwt_scale, 1/fs);
% dyy             = diff_cwtft(dy, cwt_scale, 1/fs);

gAPSmooth       = lowPassStream(gAP, fs, 2);


% [~, ICs]        = findpeaks(-dy);

[~, ICs_olden]  = findpeaks(-dy_olden);

% if length(ICs) == length(ICs_olden)
%     fprintf("CWT rms error: %.3f ms\n", (rms(ICs - ICs_olden) / fs)*1000)
% else
%     fprintf("CWT length mismatch\n");
% end

ICs             = ICs_olden;

% ICs(ICs < fs/4) = [];

% [~, FCs]        = findpeaks(dyy);

isLeftIC        = gAPSmooth(ICs) < 0;

% Detect anamoly in isLeftIC and apply pattern based correction.

if(sum(abs(diff(isLeftIC))) ~= (length(isLeftIC) - 1))
    warning('Consecutive ICs are not from opposite sides. Applying pattern based correction.');
    candidateA = repmat([1;0], 20, 1);
    candidateB = repmat([0;1], 20, 1);
    
    candidateA = candidateA(1:min(length(isLeftIC), length(candidateA)));
    candidateB = candidateB(1:min(length(isLeftIC), length(candidateB)));

    isLeftIC = isLeftIC(1:min(length(isLeftIC), length(candidateA)));

    
    errorA     = sqrt(sum((candidateA - isLeftIC).^2));
    errorB     = sqrt(sum((candidateB - isLeftIC).^2));
    
    if errorA < errorB
        isLeftIC = candidateA == 1;
    else
        isLeftIC = candidateB == 1;
    end
end

leftICs         = ICs(isLeftIC);
rightICs        = ICs(~isLeftIC);

if debugFlag > 1
    figure
    plot(aVert, 'Color', [0, 0.4470, 0.7410]);
    hold on;
    plot(leftICs, aVert(leftICs), 'bo');
    plot(rightICs, aVert(rightICs), 'ro');
    % plot(FCs, aVert(FCs), 'kx');
    plot(gAPSmooth./peak2peak(gAPSmooth).*peak2peak(aVert), 'Color', [0.8500, 0.3250, 0.0980]);
    hold off;
    xlabel('Sample no.');
    ylabel('Vertical acceleration m/sec/sec');
end

FCs             = [];
end

