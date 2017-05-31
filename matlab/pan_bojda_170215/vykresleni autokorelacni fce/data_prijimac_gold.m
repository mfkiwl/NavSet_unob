clear all

%pro generování požadovaného kódu odkomentuji řádek. hodnota ukazuje na
%začátek dat použitých pro zpracování

%hodnot=156100;     %posuv_0
%hodnot=215100;     %posuv_100m
%hodnot=273550;     %posuv_200m
%hodnot=379200;     %posuv_300m  379300
%hodnot=126200;     %posuv_400m, hodnot=50000;
%hodnot=77580;       %posuv_500m
%hodnot=175300;     %posuv_600m
%hodnot=166700;     %posuv_610m  166800
%hodnot=28000;       %posuv_620m
%hodnot=132400;     %posuv_630m  132500
%hodnot=117500;     %posuv_640m  117600
%hodnot=112900;     %posuv_650m  113000
%hodnot=22630;       %posuv_660m
%hodnot=142700;     %posuv_670m, hodnot=150000; pomaleji se zavesilo
%hodnot=136600;     %posuv_680m,  hodnot=150000; pomaleji se zavesilo (presnejsi nez pro100000)  136700
%hodnot=252700;     %posuv_690m,
%hodnot=105520;     %posuv_700m
%hodnot=49810;       %posuv_800m
%hodnot=4065;         %posuv_900m
%hodnot=83510;       %posuv_1000m, hodnot=100000;
%hodnot=57100;       %posuv_20000m
%hodnot=57100;       %posuv_40000m
%hodnot=591638;       %bojda_a1.dat
hodnot=443000;       %bojda_a3.dat
%hodnot=788540;       %bojda_rec.dat
fid = fopen('../../data/bojda_a3.dat','r');
y = fread(fid,hodnot*2,'uint8=>double');
hodnot=100000;
clear y
y = fread(fid,hodnot*2,'uint8=>double');

fid=fclose('all');
y = y - 127.5;
I(1:hodnot,1) =y(1:2:end);
Q(1:hodnot,1) =y(2:2:end);

%% generovani goldu
g1 = [1 0 0 0 0 0 0 0 0 0];
g2 = [1 0 0 0 0 0 0 0 0 0];
%g1 = [1 1 1 1 1 1 1 1 1 1];
%g2 = [1 1 1 1 1 1 1 1 1 1];

for i = 1:1023
    a(i) = mod(mod(g2(1,2)+g2(1,6),2)+g1(1,10),2);
    G1(i)=g1(1,10);
    temp = mod(g1(1,10)+g1(1,3),2);
    g1=[temp g1(1,1:end-1)];
    
    temp = mod(g2(1,10)+g2(1,9)+g2(1,8)+g2(1,6)+g2(1,3)+g2(1,2),2);
    g2=[temp g2(1,1:end-1)];
end

g1 = [1 0 0 0 0 0 0 0 0 0];
g2 = [1 0 0 0 0 0 0 0 0 0];
%g1 = [1 1 1 1 1 1 1 1 1 1];
%g2 = [1 1 1 1 1 1 1 1 1 1];

for i = 1:1023
    b(i) = mod(mod(g2(1,3)+g2(1,7),2)+g1(1,10),2);
    G2(i)=g2(1,10);
    temp = mod(g1(1,10)+g1(1,3),2);
    g1=[temp g1(1,1:end-1)];
    
    temp = mod(g2(1,10)+g2(1,9)+g2(1,8)+g2(1,6)+g2(1,3)+g2(1,2),2);
    g2=[temp g2(1,1:end-1)];
end

%% generovani obrazu
k = 9; %šířka 1 chipu = k+1 vzorků
%gold1
n = 1;
for i = 1:1023
    x = a(i);
   for ii = n:n+k
      obraz(1,ii) = x;
   end 
   n = n+k+1;
end

%gold2
n = 1;
for i = 1:1023
    x = b(i);
   for ii = n:n+k
      obraz(2,ii) = x;
   end 
   n = n+k+1;
end
obraz=obraz*2-1;