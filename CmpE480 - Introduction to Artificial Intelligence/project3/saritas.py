# Robot is located in an arbitrary cell in the upper row

# Emission probability:
on_if_wall = 0.7       # off_if_wall = 1 - 0.7 = 0.3
off_if_not_wall = 0.8  # on_if_not_wall = 1 - 0.8 = 0.2
 
# Uncertainty in actions
move_if_even = 0.8   # stay_if_even = 0.2
move_if_odd = 0.6    # stay_if_odd = 0.4

# sensor, move, sensor, move, sensor, move, sensor, move 
def solve(walls, sensors):
    if(len(walls) == 1): # if there is only one cell, the answer is clear
        return 1, 1

    probs = [1 / (len(walls))] * (len(walls))  # probability of robot's being in cell x
    # indices start from 1
    
    off_if_wall = 1.0 - on_if_wall
    on_if_not_wall = 1.0 - off_if_not_wall

    stay_if_even = 1.0 - move_if_even
    stay_if_odd = 1.0 - move_if_odd

    for sensor in sensors:
        # first get the sensor - update the probs
        if(sensor == "on"): probs = [p * on_if_wall if w == "x" else p * on_if_not_wall for p, w in zip(probs, walls)]
        else: probs = [p * off_if_wall if w == "x" else p * off_if_not_wall for p, w in zip(probs, walls)]
        # now, get the move

        prevProbs = probs.copy()
        # treat probs[0] and probs[-1] carefully
        probs[0] = prevProbs[0] * stay_if_odd  # index is actually 1
        for i in range(1, len(probs) - 1):
            id = i + 1
            if(id % 2 == 0): probs[i] = prevProbs[i] * stay_if_even + prevProbs[i - 1] * move_if_odd
            else: probs[i] = prevProbs[i] * stay_if_odd + prevProbs[i - 1] * move_if_even
        
        # last element is even
        if(len(probs) % 2 == 0): probs[-1] = prevProbs[-1] * 1.0 + prevProbs[-2] * move_if_odd
        else:  probs[-1] = prevProbs[-1] * 1.0 + prevProbs[-2] * move_if_even

    max_prob = max(probs) 
    #print([round(p, 4) for p in probs])
    index_max = probs.index(max_prob)
    summed = sum(probs)
    normalized = [prob * (1.0 / summed) for prob in probs]
    return index_max + 1, normalized[index_max]

def main():
    walls="x xx  xx x"
    sensors=["on","on","off","on"]

    robot_pos, robot_pos_prob = solve(walls, sensors)
    print("The most likely current position of the robot is", robot_pos, "with probability", robot_pos_prob)

if __name__ == "__main__":
    main()
