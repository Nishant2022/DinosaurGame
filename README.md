<h2>About</h2>
<p>This is my version of the Google Chrome Dinosaur Game.
It was created in python with the pygame library.</p>
<h2>About the Dinosaur Game</h2>
<p>The Dinosaur Game is an infinite runner game, where the goal is to run for as long as possible. Obsticals, such as cacti and birds, appear as you run, and progressivly get faster. The player is able to duck and jump to avoid the obsticals.</p>
<h2>My Version</h2>
<p>All code is held in the <a href="DinosaurGame.py">DinosaurGame.py</a> file.
When the <code>main()</code> function is executed, all assets are loaded before the main game loop runs. 
During this time, the program checks if the data folder exists and if the score.txt file exists. If either do not exists, it will create the directory or file. The score.txt file is necessary to save the player's high score after the game is closed. </p>
<p>For each group of assets: Dinosaur, ground, obsticals, and clouds, there are functions to create, move, and delete them.</p>
<p>On startup, the very first game has a special animation in the beginning, to emulate what happens on the Google Chrome version</p>
<h3>How to Play</h3>
<p>To run the game, first run the <a href="DinosaurGame.py">DinosaurGame.py</a> file. 
To start the game press the <kbd>w</kbd> or <kbd>Up Arrow</kbd> keys.</p>
<p>The controls are as follows:</p>
<ul>
    <li><kbd>w</kbd> and <kbd>Up Arrow</kbd>: jump.</li>
    <li><kbd>s</kbd> and <kbd>Down Arrow</kbd>: duck.</li>
</ul>