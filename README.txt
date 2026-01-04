# Sudoku Puzzle Game

## 🎯 Overview
A complete Sudoku puzzle game built with Streamlit featuring an interactive 9x9 grid puzzle with game functionality, validation, and solving assistance.

## 🎮 Features
- **Interactive Game Board**: Click to select cells and input numbers
- **Difficulty Levels**: Easy, Medium, Hard, and Expert puzzles
- **Game Validation**: Real-time validation of moves
- **Hint System**: Get help when stuck
- **Auto-Solve**: Watch the algorithm solve the puzzle
- **Timer**: Track your solving time
- **Mistake Counter**: Keep track of errors
- **Visual Feedback**: Color-coded cells for different states
- **Responsive Design**: Works on desktop and mobile

## 📦 Installation

1. **Install Python** (3.8 or higher)

2. **Install required packages**:
```bash
pip install streamlit pandas numpy
1. Clone or download the game files

🚀 How to Run

1. Navigate to the project directory:

```bash
cd path/to/sudoku-game
```

1. Launch the game:

```bash
streamlit run sudoku_game.py
```

1. Open your browser and go to:

```
http://localhost:8501
```

🎯 How to Play

Basic Rules

1. Each row must contain numbers 1-9 without repetition
2. Each column must contain numbers 1-9 without repetition
3. Each 3x3 sub-grid must contain numbers 1-9 without repetition

Controls

· Click on any empty cell to select it
· Type numbers 1-9 to fill the cell
· Press 0 or Delete to clear a cell
· Use arrow keys to navigate between cells
· Space bar to get a hint

Game Interface

· Top Bar: Timer, difficulty selector, new game button
· Game Board: 9x9 Sudoku grid with color coding:
  · White: Empty cells
  · Light blue: Selected cell
  · Green: Correct numbers
  · Orange: Numbers with conflicts
  · Gray: Pre-filled puzzle numbers
· Side Panel: Game controls, hints, solve options

🎚️ Difficulty Levels

· Easy: 45-50 given numbers
· Medium: 35-40 given numbers
· Hard: 25-30 given numbers
· Expert: 17-22 given numbers

🛠️ Game Controls

Buttons:

· New Game: Start a fresh puzzle
· Check Solution: Validate your current progress
· Get Hint: Reveal one correct number
· Show Solution: Display the complete solved puzzle
· Reset Game: Clear all your inputs
· Pause/Resume: Control the timer

Keyboard Shortcuts:

· 1-9: Enter numbers
· 0 or Delete: Clear cell
· Arrow Keys: Navigate grid
· Space: Get hint
· Enter: Check solution

📁 Project Structure

```
sudoku_game/
├── sudoku_game.py          # Main game application
├── README.txt              # This documentation
├── puzzles/               # (Optional) Puzzle database
│   ├── easy_puzzles.json
│   ├── medium_puzzles.json
│   └── hard_puzzles.json
└── requirements.txt       # Python dependencies
```

🧩 Game Logic

Puzzle Generation

· Puzzles are generated using backtracking algorithms
· Ensures unique solutions
· Difficulty based on number of givens and logical complexity

Validation

· Real-time row, column, and sub-grid validation
· Immediate visual feedback for conflicts
· Complete solution verification

Solving Algorithm

· Uses backtracking with constraint propagation
· Can solve any valid Sudoku puzzle
· Step-by-step solving visualization available

🎨 Customization

Changing Theme

Modify the CSS in the game file:

```python
st.markdown("""
<style>
.sudoku-cell { /* Cell styles */ }
.timer { /* Timer styles */ }
/* etc. */
</style>
""", unsafe_allow_html=True)
```

Adding Puzzles

Add new puzzles to the puzzle dictionaries in the code:

```python
easy_puzzles = [
    [[5,3,0,0,7,0,0,0,0], ...],
    # Add more puzzles here
]
```

🐛 Troubleshooting

Common Issues:

1. Game not loading: Ensure all dependencies are installed
2. Input not working: Click the cell first, then type
3. Slow performance: Reduce browser extensions or clear cache
4. Display issues: Refresh the page (F5)

Solutions:

· Update Streamlit: pip install --upgrade streamlit
· Clear browser cache
· Restart the Streamlit server

📊 Scoring (Optional Feature)

· Time bonus: Faster completion = higher score
· Mistake penalty: Each error reduces score
· Hint penalty: Using hints reduces maximum possible score
· Difficulty multiplier: Harder puzzles = higher base score

🤝 Contributing

Feel free to:

· Add new puzzle sets
· Improve the UI/UX
· Optimize solving algorithms
· Add new features

📝 License

This Sudoku game is open source and free to use, modify, and distribute.

🙏 Credits

· Built with Streamlit
· Sudoku logic and algorithms
· UI/UX design for optimal gameplay

🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Ensure you have the latest versions
3. Contact the developer with specific error messages

---

Enjoy playing Sudoku! 🎮

Start the game with: streamlit run sudoku_game.py