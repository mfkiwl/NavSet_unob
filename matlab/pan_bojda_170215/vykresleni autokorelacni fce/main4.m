clear all
%%inicializace

data_prijimac_gold;
integr=100; %pocet vzorku ktery se suarizuje Ix a Qx
%------------------------------------------------------------------------
% NCO set
fs=2000000;
fc=1700;       
fnco = 10000;
tnco = 0:1/fnco:1;
NCO_source = sin(2*pi*tnco);
M = fnco/(fs/fc);
M = round(M);
c = 0;
clear tnco
%------------------------------------------------------------------------
s=I./(cos(atan(Q./I)));
kod=1;
k=1;        % krok o ktery se posouvaji pointry v masce
for posun=1:1023
%------------------------------------------------------------------------
% reset
% NCO
c = 0;
%DLL
    Ip(mod(i,integr)+1,1)=0;
    Ip2(mod(i,integr)+1,1)=0;
    Qp(mod(i,integr)+1,1)=0;
%------------------------------------------------------------------------
%------------------------------------------------------------------------
%DLL
        pointer_gold(1)=posun*k*10;
        if pointer_gold(1)>length(obraz)
            pointer_gold(1)=pointer_gold(1)-length(obraz);
        elseif pointer_gold(1)<1
            pointer_gold(1)=pointer_gold(1)+length(obraz);
        end
%% dll
for i=1:length(I)   
    %------------------------------------------------------------------
    %costas bez discriminatoru
        if c + M > fnco     %pojistka proti preteneni c
            c = (c + M) - fnco;
        elseif c<0          %pojistka proti podteceni c
            c = fnco + c;
        elseif c ==0
            c = fnco;
        end
        NCO_SIN = NCO_source(1,c);

        c = c + M;
    %------------------------------------------------------------------
        pointer_gold(1)=pointer_gold(1)+k;
        if pointer_gold(1)>length(obraz)
            pointer_gold(1)=pointer_gold(1)-length(obraz);
        elseif pointer_gold(1)<1
            pointer_gold(1)=pointer_gold(1)+length(obraz);
        end
       
    ans=mod(i,integr)+1;
    
    Ip(ans,1)=sign(I(i)*obraz(kod,pointer_gold(1))*sign(NCO_SIN));
    Ip2(ans,1)=sign(s(i)*obraz(kod,pointer_gold(1))*sign(NCO_SIN));
    Qp(ans,1)=sign(Q(i)*obraz(kod,pointer_gold(1))*sign(NCO_SIN));
    
    data(i,1)=Ip2(ans,1);
    
    if ans-1==0 
        %--------------------------------------------------------------------------
        %costas discriminator
        fi=atan2((sum(Ip)/length(Ip)),(sum(Qp)/length(Qp)));
        c=round((fi*fnco)/(2*pi))+M*length(Ip)/2;   %+M*ength(Ip)/2 z grafu nevim proc zrovna polovina (fnco=10000)
        %--------------------------------------------------------------------------
    end
    clear ans
end
korelace(posun)=sum(data)/length(data);
end