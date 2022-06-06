# JaneStreetPuzzle

August 2021 : Puzzle - https://www.janestreet.com/puzzles/robot-tug-of-war-index/

## Question:

The Robot Weightlifting World Championship was such a huge success that the organizers have hired you to help design its sequel: a Robot Tug-of-War Competition!

In each one-on-one matchup, two robots are tied together with a rope. The center of the rope has a marker that begins above position 0 on the ground. The robots then alternate pulling on the rope. The first robot pulls in the positive direction towards 1; the second robot pulls in the negative direction towards -1. Each pull moves the marker a uniformly random draw from [0,1] towards the pulling robot. If the marker first leaves the interval [‑½,½] past ½, the first robot wins. If instead it first leaves the interval past -½, the second robot wins.

However, the organizers quickly noticed that the robot going second is at a disadvantage. They want to handicap the first robot by changing the initial position of the marker on the rope to be at some negative real number. Your job is to compute the position of the marker that makes each matchup a 50-50 competition between the robots. Find this position to seven significant digits—the integrity of the Robot Tug-of-War Competition hangs in the balance!

## Methodology

- Simulated 1 game starting at an arbitrary starting point
- Simulated multiple games from starting points incremented from -0.5 to 0.5 (note scale set by interval for convenience. simply divide by interval to normalise axis so values range from -1 to 1, instead of -1e5 to 1e5 if interval is set to 1e5)

- Recorded winner of the multiple trials at the different starting points and converted to percentages. I.e. p1 wins 41% of the time in 1000 gmaes played that had a starting point of -0.4 (when scale normalised).


- Plotted the probability distribution to show the pribability of p1 winning| starting point x (conditioned on particular starting point)
- Through visual inspection, identified that distribution quite noisy, but that there was a clear underlying monotonic tread (continually increasing where function does not have an inflection point)
- Took averages over rolling window to sooth outh the distribution. Used centrally-weighted rolling window to avoid skewing the averaged values
- Inspected results using different sizes of rolling windows (covering 10, 100 and 1000 increments respectively)

- Found the location of the porbability closest to 0.5 to ensure that game as fair as possible.

## Answers
- -0.2847645  (correct to 3sf) - https://www.janestreet.com/puzzles/robot-tug-of-war-solution/
  - Averaged using window 1000 increments wide. 2e3 games were played at each position on the discretised axis


## Imporvements next time
- Implement in Java or C++ so runs faster and can set interval to >1e7 (10 million). This will achieve the required degree of accuracy


