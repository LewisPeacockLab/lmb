function [Jac] = quickJacobian(x, y, varargin)
Np = length(x);
Nd = length(y);
Jac = zeros(Nd,Np);
epsilon = sqrt(eps);

% Iterate over parameters to estimate columns of 
% Jacobian by finite differences.
for i=1:Np
    x_offset = x;
    x_offset(i) = x_offset(i) + epsilon;

    % get model predictions for offset parameter vector.
    f_offset = feval(varargin{1},x_offset,varargin{2:end});
    Jac(:,i) = (f_offset - y)/epsilon;        
end
