%clear all
if qq==1
hodnot=156100;     %posuv_0
text='../../data/posuvy/posuv_0';
elseif qq==2
hodnot=215079;     %posuv_100m
text='../../data/posuvy/posuv_100m';
elseif qq==3
hodnot=273550;     %posuv_200m
text='../../data/posuvy/posuv_200m';
elseif qq==4
hodnot=379200;     %posuv_300m  379300
text='../../data/posuvy/posuv_300m';
elseif qq==5
hodnot=126200;     %posuv_400m, hodnot=50000;
text='../../data/posuvy/posuv_400m';
elseif qq==6
hodnot=77580;       %posuv_500m
text='../../data/posuvy/posuv_500m';
elseif qq==7
hodnot=175300;     %posuv_600m
text='../../data/posuvy/posuv_600m';
elseif qq==8
hodnot=166700;     %posuv_610m  166800
text='../../data/posuvy/posuv_610m';
elseif qq==9
hodnot=28000;       %posuv_620m
text='../../data/posuvy/posuv_620m';
elseif qq==10
hodnot=132400;     %posuv_630m  132500
text='../../data/posuvy/posuv_630m';
elseif qq==11
hodnot=117585;     %posuv_640m  117600
text='../../data/posuvy/posuv_640m';
elseif qq==12
hodnot=112900;     %posuv_650m  113000
text='../../data/posuvy/posuv_650m';
elseif qq==13
hodnot=22630;       %posuv_660m
text='../../data/posuvy/posuv_660m';
elseif qq==14
hodnot=142700;     %posuv_670m, hodnot=150000; pomaleji se zavesilo
text='../../data/posuvy/posuv_670m';
elseif qq==15
hodnot=136600;     %posuv_680m,  hodnot=150000; pomaleji se zavesilo (presnejsi nez pro100000)  136700
text='../../data/posuvy/posuv_680m';
elseif qq==16
hodnot=252700;     %posuv_690m,
text='../../data/posuvy/posuv_690m';
elseif qq==17
hodnot=105520;     %posuv_700m
text='../../data/posuvy/posuv_700m';
elseif qq==18
hodnot=49810;       %posuv_800m
text='../../data/posuvy/posuv_800m';
elseif qq==19
hodnot=4065;         %posuv_900m
text='../../data/posuvy/posuv_900m';
elseif qq==20
hodnot=83510;       %posuv_1000m, hodnot=100000;
text='../../data/posuvy/posuv_1000m';
elseif qq==21
hodnot=173023;       %posuv_2000m
text='../../data/posuvy/posuv_2000m';
elseif qq==22
hodnot=205528;       %posuv_5000m
text='../../data/posuvy/posuv_5000m';
elseif qq==23
hodnot=292306;       %posuv_10000m
text='../../data/posuvy/posuv_10000m';
elseif qq==24
hodnot=180548;       %posuv_15000m
text='../../data/posuvy/posuv_15000m';
elseif qq==25
hodnot=57100;       %posuv_20000m
text='../../data/posuvy/posuv_20000m';
end
%hodnot=443000;       %bojda_a3.dat
%text='../../data/bojda_a3.dat';
%hodnot=272870;       %pokus_g2
%hodnot=391889;       %pokus_g1,2

fid = fopen(text,'r');
y = fread(fid,hodnot*2,'uint8=>double');
hodnot=100000;
clear y
y = fread(fid,hodnot*2,'uint8=>double');

fid=fclose('all');
y = y - 127.5;
I(1:hodnot,1) =y(1:2:end)/40;
Q(1:hodnot,1) =y(2:2:end)/40;

% generovani goldu

%g1 = [1 1 1 1 1 1 1 1 1 1];
%g2 = [1 1 1 1 1 1 1 1 1 1];
g1 = [1 0 0 0 0 0 0 0 0 0];
g2 = [1 0 0 0 0 0 0 0 0 0];

for i = 1:1023
    a(i) = mod(mod(g2(1,2)+g2(1,6),2)+g1(1,10),2);
    G1(i)=g1(1,10);
    temp = mod(g1(1,10)+g1(1,3),2);
    g1=[temp g1(1,1:end-1)];
    
    temp = mod(g2(1,10)+g2(1,9)+g2(1,8)+g2(1,6)+g2(1,3)+g2(1,2),2);
    g2=[temp g2(1,1:end-1)];
end

%g1 = [1 1 1 1 1 1 1 1 1 1];
%g2 = [1 1 1 1 1 1 1 1 1 1];
g1 = [1 0 0 0 0 0 0 0 0 0];
g2 = [1 0 0 0 0 0 0 0 0 0];

for i = 1:1023
    b(i) = mod(mod(g2(1,3)+g2(1,7),2)+g1(1,10),2);
    G2(i)=g2(1,10);
    temp = mod(g1(1,10)+g1(1,3),2);
    g1=[temp g1(1,1:end-1)];
    
    temp = mod(g2(1,10)+g2(1,9)+g2(1,8)+g2(1,6)+g2(1,3)+g2(1,2),2);
    g2=[temp g2(1,1:end-1)];
end

%generovani obrazu
k = 99; %šířka 1 chipu = k+1 vzorků
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