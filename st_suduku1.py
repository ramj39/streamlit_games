import streamlit as st
import numpy as np
import random
import time
st.markdown(
    """
    <style>
    .stDataFrame td {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Set page configuration
st.set_page_config(
    page_title="Sudoku Game",
    page_icon="🔢",
    layout="wide"
)

# Custom CSS with proper font styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sudoku-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        max-width: 550px;
    }
    .timer {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding: 10px;
        background-color: #F0F9FF;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .number-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    /* Style for the sudoku grid cells */
    .sudoku-cell {
        width: 50px;
        height: 50px;
        border: 1px solid #94A3B8;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px !important;  /* Larger font size */
        font-weight: bold !important;
    }
    
    .thick-right {
        border-right: 3px solid #1E293B !important;
    }
    
    .thick-bottom {
        border-bottom: 3px solid #1E293B !important;
    }
    
    /* Given numbers (gray) */
    .given-cell {
        background-color: #F1F5F9;
        color: #1E293B !important;
        font-size: 28px !important;
    }
    
    /* User cells (blue numbers) */
    .user-cell {
        background-color: white;
        color: #1E40AF !important;  /* Blue color for user numbers */
        font-size: 28px !important;
        cursor: pointer;
    }
    
    .user-cell:hover {
        background-color: #E0F2FE;
    }
    
    /* Selected cell */
    .selected-cell {
        background-color: #BFDBFE !important;
        border: 2px solid #3B82F6 !important;
        color: #1E40AF !important;
        font-size: 28px !important;
    }
    
    /* Error cells */
    .error-cell {
        background-color: #FEE2E2 !important;
        color: #DC2626 !important;
        font-size: 28px !important;
    }
    
    /* Hint cells */
    .hint-cell {
        background-color: #FEF3C7 !important;
        color: #D97706 !important;
        font-size: 28px !important;
    }
    
    /* Custom styling for number buttons */
    .stButton > button {
        height: 50px !important;
        width: 50px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Clear button styling */
    .clear-btn {
        background-color: #FEE2E2 !important;
        color: #DC2626 !important;
        border-color: #FCA5A5 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

class SudokuGame:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.board = None
        self.solution = None
        self.user_board = None
        self.start_time = None
        self.end_time = None
        self.hints_used = 0
        self.errors = 0
        self.generate_new_puzzle()
    
    def generate_new_puzzle(self):
        # Generate a complete Sudoku solution
        self.solution = self.generate_solution()
        
        # Create puzzle by removing numbers based on difficulty
        self.board = np.copy(self.solution)
        self.user_board = np.copy(self.board)
        
        # Number of cells to remove based on difficulty
        difficulty_levels = {
            'easy': 35,
            'medium': 45,
            'hard': 50,
            'expert': 55
        }
        
        cells_to_remove = difficulty_levels.get(self.difficulty, 45)
        
        # Remove numbers randomly
        all_positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(all_positions)
        
        removed = 0
        for i, j in all_positions:
            if removed >= cells_to_remove:
                break
            
            temp = self.board[i][j]
            self.board[i][j] = 0
            self.user_board[i][j] = 0
            
            if self.has_unique_solution():
                removed += 1
            else:
                self.board[i][j] = temp
                self.user_board[i][j] = temp
        
        self.start_time = time.time()
        self.end_time = None
        self.hints_used = 0
        self.errors = 0
    
    def generate_solution(self):
        board = np.zeros((9, 9), dtype=int)
        
        def fill_board(board, row=0, col=0):
            if row == 9:
                return True
            if col == 9:
                return fill_board(board, row + 1, 0)
            if board[row][col] != 0:
                return fill_board(board, row, col + 1)
            
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            
            for num in numbers:
                if self.is_valid(board, row, col, num):
                    board[row][col] = num
                    if fill_board(board, row, col + 1):
                        return True
                    board[row][col] = 0
            return False
        
        # Fill diagonal boxes first
        for i in range(0, 9, 3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for r in range(3):
                for c in range(3):
                    board[i + r][i + c] = numbers.pop()
        
        fill_board(board)
        return board
    
    def is_valid(self, board, row, col, num):
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        if num in board[box_row:box_row+3, box_col:box_col+3]:
            return False
        return True
    
    def has_unique_solution(self):
        board_copy = np.copy(self.board)
        
        def count_solutions(board, count=0):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid(board, i, j, num):
                                board[i][j] = num
                                count = count_solutions(board, count)
                                if count > 1:
                                    return count
                                board[i][j] = 0
                        return count
            return count + 1
        
        return count_solutions(board_copy) == 1
    
    def get_hint(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.user_board[row][col] = self.solution[row][col]
            self.hints_used += 1
            return row, col
        return None
    
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] != self.solution[i][j]:
                    return False
        self.end_time = time.time()
        return True
    
    def check_errors(self):
        errors = []
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] != 0:
                    temp = self.user_board[i][j]
                    self.user_board[i][j] = 0
                    
                    if not self.is_valid(self.user_board, i, j, temp):
                        errors.append((i, j))
                    
                    self.user_board[i][j] = temp
        return errors
    
    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        if self.end_time is not None:
            return int(self.end_time - self.start_time)
        return int(time.time() - self.start_time)
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = SudokuGame()
if 'show_errors' not in st.session_state:
    st.session_state.show_errors = False
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'hint_cell' not in st.session_state:
    st.session_state.hint_cell = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'selected_cell' not in st.session_state:
    st.session_state.selected_cell = None

# Main app
st.markdown('<div class="main-header">🔢 Interactive Sudoku</div>', unsafe_allow_html=True)
st.markdown("**Click a cell, then click a number button below to enter it**")

# Sidebar
with st.sidebar:
    st.header("🎮 Game Controls")
    
    # Difficulty
    difficulty = st.selectbox(
        "Difficulty",
        ["easy", "medium", "hard", "expert"],
        index=1
    )
    
    # New game
    if st.button("🔄 New Game", type="primary", use_container_width=True):
        st.session_state.game = SudokuGame(difficulty)
        st.session_state.show_errors = False
        st.session_state.show_hint = False
        st.session_state.hint_cell = None
        st.session_state.game_over = False
        st.session_state.selected_cell = None
        st.success(f"New {difficulty} game started!")
        st.rerun()
    
    st.divider()
    
    # Game helpers
    st.subheader("Helpers")
    
    if st.button("💡 Get Hint", use_container_width=True):
        if not st.session_state.game_over:
            hint_cell = st.session_state.game.get_hint()
            if hint_cell:
                st.session_state.show_hint = True
                st.session_state.hint_cell = hint_cell
                st.success(f"Hint given! ({st.session_state.game.hints_used} used)")
            else:
                st.warning("No empty cells!")
            st.rerun()
    
    if st.button("🔍 Check Errors", use_container_width=True):
        if not st.session_state.game_over:
            st.session_state.show_errors = True
            errors = st.session_state.game.check_errors()
            if errors:
                st.warning(f"Found {len(errors)} errors!")
            else:
                st.success("No errors!")
            st.rerun()
    
    if st.button("✅ Check Solution", type="primary", use_container_width=True):
        if not st.session_state.game_over:
            if st.session_state.game.check_solution():
                st.session_state.game_over = True
                st.balloons()
                st.success("🎉 Puzzle solved!")
            else:
                st.error("Solution incorrect!")
            st.rerun()
    
    st.divider()
    
    # Stats
    if st.session_state.game:
        st.subheader("📊 Stats")
        game = st.session_state.game
        st.write(f"**Time:** {game.format_time(game.get_elapsed_time())}")
        st.write(f"**Hints:** {game.hints_used}")
        filled = 81 - np.count_nonzero(game.user_board == 0)
        st.write(f"**Progress:** {filled}/81")
        st.write(f"**Difficulty:** {game.difficulty.title()}")

# Main game area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Timer
    if not st.session_state.game_over:
        elapsed = st.session_state.game.get_elapsed_time()
        st.markdown(f'<div class="timer">⏱️ {st.session_state.game.format_time(elapsed)}</div>', unsafe_allow_html=True)
    
    # Sudoku grid
    game = st.session_state.game
    board = game.user_board
    original = game.board
    
    st.markdown('<div class="sudoku-container">', unsafe_allow_html=True)
    
    # Display the grid
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                # Determine cell value
                cell_value = original[i][j] if original[i][j] != 0 else board[i][j]
                display_text = str(cell_value) if cell_value != 0 else ""
                
                # Determine cell styling
                cell_class = "sudoku-cell"
                
                # Thick borders for 3x3 boxes
                if j % 3 == 2 and j < 8:
                    cell_class += " thick-right"
                if i % 3 == 2 and i < 8:
                    cell_class += " thick-bottom"
                
                # Check cell type
                if original[i][j] != 0:
                    # Given cell - gray background, dark text
                    cell_class += " given-cell"
                    # Display as markdown with styling
                    st.markdown(f'<div class="{cell_class}">{display_text}</div>', unsafe_allow_html=True)
                else:
                    # User cell - make it clickable
                    
                    # Check if selected
                    if st.session_state.selected_cell == (i, j):
                        cell_class += " selected-cell"
                    
                    # Check for errors
                    if st.session_state.show_errors:
                        errors = game.check_errors()
                        if (i, j) in errors:
                            cell_class += " error-cell"
                    
                    # Check for hint
                    if st.session_state.show_hint and st.session_state.hint_cell == (i, j):
                        cell_class += " hint-cell"
                    
                    # Add user cell class (blue numbers)
                    cell_class += " user-cell"
                    
                    # Create a clickable button for the cell
                    if st.button(display_text, key=f"cell_{i}_{j}", use_container_width=True):
                        st.session_state.selected_cell = (i, j)
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Number buttons
    st.markdown('<div class="number-buttons">', unsafe_allow_html=True)
    
    # Create number buttons 1-9
    for num in range(1, 10):
        if st.button(str(num), key=f"num_{num}", use_container_width=True):
            if st.session_state.selected_cell:
                i, j = st.session_state.selected_cell
                if original[i][j] == 0:  # Only update if not a given cell
                    game.user_board[i][j] = num
                    st.rerun()
    
    # Clear button with custom styling
    if st.button("✕", key="clear", type="secondary", use_container_width=True):
        if st.session_state.selected_cell:
            i, j = st.session_state.selected_cell
            if original[i][j] == 0:
                game.user_board[i][j] = 0
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply custom CSS to the clear button
    st.markdown("""
    <style>
        button[kind="secondary"][data-testid="baseButton-secondary"] {
            background-color: #FEE2E2 !important;
            color: #DC2626 !important;
            border-color: #FCA5A5 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Instructions
    if st.session_state.selected_cell:
        i, j = st.session_state.selected_cell
        st.info(f"Selected: Row {i+1}, Column {j+1}")
        if original[i][j] == 0:
            st.caption("Click a number above to enter it in this cell")
    else:
        st.info("Click on any empty cell to select it, then click a number")
    
    # Game status
    if st.session_state.game_over:
        st.success(f"🎉 **Solved!** Time: {game.format_time(game.get_elapsed_time())}")
    #elif game.is_complete():
        st.warning("All cells filled! Click 'Check Solution' to verify.")

# Bottom section
st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    # Progress
    filled = 81 - np.count_nonzero(game.user_board == 0)
    progress = filled / 81
    st.subheader("Progress")
    st.progress(progress)
    st.caption(f"{filled}/81 cells ({progress*100:.0f}%)")

with col5:
    # Quick actions
    st.subheader("Quick Actions")
    
    if st.button("Clear All My Numbers", use_container_width=True):
        for i in range(9):
            for j in range(9):
                if original[i][j] == 0:
                    game.user_board[i][j] = 0
        st.session_state.show_errors = False
        st.session_state.selected_cell = None
        st.success("Cleared all your numbers!")
        st.rerun()
    
    if st.button("Show Next Number", use_container_width=True):
        if not st.session_state.game_over:
            # Find first empty cell and fill with solution
            for i in range(9):
                for j in range(9):
                    if game.user_board[i][j] == 0:
                        game.user_board[i][j] = game.solution[i][j]
                        st.session_state.selected_cell = (i, j)
                        st.success(f"Revealed number at Row {i+1}, Column {j+1}")
                        st.rerun()
                        break
                else:
                    continue
                break
            else:
                st.warning("No empty cells left!")

with col6:
    # Tips
    st.subheader("Tips")
    st.markdown("""
    1. **Start** with rows/columns that have the most numbers
    2. **Look** for numbers that can only go in one place
    3. **Use** the hint system if stuck
    4. **Check** errors regularly to avoid mistakes
    """)

# Instructions
with st.expander("📖 How to Play", expanded=True):
    st.markdown("""
    ### **Simple Steps:**
    
    1. **Select a cell**: Click on any empty white square
    2. **Enter a number**: Click a number button (1-9)
    3. **Clear a cell**: Select cell → Click ✕ button
    4. **Get help**: Use buttons in sidebar
    
    ### **Color Guide:**
    - **🟦 Gray cells**: Given numbers (cannot change)
    - **🔵 Blue numbers**: Your entries (can change)
    - **🔵 Blue border**: Currently selected cell
    - **🟥 Red background**: Error detected
    - **🟨 Yellow background**: Hint provided
    
    ### **Rules:**
    - Each row: Numbers 1-9 (no repeats)
    - Each column: Numbers 1-9 (no repeats)
    - Each 3×3 box: Numbers 1-9 (no repeats)
    -To save the game as pdf :rt click and click print in the pop-up menu
    -**Enjoy the game!** 🎯
    """)
st.write("developed by Subramanian Ramajayam")
# Footer
st.divider()
st.caption("🔢 Sudoku Game • All numbers now have same font size • Blue = your numbers, Gray = given numbers")



