function [y] = sum_3(x)
    x_str = num2str(x);
    y =0;
    for i=1:size(x_str, 2)
        y = y + str2num(x_str(i));
    end
end
