function [value, tstride]  = gsi(accelMat, fs, debugFlag)

figure;
arx             = acf(accelMat(:, 1), min(fs*4, length(accelMat(:, 1))-1));
ary             = acf(accelMat(:, 2), min(fs*4, length(accelMat(:, 2))-1));
arz             = acf(accelMat(:, 3), min(fs*4, length(accelMat(:, 3))-1));

g = gcf;
delete(g);

arx(arx<0)      = 0;
ary(ary<0)      = 0;
arz(arz<0)      = 0;

Cstep           = sqrt(arx+ary+arz);
[locAmps,locs]  = findpeaks(Cstep);

CstepLows       = find(Cstep <= 0.25*sqrt(3));
validityStart   = CstepLows(1);

pLocs           = locs(locs > 2*validityStart);
[~,tstrideAI]   = max(Cstep(pLocs));
tstrideA        = pLocs(tstrideAI);
tstepA          = round(tstrideA*0.5);
if(tstepA < validityStart)
    valueA      = 0;
else
    valueA      = Cstep(tstepA) / sqrt(3);
end


atLocB          = estimateStrideIndex(accelMat(:, 3), arz, fs, debugFlag);
[~, tstrideIB]  = min(abs(locs-atLocB));
tstrideB        = locs(tstrideIB);
tstepB          = round(tstrideB*0.5);
if(tstepB < validityStart)
    valueB      = 0;
else
    valueB      = Cstep(tstepB) / sqrt(3);
end

[~, tstrideCI]  = max(locAmps);
tstrideC        = locs(tstrideCI);
tstepC          = round(tstrideC*0.5);
if(tstepC < validityStart)
    valueC      = 0;
else
    valueC      = Cstep(tstepC) / sqrt(3);
end

[maxValue,...
    maxValInd]  = max([valueA valueB valueC]);
tstrideVect     = [tstrideA tstrideB tstrideC];

if(maxValue == 0)
    tstride     = max(tstrideVect);
else
    tstride     = tstrideVect(maxValInd);
end
tstep           = round(tstride*0.5);
value           = Cstep(tstep) / sqrt(3);

if debugFlag > 2
    figure;
    plot(Cstep);
    hold on;plot(tstride, Cstep(tstride), 'ro');
    plot(tstep, Cstep(tstep), 'kx');
    plot(tstrideA, 0.8, 'k+', 'MarkerSize', 12);
    plot(tstrideB, 0.8, 'k*', 'MarkerSize', 12);
    plot(tstrideC, 0.8, 'k^', 'MarkerSize', 12);
    legend({'Cstep', 'Tstride', 'Tstep'}, 'Interpreter', 'latex');
    hold off;
end

    function strideIndex    = estimateStrideIndex(aVert, arz, fs, debugFlag)
        
        [b, a]              = butter(2, 3/(fs/2), 'low');
        filteredData        = filtfilt(b,a, arz);
        
        [~, possibleLocs]   = findpeaks(filteredData);
        
        cwt_scale           = 16;
        aVertInt            = cumsum(aVert./fs);
        dy                  = derivative_cwt(aVertInt, 'gaus1', cwt_scale, 1/fs);
        [~, periodPeaks]    = findpeaks(-dy);
        period              = round(median(diff(periodPeaks))*2);
        
        [~, strideIndexI]   = min(abs(possibleLocs-period));
        strideIndex         = possibleLocs(strideIndexI);
        
        if debugFlag > 2
            figure;
            findpeaks(filteredData);
            hold on;
            plot(strideIndex, filteredData(strideIndex), 'ko');
            hold off;
        end
        
    end
end

