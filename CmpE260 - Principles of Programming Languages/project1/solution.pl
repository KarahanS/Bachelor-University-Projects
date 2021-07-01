% karahan saritas
% 2018400174
% compiling: yes
% complete: yes

% include the knowledge base
:- encoding(utf8).
:- ['load.pro'].


% 3.1 glanian_distance(Name1, Name2, Distance) 5 points

% Glanian Distance Calculator Predicates
gd(Distance, [], []) :-
    Distance is 0.
gd(Distance, [Head1 | Tail1], [Head2 | Tail2]) :-
    Head1 \= -1,
    gd(X, Tail1, Tail2),
    Distance is X + (Head1 - Head2)*(Head1 - Head2).
gd(Distance, [-1 | Tail1], [_ | Tail2]) :-
    gd(X, Tail1, Tail2),
    Distance is X.

glanian_distance(Name1, Name2, Distance) :-
    expects(Name1, _, X),
    glanian(Name2, _, Y),
    gd(D, X, Y), 
    Distance is sqrt(D).


% 3.2 weighted_glanian_distance(Name1, Name2, Distance) 10 points

% Weighted Glanian Distance Calculator Predicates
wgd(Distance, [], [], []) :-
    Distance is 0.
wgd(Distance, [Head1 | Tail1], [Head2 | Tail2], [Head3 | Tail3]) :-
    Head1 \= -1,
    wgd(X, Tail1, Tail2, Tail3),
    Distance is X + Head3 * (Head1 - Head2)*(Head1 - Head2).
wgd(Distance, [-1 | Tail1], [_ | Tail2], [_ | Tail3]) :-
    wgd(X, Tail1, Tail2, Tail3),
    Distance is X.

weighted_glanian_distance(Name1, Name2, Distance) :-
    expects(Name1, _, X),
    glanian(Name2, _, Y),
    weight(Name1, Z),
    wgd(D, X, Y, Z),  % execute just once.
    Distance is sqrt(D), !.

% 3.3 find_possible_cities(Name, CityList) 5 points

% Iterate through the habitant list and see if Name is a habitant of that city.
find_city(Name, [Head | Tail]) :-
    Head \= Name,
    find_city(Name, Tail).
find_city(Name, [Head | _]) :-
    Head = Name.

% City List = Current City of Name + Name's Liked Cities
% Instead, we could have just used union/3 built-in predicate, however it doesn't preserve the order we want. 
city_list([], [], [], _).
city_list([], [Head | Tail], Tail2, A) :-
    A = Head,
    city_list([], Tail, Tail2, A).
city_list([], [Head | Tail], [Head | Tail2], A):-
    A \= Head,
    city_list([], Tail, Tail2, A).
city_list([A], List1, [A | List2], A) :-
    city_list([], List1, List2, A).

find_possible_cities(Name, CityList) :-
    city(A, X, _),
    find_city(Name, X),
    % X is the city in which glanian is present 
    likes(Name, _, Y), % Y = liked cities
    city_list([A], Y, CityList, A), !.
    
% 3.4 merge_possible_cities(Name1, Name2, MergedCities) 5 points

% Find possible cities of each glanian and take the union of them.
merge_possible_cities(Name1, Name2, MergedCities) :-
    find_possible_cities(Name1, X),
    find_possible_cities(Name2, Y),
    union(X, Y, MergedCities).

% 3.5 find_mutual_activities(Name1, Name2, MutualActivities) 5 points


find_mutual_activities(Name1, Name2, MutualActivity) :-
    likes(Name1, X, _),
    likes(Name2, Y, _),
    intersection(X, Y, MutualActivity).

% 3.6 find_possible_targets(Name, Distances, TargetList) 10 points

% Find the distance between a glanian and a possible target that satisfies the requirements.
dist(Name, Target, Distance) :-
    expects(Name, GList, _),
    glanian(Target, G, _),
    % One should not match with himself.
    Name \= Target,
    member(G, GList),
    glanian_distance(Name, Target, Distance).

find_possible_targets(Name, Distances, TargetList) :-
    % Sorts the distances.
    setof([Distance, Target], dist(Name, Target, Distance), ListofPairs),
    findall(X, member([X, _], ListofPairs), Distances),
    findall(Y, member([_, Y], ListofPairs), TargetList).


% 3.7 find_weighted_targets(Name, Distances, TargetList) 15 points

% Similar to dist predicate, this time we calculate weighted glanian distance.
weighted_dist(Name, Target, Distance) :-
    expects(Name, GList, _),
    glanian(Target, G, _),
    Name \= Target,
    member(G, GList),
    weighted_glanian_distance(Name, Target, Distance).

find_weighted_targets(Name, Distances, TargetList) :-
    % Sorts the distances.
    setof([Distance, Target], weighted_dist(Name, Target, Distance), ListofPairs),
    findall(X, member([X, _], ListofPairs), Distances),
    findall(Y, member([_, Y], ListofPairs), TargetList).

% 3.8 find_my_best_target(Name, Distances, Activities, Cities, Targets) 20 points

% Finds the intersection of two lists. Used in 3.8 and 3.9 predicates.
intersect([],[],[]).
intersect([], _, []).
intersect([Head1 | List1], List2, [Head1 | List3]) :-
    member(Head1, List2),
    intersect(List1, List2, List3).
intersect([Head1 | List1], List2, List3) :-
    not(member(Head1, List2)),
    intersect(List1, List2, List3).


% Limit check (Limits of Name and features of target)
limit_check([], []).
limit_check([[] | Tail], [_ | Features]) :-
    limit_check(Tail, Features).
limit_check([[Low, High] | Tail], [F | Features]):-
    F > Low,
    F < High,
    limit_check(Tail, Features).

% Necessary check conditions for target
% If target satisfies the conditions, that it calculates weighted glanian distance
% These conditions are independent from activity and city.
comparison(Name, Target, Distance, DislikedActivities, Limit, GList) :-                                 
    glanian(Target, G, Features),                               
    likes(Target, LikedActivities, _),
    % Name != Target
    Name \= Target,
    % They don't have an old relation with each other.
    not(old_relation([Name, Target])),
    not(old_relation([Target, Name])),
    member(G, GList),
    % Intersection of Name's DislikedActivies and Target's LikedActivites are no more than two.
    intersect(DislikedActivities, LikedActivities, Conflicts),
    length(Conflicts, Length),
    Length =< 2,
    % Features of target are in the boundaries of Name's tolerance limits.
    limit_check(Limit, Features),
    weighted_glanian_distance(Name, Target, Distance).


% Helper check methods
% Name should either like City[i] or be a habitant of City[i]
check(Name, City, _) :-
    find_possible_cities(Name, List),
    member(City, List).
% Or there should be an Activity[i] in City[i] that is also in LikedActivities of Name.
check(Name, _, CityActivity) :-
    likes(Name, LikedActivities, _),
    member(CityActivity, LikedActivities).

% Necessary check conditions for city and activity
% If given city and activity satisfy the conditions, they are stored in the ListofQuadra.
city_check(Name, City, CityActivity, MergedList, DislikedActivities, DislikedCities) :-
    % City is in the merged list.
    member(City, MergedList),
    city(City, _, ActivityList),
    member(CityActivity, ActivityList),
    % City is not in disliked cities
    not(member(City, DislikedCities)),
    % Activity should not be in DislikedActivities of Name
    % There should be at least one activity in the city that satisfies this condition
    not(member(CityActivity, DislikedActivities)),
    check(Name, City, CityActivity).

goal(D, T, Name, City, CityActivity, ListofPairs, DislikedActivities, DislikedCities) :-
    member([D, T], ListofPairs),
    merge_possible_cities(Name, T, MergedList),
    city_check(Name, City, CityActivity, MergedList, DislikedActivities, DislikedCities).

find_my_best_target(Name, Distances, Activities, Cities, Targets) :-
    % First, store the information of Name
    dislikes(Name, DislikedActivities, _, Limit),              
    expects(Name, GList, _),   
    dislikes(Name, DislikedActivities, DislikedCities, _),                                  
    % fwd_modified finds all appropriate targets and relevant distances.
    setof([Distance, Target], comparison(Name, Target, Distance, DislikedActivities, Limit, GList), ListofPairs),
    % For each (D, T) pair, try different city and activity combinations.
    % If they satisfy the conditions, store these (D, A, C, T) quadras in ListofQuadra.
    setof([D, CityActivity, City, T], goal(D, T, Name, City, CityActivity, ListofPairs, DislikedActivities, DislikedCities), ListofQuadra),

    % Creating necessary lists from ListofQuadra.
    findall(X, member([X,_,_,_], ListofQuadra), Distances),
    findall(Y, member([_,Y,_,_], ListofQuadra), Activities),
    findall(Z, member([_,_,Z,_], ListofQuadra), Cities),
    findall(W, member([_,_,_,W], ListofQuadra), Targets).
    

    

% 3.9 find_my_best_match(Name, Distances, Activities, Cities, Targets) 25 points


% Necessary check conditions for target
% If target satisfies the conditions, that it calculates weighted glanian distance
comparison_advanced(Name, Target, Distance, G1, Features1, DislikedActivities1, Limit1, GList1, LikedActivities1) :-
   
    glanian(Target, G2, Features2),
    dislikes(Target, DislikedActivities2, _, Limit2),
    expects(Target, GList2, _),  
    likes(Target, LikedActivities2, _),
    
    % Name != Target
    Name \= Target,
    % They don't have an old relation with each other.
    not(old_relation([Name, Target])),
    not(old_relation([Target, Name])),
    member(G1, GList2),
    member(G2, GList1),
    % Intersection of Name's DislikedActivies and Target's LikedActivites are no more than two.
    intersect(DislikedActivities1, LikedActivities2, Conflicts1),
    length(Conflicts1, Length1),
    Length1 =< 2,
    % Intersection of Target[i]'s DislikedActivies and Name's LikedActivites are no more than two.
    intersect(DislikedActivities2, LikedActivities1, Conflicts2),
    length(Conflicts2, Length2),
    Length2 =< 2,
    % Features of target are in the boundaries of Name's tolerance limits.
    limit_check(Limit1, Features2), % Target[i]'s features should be in the tolerance limits of Name
    limit_check(Limit2, Features1), % Name's features should be in the tolerance limits of Target[i]
    weighted_glanian_distance(Name, Target, D1),
    weighted_glanian_distance(Target, Name, D2),
    Distance is (D1 + D2)/2.

% Necessary check conditions for city and activity
% If given city and activity satisfy the conditions, they are stored in the ListofQuadra.
city_check_advanced(Name, Target, City, CityActivity, MergedList, DislikedActivities1, DislikedCities1) :-
    % City is in the merged list.
    member(City, MergedList),
    city(City, _, ActivityList),
    member(CityActivity, ActivityList),
    dislikes(Target, DislikedActivities2, DislikedCities2, _),
    % City is not in disliked cities
    not(member(City, DislikedCities1)),
    not(member(City, DislikedCities2)),
    % Activity should not be in DislikedActivities of Name
    % There should be at least one activity in the city that satisfies this condition
    not(member(CityActivity, DislikedActivities1)),
    not(member(CityActivity, DislikedActivities2)),
    
    check(Name, City, CityActivity),
    check(Target, City, CityActivity).

goal_advanced(D, T, Name, City, CityActivity, ListofPairs, DislikedActivities1, DislikedCities1) :-
    member([D, T], ListofPairs),
    merge_possible_cities(Name, T, MergedList),
    city_check_advanced(Name, T, City, CityActivity, MergedList, DislikedActivities1, DislikedCities1).


find_my_best_match(Name, Distances, Activities, Cities, Targets) :-
    % Store the information of Name
    glanian(Name, G1, Features1),
    dislikes(Name, DislikedActivities1, _, Limit1),
    expects(Name, GList1, _),
    likes(Name, LikedActivities1, _),
    dislikes(Name, DislikedActivities1, DislikedCities1, _),

    % comparison_advanced finds all appropriate targets and relevant distances.
    setof([Distance, Target], comparison_advanced(Name, Target, Distance, G1, Features1, DislikedActivities1, Limit1, GList1, LikedActivities1), ListofPairs),
    % For each (D, T) pair, try different city and activity combinations.
    % If they satisfy the conditions, store these (D, A, C, T) quadras in ListofQuadra.
    setof([D, CityActivity, City, T], goal_advanced(D, T, Name, City, CityActivity, ListofPairs, DislikedActivities1, DislikedCities1), ListofQuadra),
    
    % Creating necessary lists from ListofQuadra.
    findall(X, member([X,_,_,_], ListofQuadra), Distances),
    findall(Y, member([_,Y,_,_], ListofQuadra), Activities),
    findall(Z, member([_,_,Z,_], ListofQuadra), Cities),
    findall(W, member([_,_,_,W], ListofQuadra), Targets).



% BONUS

% Implement a new predicate which you can decide its arguments that will find the 10 best matches in the whole database.
% Best match - lowest average of the two weighted distances

% Helper methods to write to a file
writeToFile_Helper(_, []) :- !.
writeToFile_Helper(File, [[G, T] |Tail]) :-
    write(File, G),
    write(File, ' '),
    write(File, T),
    write(File, '\n'),
    Tail = [[_, _] | Tail2],
    writeToFile_Helper(File, Tail2).

% Takes a file name and list. Writes the content of the list to the file.
writeToFile(Name, List) :-
    open(Name, write, File),
    writeToFile_Helper(File, List),
    close(File).

% Takes the first ten elements of a list and generates a new list with them.
takeFirstTen([], [], _).
takeFirstTen([_ | _], [], 20).
takeFirstTen([Head | Tail], [Head | Tail2], A) :-
    A < 20,
    L is A + 1,
    takeFirstTen(Tail, Tail2, L).

% It collects all the [Distance, Name, Target] triples with matching Name and Target.
% Then it takes first 20 elements of that list. We have to take 20 in order to deal with duplicates.
% Then we store [Name, Target] doubles to a new list.
% We send this list to the writer, to write its content to a file named "top10.txt"
bonus(Result):-
    setof([Distance, Name, Target], goal(Distance, Name, Target), List),
    takeFirstTen(List, Top10, 0),
    findall([G, T], member([_, G, T], Top10), Result),
    writeToFile("./top10.txt", Result), !.

% Name should be a glanian
% We should find matches of the Name
% Distance and Target should be extracted from the Matches
goal(Distance, Name, Target) :-
    glanian(Name, _, _),
    find_my_best_match_bonus(Name, Matches),
    member([Distance, Target], Matches).

% Slightly updated version of find_my_best_match
find_my_best_match_bonus(Name, Matches) :-
        % Store the information of Name
        glanian(Name, G1, Features1),
        dislikes(Name, DislikedActivities1, _, Limit1),
        expects(Name, GList1, _),
        likes(Name, LikedActivities1, _),
        dislikes(Name, DislikedActivities1, DislikedCities1, _),
    
        % comparison_advanced finds all appropriate targets and relevant distances.
        setof([Distance, Target], comparison_advanced(Name, Target, Distance, G1, Features1, DislikedActivities1, Limit1, GList1, LikedActivities1), ListofPairs),
        % For each (D, T) pair, try different city and activity combinations.
        % If they satisfy the conditions, store these (D, A, C, T) quadras in ListofQuadra.
        setof([D, T], goal_advanced(D, T, Name, _, _, ListofPairs, DislikedActivities1, DislikedCities1), Matches).
        