function predictions = witness (parms)
% Implementation of the WITNESS model for
% "Computational Modeling in Cognition: Principles and Practice"

global consts;

rand ('state', consts.seed)        %*\label{line:7:reseed}*\%

s    = parms(1);                 %*\label{line:7:p1}*\%
sim  = parms(2);
ssp  = sim;
paSim= sim;
ppSim= sim;             %*\label{line:7:p7}*\%

predictions = zeros (consts.nCond, 3);
for reps=1:consts.nRep   %*\label{line:7:mainloop}*\%
    %obtain perpetrator and perform holdup
    perp=getvec(consts.n);
    m=storevec (s, perp);  %*\label{line:7:holdup}*\%
    
    %get an innocent suspect
    inSus=getsimvec(ssp, perp);  %*\label{line:7:innocent}*\%
    %create both types of lineup
    paLineup (1,:)= inSus;     %*\label{line:7:lineup}*\%
    ppLineup (1,:)= perp;    %*\label{line:7:lineup1}*\%
    for i=2:consts.lSize  %*\label{line:7:lineloop1}*\%
        paLineup (i,:) =  getsimvec (paSim, perp);
        ppLineup (i,:) =  getsimvec (ppSim, perp);
    end   %*\label{line:7:lineloop2}*\%
    
    %eyewitness inspects lineup
    for i=1:consts.lSize   %*\label{line:7:lineloop3}*\%
        paMatch(i) = dot(paLineup(i,:), m);
        ppMatch(i) = dot(ppLineup(i,:), m);
    end   %*\label{line:7:lineloop4}*\%

    %witness responds
    for iLineup=1:consts.nCond   %*\label{line:7:tolloop}*\%
        if any(iLineup==consts.fChoice)
            criterion=0;  %*\label{line:7:fccriterion}*\%
        else
            criterion=parms(consts.ptToCrit(iLineup));   %*\label{line:7:criteria}*\%
        end
        if any(iLineup==consts.paLineup)   %*\label{line:7:whichlup}*\%
            useMatch = paMatch;
        else
            useMatch = ppMatch;
        end
        resp = decision (useMatch, criterion);
        predictions (iLineup, resp) = predictions(iLineup, resp) + 1;   %*\label{line:7:preds}*\%
    end              %*\label{line:7:tolloop2}*\%
end %rep loop
predictions = predictions/consts.nRep;  %*\label{line:7:getprops}*\%


%------ miscellaneous embedded functions 
%get random vector
    function rv = getvec (n)  %*\label{line:7:getvec}*\%
        rv = (rand(1,n)-0.5);
    end

%take a vector and return one of specified similarity
    function outVec=getsimvec (s, inVec)    %*\label{line:7:getsimvec}*\%
        a = rand(1,length(inVec)) < s;
        outVec = a.*inVec  + ~a.*getvec(length(inVec));
    end

%encode a vector in memory
    function m=storevec (s, inVec)     %*\label{line:7:storevec}*\%
        m = getsimvec(s, inVec);    
    end

%implement the decision rules
    function resp = decision(matchValues, cRec)  %*\label{line:7:df1}*\%
        %if all lineup members fall below cRec, then reject
        if max(matchValues) < cRec   %*\label{line:7:dfrej}*\%
            resp=3;
        else
            [c,j]=max(matchValues);
            if j == 1    %suspect or perp always first   %*\label{line:7:dfperp}*\%
                resp=1;
            else
                resp=2;
            end
        end
    end    %*\label{line:7:df2}*\%
end