    IQ = I(1:length(I)/4).*Q(1:length(I)/4);
    ans = fft(IQ);

    P2 = abs(ans/(length(I)/4));
    P1 = P2(1:(length(I)/4)/4);
    [num,idx] = max(P2);
    fc = fs*(idx-1)/(length(I)/4)/2;
    
    M=fnco/(fs/fc);
    M=round(M);
    clear ans