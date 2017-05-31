clear all
for qq=5
%%inicializace

data_prijimac_gold;
posun=0;
integr=200; %pocet vzorku ktery se suarizuje Ix a QxS
integr2=10000;%pocet vzorku po kerem se kontroluje lock
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

k=10;        % krok o ktery se posouvaji pointry v masce
for kod=1:2
%------------------------------------------------------------------------
% reset
    delta(1,3)=1;
    x=1;
    tau=0;
% NCO
c = 0;
%DLL
dll_lock=0;
    Ie=0;
    Ip=0;
    Il=0;
    Qe=0;
    Qp=0;
    Ql=0;
%------------------------------------------------------------------------
%------------------------------------------------------------------------
%DLL
if kod == 2
  if qq==25
      posun=-60;
      tau=posun;
  elseif qq==24
      posun=-40;
      tau=posun;
  end
end
        pointer_gold(1)=posun*k+30;
        pointer_gold(2)=posun*k+20;
        pointer_gold(3)=posun*k+10;
        for ii=1:3
        if pointer_gold(ii)>length(obraz)
            pointer_gold(ii)=pointer_gold(ii)-length(obraz);
        elseif pointer_gold(ii)<1
            pointer_gold(ii)=pointer_gold(ii)+length(obraz);
        end
        end
%% dll
for i=1:length(I) 
    
    if i==100000
       pause=1; 
    end
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
        ans=c-fnco/4;
        if ans<1
            NCO_CSIN= NCO_source(1,(ans)+fnco);
        else
             NCO_CSIN = NCO_source(1,ans);
        end
        clear ans
        graf_NCO_SIN(i)=NCO_source(1,c);
        c = c + M;
    %------------------------------------------------------------------
        pointer_gold(1)=pointer_gold(1)+k;
        if pointer_gold(1)+tau>length(obraz)
            pointer_gold(1)=pointer_gold(1)-length(obraz);
        elseif pointer_gold(1)+tau<1
            pointer_gold(1)=pointer_gold(1)+length(obraz);
        end
        
        pointer_gold(2)=pointer_gold(2)+k;
        if pointer_gold(2)+tau>length(obraz)
            pointer_gold(2)=pointer_gold(2)-length(obraz);
        elseif pointer_gold(2)+tau<1
            pointer_gold(2)=pointer_gold(2)+length(obraz);
        end

        pointer_gold(3)=pointer_gold(3)+k;
        if pointer_gold(3)+tau>length(obraz)
            pointer_gold(3)=pointer_gold(3)-length(obraz);
        elseif pointer_gold(3)+tau<1
            pointer_gold(3)=pointer_gold(3)+length(obraz);
        end
       
    ans=mod(i,integr)+1;  
    Ip(ans,1)=(I(i)*obraz(kod,pointer_gold(2)+tau));
    Qp(ans,1)=(Q(i)*obraz(kod,pointer_gold(2)+tau));
    
    Ie2(ans,1)=sign(s(i)*obraz(kod,pointer_gold(1)+tau)*sign(NCO_SIN));
    Ip2(ans,1)=sign(s(i)*obraz(kod,pointer_gold(2)+tau)*sign(NCO_SIN));
    Il2(ans,1)=sign(s(i)*obraz(kod,pointer_gold(3)+tau)*sign(NCO_SIN));
    
    data(i,1)=Ip2(ans,1);
    
    if ans-1==0    %pri vylucovani doplera nutne prizpusobovat automaticky
        if sum(Ip2)==0
            discriminator=0;
        else
            discriminator=sign((sum(Ie2)/length(Ie2)-sum(Il2)/length(Il2))/(sum(Ip2)/length(Ip2)));
            %discriminator=sign((sum(Ie)/length(Ie)-sum(Il)/length(Il))/(sum(Ip)/length(Ip)) + (sum(Qe)/length(Qe)-sum(Ql)/length(Ql))/(sum(Qp)/length(Qp)));
        end
        if dll_lock==1
            %delty(i/integr,kod)=pointer_gold(2);%pointer_gold(2);
            delty(i/integr,kod)=tau;
        else
            delty(i/integr,kod)=tau;
            %delty(i/integr,kod)=-999;
        end
        %test(i/integr,kod)=(sum(Ie2)/length(Ie2)-sum(Il2)/length(Il2))/(sum(Ip2)/length(Ip2));
        %pointer_gold=pointer_gold+k*discriminator;
            tau=tau+k*discriminator;
        %--------------------------------------------------------------------------
        %costas discriminator
        fi=atan2((sum(Ip)/length(Ip)),(sum(Qp)/length(Qp)));
        c=round((fi*fnco)/(2*pi))+M*length(Ip)/2;   %+M*ength(Ip)/2 z grafu nevim proc zrovna polovina (fnco=10000)
        %--------------------------------------------------------------------------
    end
    %-----------------------------------------------------------------------------
    %FFT
    %pamet_fft(mod(i,30000)+1,1)=Ip_graf(i);
    %if mod(i,10000)==0 & i>=length(pamet_fft)
    %    FFT_pokus
    %end
    %-----------------------------------------------------------------------------
    if mod(i,integr2)==0 %& i>=length(pamet_fft) PRO FFT CEKA AZ SE NAPLNI PAMET bacha na setrvacnost fft
        graf_prumery(i/integr2)=sum(data(i-integr2/4:i,1))/length(data(i-integr2/4:i,1));
        if sum(data(i-integr2/4:i,1))/length(data(i-integr2/4:i,1))<0.2
            %pointer_gold=pointer_gold-k*5;    %nastaveny pro kladne posuvy
            tau=tau-k*5;
           if dll_lock==1
                dll_lock=0;
           end
        else
            if dll_lock==0
                dll_lock=1;
            end
        end
    end
 x=x+1;%jen pro vykreslovani
vystup(kod,i)=tau/k;
end
y=y+1;
%% vykresleni
vykreslit=1;
t=1/fs:2000/fs:x*1/fs-1/fs;    %pro grafy

if vykreslit==1
%hold on
%plot(t,I,'b')
%hold on
%plot(Q,'r')
%hold on
%plot(t,data,'k')
%hold on
%plot(t,NCO_SIN_graf,'g')
%hold on
%plot(NCO_graf_csin,'g')
%hold on
%plot(test(:,2),'k')
%hold on
%plot(t,graf1,'b')
plot(graf_prumery,'k')
if kod ==1
hold on
end
%zero(1:length(I))=0;
%plot(zero,'r')
end
end
%% výpocet rozdílů
            delty(:,3)=(delty(:,1)-delty(:,2))/k;
            for kontrola=1:length(delty(:,3))
                %if delty(kontrola,1)>0 & delty(kontrola,2)>0 & abs(delty(kontrola,3))>1000
                    if delty(kontrola,1)==-999 | delty(kontrola,2)==-999
                       delty(kontrola,3)=0; 
                    else
                       %delty(kontrola,3)=length(obraz)+delty(kontrola,1)-delty(kontrola,2); %zvlada pouze zpozdeni 2. kodu
                    end
                %end
            end
            dt(1,1)=sum(delty(end-500:end,3))/length(delty(end-500:end,3));
            progress=text
            dt(2,1)=dt(1,1)*1/2 %us
            %dt(3,1)=median(delty(end-1000:end,3))
         %test=delty(end-1000:end,3);
         %figure
         %hist(test,100);
            delty(:,4)=delty(:,3)/2;
            
end