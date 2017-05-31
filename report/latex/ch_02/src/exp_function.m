% script to generate step response

max_t = .0002
t = 0: 1e-7:max_t;
tau = 24e-6;
c = 12/21+9/21*exp(-1/tau*t);

h1 = figure(1);
plot (t,c);
str = sprintf('Step Response');
grid on;title(str); xlabel('Time [ms]'); ylabel('Output Voltage');
axis([0,max_t,-0.01,1.14]);

set(h1,'PaperUnits','inches');
set(h1,'PaperOrientation','landscape');
Height = 3; Width = 4;
set(h1,'PaperSize',[Height,Width]);
set(h1,'PaperPosition',[0,0,Width,Height]);
print(h1,'-deps','-color','../img/step_response.eps');
print(h1,'-dtikz','-color','../img/step_response.tex');