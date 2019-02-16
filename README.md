# Typing-Trainer

I made this program with two objectives in mind. First, I wanted an exercise to practice my Python skills. Second, I wanted a application that I would use myself (eat your own dog food).

As it happens, I am using a lot the program [Klavaro](https://sourceforge.net/projects/klavaro/) these days to improve my typing ability. This is a great program that has most of what I need. However, I was getting tired of practicing always on the same text. To be fair Klavaro has an option for adding new texts, but I thought it would be nice if the program would load a new Wikipedia page every time. This way I will have endless examples and interesting text to practice on. And so I found my own user case.

## Program usage

Again, credits to Klavaro, as this is basically a slimmed down clon for my learning and personal use. It is a quite basic concept, where you get a text to type without looking at the keyboard. As you type, you see the letters coloring green or red if you do good or wrong respectively. To finish the exercise you'll have to correct your mistakes with Backspace as you go, until you reach the end. Furthermore:
- With the last Enter you'll get a summary screen that resumes how well you did.
- A link to the wikipedia page you just wrote is given in the summary in case you are feeling curious.
- You can follow your progress by the Progress button, invoking the KPIs plots of _Words per minute_, _Accuracy_, and _Score_.
- You have 5 difficulty levels by the maximum words that your text wil contain, although being the text collected randomly, there is variation in the number of words. In any case you get that information too on the upper right corner.
- You can choose from three languages for the exercise.
- You can always reload a new text if you don't like the current one.

<img src="https://github.com/josehoras/Typing-Trainer/blob/master/loading.png" alt="Loading"
	title="Loading screen" width="425" height="300" />
<img src="https://github.com/josehoras/Typing-Trainer/blob/master/training.png" alt="Training"
	title="Training screen" width="425" height="300" />
<img src="https://github.com/josehoras/Typing-Trainer/blob/master/summary.png" alt="Summary"
	title="Summary screen" width="425" height="300" />
<img src="https://github.com/josehoras/Typing-Trainer/blob/master/progress.png" alt="Progress"
	title="Progress screen" width="425" height="300" />
  
## Install

Simple GitHub cloning and Python running. The required libraries are _matplotlib_, _wikipedia_, and _six_ 
```
git clone https://github.com/josehoras/Typing-Trainer.git
cd Typing-Trainer/
pip3 install -r requirements.txt
python3 typing_trainer.py
```
