Use <- and -> to move left and right. The game ends if the randomly selected column for which the block falls is filled. 


Steps to run:
1) In the terminal, run python TetrisGame.py


How score is Calculated:
The Raw formula:
(((hours * 3600) + (minutes * 60) + (seconds * 0.5)) + g_numBlocksProcessed) * g_scoreMultiplier

For each second the player survive, they get 1 score. For each block processed, they get 1 score. 
This cumulative score is then multiplied with a score multiplier that is dependent on the size of the grid:
10x5 - 1x Multiplier
8x4  - 3x Multiplier
4x2 - 10x Multiplier
6x7 - 5x Multiplier
