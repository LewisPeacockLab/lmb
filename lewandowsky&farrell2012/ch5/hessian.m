function h = hessian(lnLfun,theta,delta, varargin)
% The argument lnLfun should be passed as a string
%   e.g., 'exGausslnL'
% The function expects the free parameters to be 
%   provided in a single vector theta, 
%   and additional arguments (including the data)
%   can be passed in varargin (see MATLAB help for
%   varargin)
% delta is the step size in the Hessian calculations

% e is the identity matrix multiplied by delta, and is used
%   to set up the e_i's and e_j's efficiently;
%   we just select the appropriate row in the loop
e = eye(length(theta)).*delta;
for i=1:length(theta)
    for j=1:length(theta)
        C(i,j) = feval(lnLfun, theta+e(i,:)+e(j,:), varargin{:})-...
            feval(lnLfun, theta+e(i,:)-e(j,:), varargin{:})-...
            feval(lnLfun, theta-e(i,:)+e(j,:), varargin{:})+...
            feval(lnLfun, theta-e(i,:)-e(j,:), varargin{:});
    end
end
h = C./(4.*(delta.^2));
