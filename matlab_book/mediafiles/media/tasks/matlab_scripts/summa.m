function [y] = summa(x)
    y = 0
    for i=1:3
        y = y+ str2int(x(i));
    end
end