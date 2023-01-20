% actions: forward, counterClockWise, clockWise, hit
% receptions: wumpusSmell, wumpusSight, bump

% helpers to avoid errors
bump(0) :- false.
wumpusSmell(0) :- false.
wumpusSight(0) :- false.
action(0, 0) :- false.

clockWise(east, south).
clockWise(south, west).
clockWise(west, north).
clockWise(north, east).

counterClockWise(X, Y) :- clockWise(Y, X).

forward(X, Y, XS, YS, east) :- XS is X, YS is Y + 1.
forward(X, Y, XS, YS, west) :- XS is X, YS is Y - 1.
forward(X, Y, XS, YS, north) :- XS is X - 1, YS is Y.
forward(X, Y, XS, YS, south) :- XS is X + 1, YS is Y.

% returns the last action
% be careful, there is still one action to be taken.
last(L) :- action(L, _), 
            L_ is L + 1, 
            \+ action(L_, _). 

% query: location - call locate from the beginning
location(I, X, Y, D) :- locate(I, X, Y, D, 1, 1, 1, east).
% destination is reached
locate(I, X, Y, F, IS, XS, YS, F) :- I is IS, X is XS, Y is YS.
% forward action
locate(I, X, Y, D, IS, XS, YS, F) :- IS_ is IS + 1,               
                               forward(XS, YS, XS_, YS_, F),
                               (action(IS, forward), \+ bump(IS_)),
                               locate(I, X, Y, D, IS_, XS_, YS_, F).
% rotate action
locate(I, X, Y, D, IS, XS, YS, F) :- IS_ is IS + 1,
                               \+ bump(IS_),
                               ( (action(IS, clockWise), clockWise(F, F_)); 
                                 (action(IS, counterClockWise), counterClockWise(F, F_))),
                               locate(I, X, Y, D, IS_, XS, YS, F_).
% hit or bump action (stay idle for both of them)
locate(I, X, Y, D, IS, XS, YS, F) :- IS_ is IS + 1,
                               (action(IS, hit); bump(IS_)),
                               locate(I, X, Y, D, IS_, XS, YS, F).

wallInFront(I) :- wall(I), !.
wall(I) :- location(I, X, Y, F), % we'll learn X, Y and F - according to F we'll calculate where the wall might be.
                forward(X, Y, XS, YS, F),  % calculate (XS, YS) given X, Y, F - to check if there is a wall in (XS, YS), we have to check if any location(S, X_, Y_, F_) exists with a proper forward action
                ((Y_ is YS - 1, location(S, XS, Y_, east), bump(S));
                 (Y_ is YS + 1, location(S, XS, Y_, west), bump(S));
                 (X_ is XS - 1, location(S, X_, YS, south), bump(S));
                 (X_ is XS + 1, location(S, X_, YS, north), bump(S))).


isWinner(I) :- I_ is I + 1, win(I_), !.  % Can agent be classified as a winner at the beginning of the action I_?
win(I) :- action(I_, hit),
          I_ < I,                                              % we know that there is a hit action before coming to here
          location(I_, X, Y, F),                              % let's learn the position of that hit action.
          forward(X, Y, XW, YW, F),                           % We hit XW, YW - so Wumpus is supposedly in (XW, YW). 
          smell(T_, XW, YW, A, B),                           
          wumpusSight(M),                                     % at some point, we saw that there was a wumpus out there (we had to)
          location(M, XS, YS, FS),                            % so, we got the sight of wumpus at location XS, YS and facing towards FS
          inSight(XS, YS, XW, YW, FS, D),                     % is XW, YW in sight of XS, FS? - you can see SW, YW from XS, FS faced towards D
          (sightCheck(XW, YW, FS, D); adj(A, B, XW, YW)).     % lastly we have to make sure that wumpus is not at some other place: candidates are other cellss

smell(S, XW, YW, A, B) :- ((Y_ is YW - 1, location(S, XW, Y_, _), wumpusSmell(S), A = XW, B = Y_);    % check if we got wumpus smell from anywhere
                        (Y_ is YW + 1, location(S, XW, Y_, _), wumpusSmell(S), A = XW, B = Y_);
                        (X_ is XW - 1, location(S, X_, YW, _), wumpusSmell(S), A = X_, B = YW);
                        (X_ is XW + 1, location(S, X_, YW, _), wumpusSmell(S), A = X_, B = YW)).

sightCheck(XW, YW, FS, D) :- (D is 4, reverse(FS, FS_), forward(XW, YW, XWR, YWR, FS_), noWumpus(XWR, YWR), forward(XWR, YWR, XWRR, YWRR, FS_), noWumpus(XWRR, YWRR), forward(XWRR, YWRR, XWRRR, YWRRR, FS_), noWumpus(XWRRR, YWRRR));
                            (D is 3, forward(XW, YW, XWD, YWD, FS), noWumpus(XWD, YWD), reverse(FS, FS_), forward(XW, YW, XWR, YWR, FS_), noWumpus(XWR, YWR), forward(XWR, YWR, XWRR, YWRR, FS_), noWumpus(XWRR, YWRR));
                            (D is 2, forward(XW, YW, XWD, YWD, FS), noWumpus(XWD, YWD), forward(XWD, YWD, XWDD, YWDD, FS), noWumpus(XWDD, YWDD), reverse(FS, FS_), forward(XW, YW, XWR, YWR, FS_), noWumpus(XWR, YWR));
                            (D is 1, forward(XW, YW, XWD, YWD, FS), noWumpus(XWD, YWD), forward(XWD, YWD, XWDD, YWDD, FS), noWumpus(XWDD, YWDD), forward(XWDD, YWDD, XWDDD, YWDDD, FS), noWumpus(XWDDD, YWDDD)).

adj(XW, YW, WA, WB) :-  (Y1 is YW - 1, (noWumpus(XW, Y1); (XW is WA, Y1 is WB))),    % check if we got wumpus smell from anywhere
                        (Y2 is YW + 1, (noWumpus(XW, Y2); (XW is WA, Y2 is WB))),
                        (X1 is XW - 1, (noWumpus(X1, YW); (X1 is WA, YW is WB))),
                        (X2 is XW + 1, (noWumpus(X2, YW); (X2 is WA, YW is WB))), !.

neighbor(X, Y, XN, YN) :- (XN is X - 1, YN is Y);
                          (XN is X + 1, YN is Y);
                          (YN is Y - 1, XN is X);
                          (YN is Y + 1, XN is X).
reverse(east, west).
reverse(west, east).
reverse(north, south).
reverse(south, north).

out(XW, YW) :- XW < 1; YW < 1.
% I assume that our agent doesn't end up in a Wumpus cell throughout his journey.


% there must exist at least one XF, YF such that you can see X, Y from XF, YF and you visited XF, YF at least once  ===> for all such XF, YF - there is no wumpusSight!

scoutPositions(T, X, Y) :- inSight(X, Y, XF, YF, F, _), reverse(F, F_), location(T, XF, YF, F_). 
% CHECK THE SMELL PART
noWumpus(X, Y) :-  out(X, Y), !;                      % out of boundaries
                   location(_, X, Y, _), !;           % we passed that cell once upon a time
                   (neighbor(X, Y, XN, YN), location(TS, XN, YN, _), TS_ is TS - 1, action(TS_, forward), \+ wumpusSmell(TS)), !;  % there was no smell in the neighbors
                   (bagof(T, scoutPositions(T, X, Y), List),  forall(member(T,List), \+ wumpusSight(T))), !.     % it was in our sight and we haven't seen wumpus
                    % X, Y = wumpus location -  we can see XF, YF from X, Y facing towards F - which means we can see X, Y from XF, YF facing towards F_

% can (XS, YS) be seen from X, Y?
inSight(X, Y, X, YS, east, D) :- Y_ is Y + 4, between(Y, Y_, YS), D is YS - Y.
inSight(X, Y, X, YS, west, D) :- Y_ is Y - 4, between(Y_, Y, YS), D is Y - YS.
inSight(X, Y, XS, Y, south, D) :- X_ is X + 4, between(X, X_, XS), D is XS - X.
inSight(X, Y, XS, Y, north, D) :- X_ is X - 4, between(X_, X, XS), D is X - XS.

% If we are at X, Y without smell - then adjacent cells are empty

%%%%% IMPORTANT %%%%%
% There is one vague point that might change the answer of the predicates:
% Should we consider all of the experience we had while answering the predicates or just the actions up until the step in query?
% For example, let's say in the 4. step, there is a wall in front of us but we do not know it yet.
% In 8. step, we bumped into that wall and learned its location.
% 10 is our last action. Now, we should evaluate the predicate wallInFront(4).
% Should wallInFront(4) be True? I assumed that it should be True because based on our overall experience, we know that there was a wall in front of us.
% I think this confusion is directly related to this question: 
% "What does wallInFront(X) mean?":
        %   a) "Do we know that there was a wall in front of the agent at step X according to the whole knowledge base we have?"
        %   b) "Do we know that there was a wall in front of the agent at step X according to the knowledge we gathered up until step X?"
        % I assumed it to be the first one (a).
        % I also implemented the second one (but didn't send) - you just have to check each time if the rule we are using is coming from a previous action.
 


% Copy paste the experince below: 
action(1,forward).
bump(2).
action(2,clockWise).
action(3,forward).
action(4,counterClockWise).
action(5,forward).
action(6,counterClockWise).